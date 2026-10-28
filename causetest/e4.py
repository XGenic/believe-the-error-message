"""Extension E4: mixed accurate and misleading errors. See PROTOCOL_E4.md.

E3 found that a caution with a stopping rule rescues the give-up trap at the floor cost. But every E3 run
saw one message type, and real error messages are mostly accurate. In E4 each 12-request run mixes
request types; the stated cause and the true fault change per request:

  true_unavailable  "unavailable" over a permanent fault (accurate)
  give_up_trap      "unavailable" over a transient fault (misleading)
  true_temporary    "temporary" over a transient fault (accurate)
  retry_trap        "temporary" over a fixable fault (misleading)
  true_format       the format claim over a fixable fault (accurate)

Two mixes hold each message type's count fixed and vary only how often it is false: in `rare`, one of the
four "unavailable" and one of the four "temporary" messages is false (2 of 12 requests); in `common`, two of
each are (4 of 12). The schedule depends only on the seed and the mix, so both arms see identical runs.

Arms: control and caution_bounded (E3's "…after a few different attempts, accept it").
"""

from __future__ import annotations

import random
from statistics import mean
from typing import Any, Dict, List, Optional, Tuple

from causetest.e2 import _boot, validity_reasons
from causetest.env import ToolEnv, World
from causetest.score import _m

ARMS = ("control", "caution_bounded")
KIND_OF = {("permanent", "permanent"): "true_unavailable", ("permanent", "transient"): "give_up_trap",
           ("transient", "transient"): "true_temporary", ("transient", "fixable"): "retry_trap",
           ("format", "fixable"): "true_format"}
CELL_OF = {k: c for c, k in KIND_OF.items()}
KINDS = tuple(KIND_OF.values())
MIXES = {
    "rare": {"true_unavailable": 3, "give_up_trap": 1, "true_temporary": 3, "retry_trap": 1, "true_format": 4},
    "common": {"true_unavailable": 2, "give_up_trap": 2, "true_temporary": 2, "retry_trap": 2, "true_format": 4},
}
FOLLOW = {"unavailable": ("permanent", "STOP"), "temporary": ("transient", "RETRY")}  # message: (claim, implied)


def schedule_for(seed: int, mix: str, n_tasks: int = 12) -> List[Tuple[str, str]]:
    """The (claim, fault) of each request: the mix's counts in an order drawn from the seed alone."""
    counts = MIXES[mix]
    if sum(counts.values()) != n_tasks:
        raise ValueError(f"mix {mix} has {sum(counts.values())} requests, not {n_tasks}")
    order = [CELL_OF[k] for k, n in counts.items() for _ in range(n)]
    random.Random(f"e4|{seed}|{mix}").shuffle(order)
    return order


def valid_cell(arm: str, mix: str) -> bool:
    return arm in ARMS and mix in MIXES


class MixedToolEnv:
    """A ToolEnv whose stated cause and true fault are set at the start of each request."""

    def __init__(self, world: World, schedule: List[Tuple[str, str]]):
        self.world, self.schedule, self.env = world, schedule, None

    def start_task(self, index: int) -> Dict[str, str]:
        claim, fault = self.schedule[index]
        self.env = ToolEnv(self.world, claim, fault)
        return {"claim": claim, "fault": fault, "kind": KIND_OF[(claim, fault)]}

    def call(self, calls_before: int, args: Dict[str, Any]):
        return self.env.call(calls_before, args)


# ---------------------------------------------------------------- measures

def run_stats(row: Dict[str, Any]) -> Dict[str, Any]:
    """Per run: success and calls by request kind and overall, and the share of first responses that
    follow each message's implied strategy, by half of the run."""
    out: Dict[str, Any] = {}
    tasks = row["tasks"]
    for kind in KINDS:
        ts = [t["summary"] for t in tasks if t.get("kind") == kind]
        out[kind] = (mean(float(x["success"]) for x in ts), mean(x["calls"] for x in ts)) if ts else None
    out["all"] = (mean(float(t["summary"]["success"]) for t in tasks), mean(t["summary"]["calls"] for t in tasks))
    half = len(tasks) // 2
    for msg, (claim, implied) in FOLLOW.items():
        for part, ts in (("early", tasks[:half]), ("late", tasks[half:]), ("all", tasks)):
            codes = [t["summary"]["first_response"] for t in ts if t.get("claim") == claim]
            codes = [c for c in codes if c not in (None, "UNCLASSIFIABLE")]
            out[f"follow_{msg}_{part}"] = (sum(c == implied for c in codes) / len(codes)) if codes else None
    return out


