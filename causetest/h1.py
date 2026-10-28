"""Study H1: does tool withdrawal carry over to a tool that works? See PROTOCOL_H1.md.

In W2-A, gpt-oss-120b increasingly answered without calling the tool at all: by request 6, a third of its C4
runs. That could be adaptation (not calling a tool that keeps failing) or helplessness: the habit carrying over
once the tool works again, as in C3's triadic design. Each H1 run has 12 requests: a training block of 8, set
by the condition, then a test block of 4 in which every call works.

  no_failure                  training: no fault (every resolvable call works)
  controllable                training: the format message over a fixable fault (the agent can fix it)
  uncontrollable              training: the same format message over a permanent fault (nothing works)
  uncontrollable_temporary    training: "temporary service problem" over a permanent fault

Controllable and uncontrollable show the agent the same message; only whether its actions can succeed differs.
Primary measure: the share of test-block requests answered without any tool call (withdrawal).
"""

from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List, Optional, Tuple

from causetest.e2 import _boot, validity_reasons
from causetest.e5 import _NoFault
from causetest.env import ToolEnv, World
from causetest.score import _m

ARMS = ("control",)
N_TRAIN, N_TEST = 8, 4
TRAINING = {"no_failure": ("neutral", "none"), "controllable": ("format", "fixable"),
            "uncontrollable": ("format", "permanent"), "uncontrollable_temporary": ("transient", "permanent")}
TEST = ("neutral", "none")


def schedule_for(condition: str, n_tasks: int = N_TRAIN + N_TEST) -> List[Tuple[str, str]]:
    if n_tasks != N_TRAIN + N_TEST:
        raise ValueError(f"H1 runs have exactly {N_TRAIN + N_TEST} requests")
    return [TRAINING[condition]] * N_TRAIN + [TEST] * N_TEST


def valid_cell(arm: str, condition: str) -> bool:
    return arm in ARMS and condition in TRAINING


class ScheduledToolEnv:
    """The stated cause and true fault of each request, set at its start; fault "none" means every resolvable
    call works (an unresolvable one gets the neutral error)."""

    def __init__(self, world: World, schedule: List[Tuple[str, str]]):
        self.world, self.schedule, self.env = world, schedule, None

    def start_task(self, index: int) -> Dict[str, str]:
        claim, fault = self.schedule[index]
        self.env = _NoFault(self.world) if fault == "none" else ToolEnv(self.world, claim, fault)
        return {"claim": claim, "fault": fault, "kind": "train" if index < N_TRAIN else "test"}

    def call(self, calls_before: int, args: Dict[str, Any]):
        return self.env.call(calls_before, args)


# ---------------------------------------------------------------- measures

def run_stats(row: Dict[str, Any]) -> Dict[str, Any]:
    train = [t["summary"] for t in row["tasks"][:N_TRAIN]]
    test = [t["summary"] for t in row["tasks"][N_TRAIN:]]
    return {
        "test_no_call": mean(float(s["calls"] == 0) for s in test),
        "test_success": mean(float(s["success"]) for s in test),
        "train_no_call": mean(float(s["calls"] == 0) for s in train),
        "train_late_no_call": mean(float(s["calls"] == 0) for s in train[-3:]),
        "train_success": mean(float(s["success"]) for s in train),
        "train_failed_calls": sum(s["failures"] for s in train),
        "no_call_by_request": [float(t["summary"]["calls"] == 0) for t in row["tasks"]],
    }


def contrasts_h1(stats) -> Dict[str, Optional[float]]:
    def m(cond, key):
        v = [r[key] for r in stats.get(("control", "helpless", cond), [])]
        return mean(v) if v else None

    def diff(a, b):
        return None if a is None or b is None else a - b

    out: Dict[str, Optional[float]] = {}
    for key in ("test_no_call", "test_success", "train_late_no_call"):
        out[f"uncontrollable_minus_no_failure|{key}"] = diff(m("uncontrollable", key), m("no_failure", key))
        out[f"uncontrollable_minus_controllable|{key}"] = diff(m("uncontrollable", key), m("controllable", key))
        out[f"temporary_minus_uncontrollable|{key}"] = diff(m("uncontrollable_temporary", key), m("uncontrollable", key))
    return out


def _rule(x, ci, th, yes: str, no: str) -> str:
    lo, hi = ci
    if x is None or lo is None:
        return "NOT_ESTIMABLE"
    if x >= th["h1_effect_min"] and lo > th["h1_effect_ci_lo"]:
        return yes
    if abs(x) < th["h1_none_abs"] and -th["h1_none_ci"] < lo and hi < th["h1_none_ci"]:
        return no
    return "INCONCLUSIVE"


def verdicts_h1(est, ci, per_cond, th) -> Dict[str, str]:
    k1, k2 = "uncontrollable_minus_no_failure|test_no_call", "uncontrollable_minus_controllable|test_no_call"
    primary = _rule(est.get(k1), ci.get(k1, (None, None)), th, "CARRYOVER", "NO_CARRYOVER")
    controllable_ok = (per_cond.get("controllable", {}).get("train_success") or 0) >= th["h1_min_controllable_success"]
    if primary != "CARRYOVER":
        secondary = "NOT_APPLICABLE"
    elif not controllable_ok:
        secondary = "NOT_APPLICABLE_CONTROLLABLE_FAILED"
    else:
        secondary = _rule(est.get(k2), ci.get(k2, (None, None)), th, "CONTROLLABILITY_MATTERS", "FAILURE_GENERAL")
    return {"primary": primary, "secondary": secondary}


