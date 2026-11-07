"""Study G1: is Gemini's give-up result about reasoning or about the model? See PROTOCOL_G1.md.

In W2-E, Gemini 3.8 Flash at its default solved 61% of the give-up trap, and no other arm passed 15%. It is also the
only arm that reasons much on the trap's first request: a mean of 686 tokens, against at most 88 elsewhere. W2-E ran one
setting per model, so it cannot separate the two. G1 changes reasoning in both directions, on C4's seeds, and compares
each new run with the W2-E run of the same model:

  Sonnet at effort max, against Sonnet at its default: about Gemini's reasoning, on another model.
    RISES   the trap's success is DIFFERENT and higher by study N1's rule
    STAYS   it is not, and success stays at or below PANEL_MAX
  Gemini at reasoning low, against Gemini at its default: less reasoning, on the same model.
    FALLS   the trap's success is DIFFERENT and lower by study N1's rule
    HOLDS   it is not, and the interval for success stays above PANEL_MAX

An arm whose reasoning did not move as intended is NOT_TESTABLE. Anything else is UNCLEAR. The study's verdict:
REASONING_MATTERS if Sonnet RISES; GEMINI_ITSELF if Sonnet STAYS and Gemini HOLDS; GEMINI_SPECIFIC if Sonnet STAYS and
Gemini FALLS; UNCLEAR otherwise; INVALID if a new run fails the C4 validity rules.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from statistics import mean, median
from typing import Any, Dict, List, Optional, Sequence, Tuple

from causetest.compare import DIFF_MIN, _success, verdict as n1_verdict
from causetest.e2 import validity_reasons
from causetest.probe import tokens
from causetest.score import first_responses

TRAP, NEUTRAL = ("permanent", "transient"), ("neutral", "transient")
PANEL_MAX = 0.15  # the highest give-up-trap success on any arm but Gemini is 0.144 (GPT-6-luna, native, medium)
REACHES_GEMINI = 0.5  # Sonnet at max must reason at least this share of Gemini's mean on the trap's request 1
BELOW_GEMINI = 0.75  # Gemini at low must reason at most this share of Gemini's mean at its default
RUNS = {"sonnet_max": "g1-claude-sonnet-5-5-max", "sonnet_default": "w2e-c4-claude-sonnet-5-5",
        "gemini_low": "g1-gemini-3-8-flash-low", "gemini_medium": "w2e-c4-gemini-3-8-flash"}


def _in_cell(rows: List[Dict[str, Any]], cell: Tuple[str, str]) -> List[Dict[str, Any]]:
    return [r for r in rows if r["status"] == "complete" and (r["claim"], r["fault"]) == cell]


def request1_reasoning(row: Dict[str, Any]) -> int:
    """Reasoning tokens over all of a run's first request, the request that decides most runs (W2-E)."""
    return sum(tokens(t["meta"].get("usage") or {})["reasoning"] for t in row["tasks"][0]["turns"])


def cell_details(rows: List[Dict[str, Any]], cell: Tuple[str, str]) -> Dict[str, Any]:
    rs = _in_cell(rows, cell)
    if not rs:
        return {"runs": 0}
    n_tasks = len(rs[0]["tasks"])
    first = sorted(request1_reasoning(r) for r in rs)
    turns = [t for r in rs for task in r["tasks"] for t in task["turns"]]
    after = [0, 0]
    for r in rs:
        seen = False
        for task in r["tasks"]:
            if seen:
                after = [after[0] + bool(task["summary"]["success"]), after[1] + 1]
            seen = seen or bool(task["summary"]["success"])
    return {"runs": len(rs), "success": mean(_success(r) for r in rs),
            "success_by_request": [mean(float(r["tasks"][i]["summary"]["success"]) for r in rs) for i in range(n_tasks)],
            "correct": mean(float(t["summary"]["correct"]) for r in rs for t in r["tasks"]),
            "calls_per_request": mean(t["summary"]["calls"] for r in rs for t in r["tasks"]),
            "third_call_on_request_1": sum(r["tasks"][0]["summary"]["calls"] >= 3 for r in rs),
            "solved_after_a_solved_request": after,
            "runs_solving_all_or_none": sum(_success(r) in (0.0, 1.0) for r in rs),
            "reasoning_request_1": {"mean": mean(first), "median": median(first), "p90": first[int(0.9 * len(first))]},
            "reasoning_per_call": mean(tokens(t["meta"].get("usage") or {})["reasoning"] for t in turns)}