def contrasts_e4(stats: Dict[Tuple[str, str, str], List[Dict[str, Any]]]) -> Dict[str, Optional[float]]:
    def m(arm, mix, key, i=None):
        v = [r[key] if i is None else (r[key][i] if r[key] is not None else None)
             for r in stats.get((arm, "mixed", mix), [])]
        v = [x for x in v if x is not None]
        return mean(v) if v else None

    def diff(a, b):
        return None if a is None or b is None else a - b

    out: Dict[str, Optional[float]] = {}
    for mix in MIXES:
        if ("caution_bounded", "mixed", mix) not in stats or ("control", "mixed", mix) not in stats:
            continue
        d = lambda key, i: diff(m("caution_bounded", mix, key, i), m("control", mix, key, i))
        out[f"{mix}|give_up_rescue"] = d("give_up_trap", 0)
        out[f"{mix}|retry_trap"] = d("retry_trap", 0)
        out[f"{mix}|true_unavailable_calls"] = d("true_unavailable", 1)
        out[f"{mix}|true_temporary_success"] = d("true_temporary", 0)
        out[f"{mix}|true_format_success"] = d("true_format", 0)
        out[f"{mix}|all_success"] = d("all", 0)
        out[f"{mix}|all_calls"] = d("all", 1)
        s, c = out[f"{mix}|all_success"], out[f"{mix}|all_calls"]
        out[f"{mix}|calls_per_extra_success"] = c / s if s is not None and c is not None and s > 0.01 else None
    for arm in ARMS:  # adaptation: does a higher share of false messages change how often the agent follows them?
        for msg in FOLLOW:
            key = f"follow_{msg}_all"
            out[f"adapt|{arm}|{msg}"] = diff(m(arm, "common", key), m(arm, "rare", key))
            for mix in MIXES:
                out[f"drift|{arm}|{mix}|{msg}"] = diff(m(arm, mix, f"follow_{msg}_late"),
                                                       m(arm, mix, f"follow_{msg}_early"))
    return out


def mix_verdict(mix: str, est, ci, th) -> str:
    """Decision rule for the bounded caution in one mix (PROTOCOL_E4.md)."""
    r, c = est.get(f"{mix}|give_up_rescue"), est.get(f"{mix}|true_unavailable_calls")
    r_ci, c_ci = ci.get(f"{mix}|give_up_rescue", (None, None)), ci.get(f"{mix}|true_unavailable_calls", (None, None))
    if r is None or c is None or r_ci[0] is None or c_ci[1] is None:
        return "NOT_ESTIMABLE"
    if not (r >= th["e4_rescue_min"] and r_ci[0] > th["e4_rescue_ci_lo"]):
        return "FADES"
    if c <= th["e4_cost_max"] and c_ci[1] < th["e4_cost_ci_hi"]:
        return "HOLDS"
    return "RESCUE_ONLY"


def harm_flags(mix: str, est, ci, th) -> List[str]:
    flags = []
    for kind in ("true_temporary", "true_format"):
        k = f"{mix}|{kind}_success"
        x, (lo, hi) = est.get(k), ci.get(k, (None, None))
        if x is not None and hi is not None and x <= th["e4_harm_drop"] and hi < th["e4_harm_ci_hi"]:
            flags.append(f"success on {kind.replace('_', ' ')} requests fell by {-x:.2f}")
    return flags


def summarize_e4(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    from causetest.runner import cells_for
    th, n_runs = cfg["thresholds"], cfg["runs_per_cell"]
    cells = cells_for(cfg)
    complete = [r for r in rows if r["status"] == "complete"]
    by_rows = {c: [r for r in complete if (r.get("arm"), r["claim"], r["fault"]) == c] for c in cells}
    stats = {c: [run_stats(r) for r in rs] for c, rs in by_rows.items() if rs}
    est = contrasts_e4(stats)
    ci = _boot(stats, cfg["bootstrap_reps"], cfg["bootstrap_seed"], contrasts_e4)
    verdicts = {mix: mix_verdict(mix, est, ci, th) for mix in MIXES if f"{mix}|give_up_rescue" in est}
    harms = {mix: harm_flags(mix, est, ci, th) for mix in verdicts}
    by_kind = {}
    for c, rs in by_rows.items():
        st = stats.get(c, [])
        by_kind["|".join((c[0], c[2]))] = {
            kind: {"success": _m([r[kind][0] for r in st if r[kind]]), "calls": _m([r[kind][1] for r in st if r[kind]])}
            for kind in KINDS + ("all",)}
        by_kind["|".join((c[0], c[2]))]["runs"] = len(rs)
    turns = sum(t["summary"]["agent_turns"] for r in complete for t in r["tasks"])
    bad = sum(t["summary"]["format_errors"] + t["summary"]["over_budget"] for r in complete for t in r["tasks"])
    first = [t["summary"]["first_response"] for r in complete for t in r["tasks"] if t["summary"]["first_response"]]
    engagement = [_m([float(r["tasks"][0]["summary"]["calls"] > 0) for r in rs]) for rs in by_rows.values() if rs]
    validity = {
        "completion_min": min(len(rs) / n_runs for rs in by_rows.values()),
        "completion": {"|".join(c): len(rs) / n_runs for c, rs in by_rows.items()},
        "protocol_failure_share": bad / turns if turns else None,
        "engagement_min": min(engagement) if engagement else None,
        "unclassifiable_share": (sum(x == "UNCLASSIFIABLE" for x in first) / len(first)) if first else None,
    }
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "E4",
         "n_tasks": int(cfg["n_tasks"]), "runs_per_cell": n_runs, "estimates": est,
         "ci": {k: list(v) for k, v in ci.items()}, "contrast_verdicts": verdicts, "cost_flags": harms,
         "by_kind": by_kind, "validity": validity}
    invalid = validity_reasons(validity, th)
    if not verdicts or "NOT_ESTIMABLE" in verdicts.values():
        invalid.append("some mix could not be estimated")
    s["verdict"] = ({"verdict": "INVALID", "reasons": invalid} if invalid else
                    {"verdict": "VALID", "reasons": [f"{k}: {v}" for k, v in verdicts.items()]})
    return s


