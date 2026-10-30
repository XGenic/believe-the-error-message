"""Study P1: does the give-up effect depend on the exact wording of the error? See PROTOCOL_P1.md.

Every earlier study used one sentence per stated cause. The give-up effect, the paper's cleanest result, is
measured against the neutral message over the same transient fault: "ERROR: stock data for this depot is
unavailable." against "ERROR: request rejected." P1 adds three rewordings of the "unavailable" message and
one of the neutral message, all over the transient fault (the first two calls of a request fail):

  original       ERROR: stock data for this depot is unavailable.     (C4)
  on_record      ERROR: this depot has no stock data on record.         another sentence, the same cause
  not_available  ERROR: stock information is not available for this depot.   a close rewording
  code_404       ERROR 404: no stock data found for this depot.         a status-code style
  neutral original       ERROR: request rejected.                       (C4)
  neutral not_completed  ERROR: the request could not be completed.     another neutral sentence

The system prompt is C4's, unchanged. Cells are (wording, claim, fault): the claim slot says which message
family the wording belongs to ("permanent" or "neutral"), and the fault is always "transient".

Per subject, for each "unavailable" wording w: the effect of w is success under w minus success under the
original neutral message. Primary verdict: GENERALIZES if every rewording has an effect that is DIFFERENT
and negative by study N1's rule; SPECIFIC if none does; PARTIAL otherwise; NOT_TESTABLE if the original
wording itself has no such effect. Secondary: each rewording minus the original wording, each effect against
the second neutral sentence, and the second neutral sentence minus the first.
"""

from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List, Optional, Tuple

from causetest.e2 import _boot, cell_lines, cell_table, validity_reasons
from causetest.env import CLAIM_TEXT
from causetest.w6 import pair_label

# Agent-facing text. Fixed here, before any P1 call.
UNAVAILABLE = {
    "original": CLAIM_TEXT["permanent"],
    "on_record": "ERROR: this depot has no stock data on record.",
    "not_available": "ERROR: stock information is not available for this depot.",
    "code_404": "ERROR 404: no stock data found for this depot.",
}
NEUTRAL = {
    "original": CLAIM_TEXT["neutral"],
    "not_completed": "ERROR: the request could not be completed.",
}
FAMILY = {"permanent": UNAVAILABLE, "neutral": NEUTRAL}
FAULT = "transient"
REWORDINGS = tuple(w for w in UNAVAILABLE if w != "original")


def valid_cell(arm: str, claim: str, fault: str) -> bool:
    return fault == FAULT and claim in FAMILY and arm in FAMILY[claim]


def message_for(arm: str, claim: str) -> str:
    return FAMILY[claim][arm]


# ---------------------------------------------------------------- measures

def contrasts_p1(stats: Dict[Tuple[str, str, str], List[Tuple[float, float]]]) -> Dict[str, Optional[float]]:
    def succ(arm, claim):
        v = stats.get((arm, claim, FAULT))
        return mean(x[0] for x in v) if v else None

    def diff(a, b):
        return None if a is None or b is None else a - b

    base, alt = succ("original", "neutral"), succ("not_completed", "neutral")
    out: Dict[str, Optional[float]] = {}
    for w in UNAVAILABLE:
        out[f"effect|{w}"] = diff(succ(w, "permanent"), base)
        out[f"effect_vs_second_neutral|{w}"] = diff(succ(w, "permanent"), alt)
        if w != "original":
            out[f"vs_original|{w}"] = diff(succ(w, "permanent"), succ("original", "permanent"))
    out["second_neutral_vs_first"] = diff(alt, base)
    return out


def subject_verdict(est: Dict[str, Optional[float]], labels: Dict[str, str]) -> str:
    """Decision rule (PROTOCOL_P1.md), applied in order."""
    keys = [f"effect|{w}" for w in UNAVAILABLE]
    if any(labels.get(k, "NOT_ESTIMABLE") == "NOT_ESTIMABLE" for k in keys):
        return "NOT_ESTIMABLE"

    def lowers(w):
        return labels[f"effect|{w}"] == "DIFFERENT" and est[f"effect|{w}"] < 0
    if not lowers("original"):
        return "NOT_TESTABLE"
    n = sum(lowers(w) for w in REWORDINGS)
    return "GENERALIZES" if n == len(REWORDINGS) else "SPECIFIC" if n == 0 else "PARTIAL"


def summarize_p1(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    th, n_runs = cfg["thresholds"], cfg["runs_per_cell"]
    stats, details, validity = cell_table(rows, cfg)
    est = contrasts_p1(stats)
    ci = _boot(stats, cfg["bootstrap_reps"], cfg["bootstrap_seed"], contrasts_p1)
    labels = {k: pair_label(est[k], ci.get(k, (None, None))) for k in est}
    verdict = subject_verdict(est, labels)
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "P1",
         "n_tasks": int(cfg.get("n_tasks", 6)), "runs_per_cell": n_runs, "estimates": est,
         "ci": {k: list(v) for k, v in ci.items()}, "labels": labels, "contrast_verdicts": {"primary": verdict},
         "cells": details, "validity": validity}
    invalid = validity_reasons(validity, th)
    if verdict == "NOT_ESTIMABLE":
        invalid.append("some wording could not be estimated")
    s["verdict"] = ({"verdict": "INVALID", "reasons": invalid} if invalid else
                    {"verdict": "VALID", "reasons": [f"primary: {verdict}"]})
    return s


# ---------------------------------------------------------------- report

def _f(x) -> str:
    return "n/a" if x is None else f"{x:+.3f}"


def verdict_markdown_p1(s: Dict[str, Any]) -> str:
    v, est, cells = s["verdict"], s["estimates"], s["cells"]

    def cell(k):
        if k not in est:
            return "n/a"
        lo, hi = s["ci"].get(k, (None, None))
        return f"{_f(est[k])} [{_f(lo)}, {_f(hi)}] {s['labels'].get(k)}"

    def level(arm, claim):
        x = cells.get(f"{arm}|{claim}|{FAULT}", {}).get("success")
        return "n/a" if x is None else f"{x:.2f}"

    lines = [f"# C4 study P1 verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; {s['n_tasks']} requests per run, "
             f"{s['runs_per_cell']} runs per cell. Every cell has the transient fault (the first two calls fail).", ""]
    if v["verdict"] == "INVALID":
        lines += [f"- {r}" for r in v["reasons"]] + [""]
    lines += [f"## Primary: does each rewording of \"unavailable\" lower success against the neutral message? "
              f"**{s['contrast_verdicts']['primary']}**", "",
              "| Wording | Text | Success | Effect vs \"request rejected\" | Minus the original wording | "
              "Effect vs the second neutral sentence |", "|---|---|---|---|---|---|"]
    for w, text in UNAVAILABLE.items():
        lines.append(f"| {w} | {text} | {level(w, 'permanent')} | {cell('effect|' + w)} | "
                     f"{cell('vs_original|' + w) if w != 'original' else ''} | {cell('effect_vs_second_neutral|' + w)} |")
    lines += ["", "## Neutral messages", "", "| Wording | Text | Success |", "|---|---|---|"]
    lines += [f"| {w} | {text} | {level(w, 'neutral')} |" for w, text in NEUTRAL.items()]
    lines += ["", f"- Second neutral sentence minus the first: {cell('second_neutral_vs_first')}"]
    return "\n".join(lines + cell_lines(s))