def summarize_h1(rows: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
    from causetest.runner import cells_for
    th, n_runs = cfg["thresholds"], cfg["runs_per_cell"]
    cells = cells_for(cfg)
    complete = [r for r in rows if r["status"] == "complete"]
    by_rows = {c: [r for r in complete if (r.get("arm"), r["claim"], r["fault"]) == c] for c in cells}
    stats = {c: [run_stats(r) for r in rs] for c, rs in by_rows.items() if rs}
    est = contrasts_h1(stats)
    ci = _boot(stats, cfg["bootstrap_reps"], cfg["bootstrap_seed"], contrasts_h1)
    per_cond = {}
    for c in cells:
        st = stats.get(c, [])
        d = {k: _m([r[k] for r in st]) for k in ("test_no_call", "test_success", "train_no_call", "train_late_no_call",
                                                  "train_success", "train_failed_calls")}
        d["no_call_by_request"] = [_m([r["no_call_by_request"][i] for r in st]) for i in range(N_TRAIN + N_TEST)]
        d["runs"] = len(by_rows[c])
        per_cond[c[2]] = d
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
    verdicts = verdicts_h1(est, ci, per_cond, th)
    s = {"label": cfg.get("label", ""), "model": cfg["model"], "transport": cfg["transport"], "design": "H1",
         "n_tasks": N_TRAIN + N_TEST, "runs_per_cell": n_runs, "estimates": est,
         "ci": {k: list(v) for k, v in ci.items()}, "contrast_verdicts": verdicts, "per_condition": per_cond,
         "validity": validity}
    invalid = validity_reasons(validity, th)
    if verdicts["primary"] == "NOT_ESTIMABLE":
        invalid.append("the primary contrast could not be estimated")
    s["verdict"] = ({"verdict": "INVALID", "reasons": invalid} if invalid else
                    {"verdict": verdicts["primary"], "reasons": [f"secondary: {verdicts['secondary']}"]})
    return s


def _f(x, signed=True) -> str:
    if x is None:
        return "n/a"
    return (f"{x:+.3f}" if signed else f"{x:.2f}") if isinstance(x, float) else str(x)


def verdict_markdown_h1(s: Dict[str, Any]) -> str:
    v, est = s["verdict"], s["estimates"]

    def cell(k):
        lo, hi = s["ci"].get(k, (None, None))
        return "n/a" if est.get(k) is None else f"{_f(est[k])} [{_f(lo)}, {_f(hi)}]"

    lines = [f"# C4 study H1 verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; {N_TRAIN} training + {N_TEST} test "
             f"requests per run, {s['runs_per_cell']} runs per condition.", ""] + [f"- {r}" for r in v["reasons"]]
    lines += ["", "## Per condition (test block: every call works)", "",
              "| Training condition | Runs | Training success | Failed calls in training | No-call, last 3 training | "
              "**No-call, test block** | Test success |", "|---|---|---|---|---|---|---|"]
    for cond, d in s["per_condition"].items():
        lines.append(f"| {cond} | {d['runs']} | {_f(d['train_success'], False)} | {_f(d['train_failed_calls'], False)} | "
                     f"{_f(d['train_late_no_call'], False)} | **{_f(d['test_no_call'], False)}** | "
                     f"{_f(d['test_success'], False)} |")
    lines += ["", "## No-call share by request (1–8 training, 9–12 test)", ""]
    for cond, d in s["per_condition"].items():
        lines.append(f"- {cond}: " + " ".join(_f(x, False) for x in d["no_call_by_request"]))
    lines += ["", "## Contrasts", "", "| Contrast | No-call, test | Test success | No-call, last 3 training |",
              "|---|---|---|---|"]
    for name, label in (("uncontrollable_minus_no_failure", "**primary:** uncontrollable minus no failure"),
                        ("uncontrollable_minus_controllable", "**secondary:** uncontrollable minus controllable"),
                        ("temporary_minus_uncontrollable", "message: 'temporary' minus format, both uncontrollable")):
        lines.append(f"| {label} | " + " | ".join(cell(f"{name}|{k}") for k in
                                                ("test_no_call", "test_success", "train_late_no_call")) + " |")
    val = s["validity"]
    lines += ["", f"- primary verdict: **{s['contrast_verdicts']['primary']}**; secondary: "
              f"**{s['contrast_verdicts']['secondary']}**", "", "## Validity", "",
              f"- completion (min) {val['completion_min']:.3f}; protocol failures {val['protocol_failure_share']}; "
              f"tool use on request 1 (min) {val['engagement_min']}; unclassifiable {val['unclassifiable_share']}",
              f"- run statuses: {s.get('status_counts')}", f"- cost: {s.get('cost')}", ""]
    return "\n".join(lines)