# ---------------------------------------------------------------- report

def _f(x, signed=True) -> str:
    if x is None:
        return "n/a"
    return (f"{x:+.3f}" if signed else f"{x:.2f}") if isinstance(x, float) else str(x)


def verdict_markdown_e4(s: Dict[str, Any]) -> str:
    v, est = s["verdict"], s["estimates"]

    def cell(k):
        lo, hi = s["ci"].get(k, (None, None))
        return "n/a" if est.get(k) is None else f"{_f(est[k])} [{_f(lo)}, {_f(hi)}]"

    lines = [f"# C4 extension E4 verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; {s['n_tasks']} mixed requests per "
             f"run, {s['runs_per_cell']} runs per cell.", ""]
    if v["verdict"] == "INVALID":
        lines += [f"- {r}" for r in v["reasons"]] + [""]
    lines += ["## Primary: the bounded caution against control, per mix", "",
              "| Mix | Verdict | Give-up rescue | Extra calls, true 'unavailable' | Harm flags |", "|---|---|---|---|---|"]
    for mix in MIXES:
        if mix in s["contrast_verdicts"]:
            flags = "; ".join(s["cost_flags"].get(mix, [])) or "none"
            lines.append(f"| {mix} | **{s['contrast_verdicts'][mix]}** | {cell(mix + '|give_up_rescue')} | "
                         f"{cell(mix + '|true_unavailable_calls')} | {flags} |")
    lines += ["", "## Net effect over all requests, and the accurate request types", "",
              "| Mix | Δ success, all | Δ calls, all | Extra calls per extra success | Δ success, true 'temporary' | "
              "Δ success, true 'format' | Δ success, retry trap |", "|---|---|---|---|---|---|---|"]
    for mix in MIXES:
        if mix in s["contrast_verdicts"]:
            lines.append(f"| {mix} | {cell(mix + '|all_success')} | {cell(mix + '|all_calls')} | "
                         f"{cell(mix + '|calls_per_extra_success')} | {cell(mix + '|true_temporary_success')} | "
                         f"{cell(mix + '|true_format_success')} | {cell(mix + '|retry_trap')} |")
    lines += ["", "## Secondary: does the share of false messages change how often the agent follows them?", "",
              "Follow rate of each message's implied strategy at the first failure (stop after 'unavailable', identical "
              "retry after 'temporary'). The first failure looks the same whether the message is true or false.", "",
              "| Arm | Message | Common minus rare | Late minus early, rare | Late minus early, common |",
              "|---|---|---|---|---|"]
    for arm in ARMS:
        for msg in FOLLOW:
            lines.append(f"| {arm} | {msg} | {cell(f'adapt|{arm}|{msg}')} | {cell(f'drift|{arm}|rare|{msg}')} | "
                         f"{cell(f'drift|{arm}|common|{msg}')} |")
    lines += ["", "## By request kind (success / calls per request)", "",
              "| Arm, mix | Runs | " + " | ".join(KINDS) + " | all |", "|---|---|" + "---|" * (len(KINDS) + 1)]
    for key, d in s["by_kind"].items():
        cols = [f"{_f(d[k]['success'], False)} / {_f(d[k]['calls'], False)}" for k in KINDS + ("all",)]
        lines.append(f"| {key.replace('|', ', ')} | {d['runs']} | " + " | ".join(cols) + " |")
    val = s["validity"]
    lines += ["", "## Validity", "", f"- completion (min over cells) {val['completion_min']:.3f}; protocol failures "
              f"{val['protocol_failure_share']}; tool use on request 1 (min) {val['engagement_min']}; "
              f"unclassifiable {val['unclassifiable_share']}",
              f"- run statuses: {s.get('status_counts')}", f"- cost: {s.get('cost')}", ""]
    return "\n".join(lines)