def summarize_g1(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    from causetest.runner import cells_for  # local import, as in extension.py
    n_runs, cells = cfg["runs_per_cell"], cells_for(cfg)
    complete = [r for r in rows if r["status"] == "complete"]
    by_cell = {c: _in_cell(rows, c) for c in cells}
    turns = sum(t["summary"]["agent_turns"] for r in complete for t in r["tasks"])
    bad = sum(t["summary"]["format_errors"] + t["summary"]["over_budget"] for r in complete for t in r["tasks"])
    first = [x for r in complete for x in first_responses(r) if x is not None]
    engagement = [mean(float(r["tasks"][0]["summary"]["calls"] > 0) for r in rs) for rs in by_cell.values() if rs]
    validity = {"completion_min": min(len(rs) / n_runs for rs in by_cell.values()),
                "completion": {"|".join(c): len(rs) / n_runs for c, rs in by_cell.items()},
                "protocol_failure_share": bad / turns if turns else None,
                "engagement_min": min(engagement) if engagement else None,
                "unclassifiable_share": (sum(x == "UNCLASSIFIABLE" for x in first) / len(first)) if first else None}
    invalid = validity_reasons(validity, cfg["thresholds"])
    return {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "G1",
            "n_tasks": int(cfg.get("n_tasks", 6)), "runs_per_cell": n_runs, "validity": validity,
            "cells": {"|".join(c): cell_details(rows, c) for c in cells},
            "verdict": ({"verdict": "INVALID", "reasons": invalid} if invalid else
                        {"verdict": "VALID", "reasons": ["the study's verdict comes from `python -m causetest g1`"]})}


def verdict_markdown_g1(s: Dict[str, Any]) -> str:
    v = s["verdict"]
    lines = [f"# C4 study G1, one run: {v['verdict']}", "", f"**{s['label']}**: transport `{s['transport']}`, model "
             f"`{s['model']}`; {s['n_tasks']} requests per run, {s['runs_per_cell']} runs per cell.", ""]
    lines += [f"- {r}" for r in v["reasons"]] + ["", "| Cell | Runs | Solved | Third call on request 1 | Reasoning on "
              "request 1: mean, median, p90 | Reasoning per call |", "|---|---|---|---|---|---|"]
    for name, c in s["cells"].items():
        if c["runs"]:
            r = c["reasoning_request_1"]
            lines.append(f"| {name} | {c['runs']} | {c['success']:.3f} | {c['third_call_on_request_1']} | "
                         f"{r['mean']:.0f}, {r['median']:.0f}, {r['p90']} | {c['reasoning_per_call']:.0f} |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- the study's verdict


def _interval(values: List[float]) -> Tuple[float, float]:
    values = sorted(values)
    return values[int(0.025 * len(values))], values[int(0.975 * len(values)) - 1]


def contrast(new: Sequence[float], base: Sequence[float], reps: int, seed: int) -> Dict[str, Any]:
    """New run minus base run, on per-run success: runs resampled within each run independently, as in study N1."""
    rng = random.Random(seed)
    level, diff = [], []
    for _ in range(reps):
        a = mean(rng.choices(new, k=len(new)))
        level.append(a)
        diff.append(a - mean(rng.choices(base, k=len(base))))
    d, (d_lo, d_hi), (lo, hi) = mean(new) - mean(base), _interval(diff), _interval(level)
    return {"new": mean(new), "new_ci": [lo, hi], "base": mean(base), "delta": d, "delta_ci": [d_lo, d_hi],
            "label": n1_verdict(d, d_lo, d_hi)}


def sonnet_arm(c: Dict[str, Any], reaches: bool) -> str:
    if not reaches:
        return "NOT_TESTABLE"
    if c["label"] == "DIFFERENT" and c["delta"] > 0:
        return "RISES"
    return "STAYS" if c["delta"] < DIFF_MIN and c["new"] <= PANEL_MAX else "UNCLEAR"


def gemini_arm(c: Dict[str, Any], below: bool) -> str:
    if not below:
        return "NOT_TESTABLE"
    if c["label"] == "DIFFERENT" and c["delta"] < 0:
        return "FALLS"
    return "HOLDS" if c["new_ci"][0] > PANEL_MAX else "UNCLEAR"


def overall(sonnet: str, gemini: str) -> str:
    if sonnet == "RISES":
        return "REASONING_MATTERS"
    if sonnet == "STAYS" and gemini == "HOLDS":
        return "GEMINI_ITSELF"
    return "GEMINI_SPECIFIC" if sonnet == "STAYS" and gemini == "FALLS" else "UNCLEAR"


def study(rows: Dict[str, List[Dict[str, Any]]], valid: Dict[str, bool], reps: int = 2000,
          seed: int = 20262401) -> Dict[str, Any]:
    """`rows` holds the raw rows of RUNS' four runs under its keys; `valid` says whether the two new runs are VALID."""
    trap = {k: _in_cell(v, TRAP) for k, v in rows.items()}
    first = {k: mean(request1_reasoning(r) for r in v) for k, v in trap.items()}
    per_run = {k: [_success(r) for r in v] for k, v in trap.items()}
    son = contrast(per_run["sonnet_max"], per_run["sonnet_default"], reps, seed)
    gem = contrast(per_run["gemini_low"], per_run["gemini_medium"], reps, seed)
    reaches = first["sonnet_max"] >= REACHES_GEMINI * first["gemini_medium"]
    below = first["gemini_low"] <= BELOW_GEMINI * first["gemini_medium"]
    arms = {"sonnet": sonnet_arm(son, reaches), "gemini": gemini_arm(gem, below)}
    neutral = contrast([_success(r) for r in _in_cell(rows["gemini_low"], NEUTRAL)],
                       [_success(r) for r in _in_cell(rows["gemini_medium"], NEUTRAL)], reps, seed)
    return {"verdict": overall(**arms) if all(valid.values()) else "INVALID", "arms": arms, "valid": valid,
            "sonnet": son, "gemini": gem, "gemini_neutral": neutral, "reasoning_request_1": first,
            "manipulation": {"sonnet_reaches_half_of_gemini": reaches, "gemini_low_at_most_three_quarters": below},
            "message_effect": {"gemini_low": gem["new"] - neutral["new"], "gemini_medium": gem["base"] - neutral["base"]},
            "cells": {k: cell_details(v, TRAP) for k, v in rows.items()},
            "neutral_cells": {k: cell_details(rows[k], NEUTRAL) for k in ("gemini_low", "gemini_medium")}}


def report(r: Dict[str, Any]) -> str:
    def row(name, key):
        c, x = r[key], r["cells"]
        return (f"| {name} | {c['base']:.3f} | {c['new']:.3f} [{c['new_ci'][0]:.3f}, {c['new_ci'][1]:.3f}] | {c['delta']:+.3f} "
                f"[{c['delta_ci'][0]:+.3f}, {c['delta_ci'][1]:+.3f}] | {c['label']} | {r['arms'][key]} |")

    lines = [f"# C4 study G1: {r['verdict']}", "",
             "Is Gemini 3.8 Flash's give-up result about reasoning or about the model? Each new run is compared with the "
             "W2-E run of the same model, on the same seeds (`PROTOCOL_G1.md`).", "",
             "| Arm, give-up trap solved | Default (W2-E) | New setting | New − default | N1 label | Arm's result |",
             "|---|---|---|---|---|---|", row("Sonnet: effort max", "sonnet"), row("Gemini: reasoning low", "gemini"), "",
             "| Run | Reasoning on the trap's request 1: mean | Third call on request 1 | Solved after a solved request |",
             "|---|---|---|---|"]
    for key, name in (("sonnet_default", "Sonnet, default"), ("sonnet_max", "Sonnet, max"),
                      ("gemini_medium", "Gemini, medium (default)"), ("gemini_low", "Gemini, low")):
        c = r["cells"][key]
        lines.append(f"| {name} | {r['reasoning_request_1'][key]:.0f} | {c['third_call_on_request_1']} of {c['runs']} | "
                     f"{c['solved_after_a_solved_request'][0]} of {c['solved_after_a_solved_request'][1]} |")
    n, m = r["gemini_neutral"], r["message_effect"]
    lines += ["", f"- Reasoning moved as intended: Sonnet reached half of Gemini's mean: "
              f"{r['manipulation']['sonnet_reaches_half_of_gemini']}; Gemini at low at most three quarters of its default: "
              f"{r['manipulation']['gemini_low_at_most_three_quarters']}.",
              f"- Gemini under \"request rejected\": {n['base']:.3f} at its default, {n['new']:.3f} at low "
              f"({n['delta']:+.3f} [{n['delta_ci'][0]:+.3f}, {n['delta_ci'][1]:+.3f}], {n['label']}).",
              f"- The message's effect on Gemini (trap minus \"request rejected\"): {m['gemini_medium']:+.3f} at its default, "
              f"{m['gemini_low']:+.3f} at low."]
    return "\n".join(lines) + "\n"


def write_g1(runs_root: Path, out_dir: Path, reps: int = 2000) -> Dict[str, Any]:
    def load(name: str) -> List[Dict[str, Any]]:
        text = (runs_root / name / "results.jsonl").read_text(encoding="utf-8")
        return sorted((json.loads(x) for x in text.splitlines() if x.strip()), key=lambda r: (r["run_id"], r.get("attempt", 1)))

    def is_valid(name: str) -> bool:
        s = json.loads((runs_root / name / "analysis" / "summary.json").read_text(encoding="utf-8"))
        return s["verdict"]["verdict"] == "VALID"

    r = study({k: load(v) for k, v in RUNS.items()},
              {k: is_valid(RUNS[k]) for k in ("sonnet_max", "gemini_low")}, reps=reps)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "g1.json").write_text(json.dumps(r, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    (out_dir / "G1.md").write_text(report(r), encoding="utf-8", newline="\n")
    return r
