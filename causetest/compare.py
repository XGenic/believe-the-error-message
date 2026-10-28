"""Comparing two runs of the same design (paper plan W1, study N1; see PROTOCOL_N1.md).

N1 asks whether results change when the agent calls the tool natively instead of writing CALL lines, and,
secondarily, with reasoning off. For each measure the difference A minus B gets a 95% percentile bootstrap
interval (runs resampled within each cell of each run independently) and a fixed verdict:

  SAME       |Δ| < 0.15 and the interval lies within (−0.25, +0.25)
  DIFFERENT  |Δ| ≥ 0.15 and the interval excludes 0
  UNCLEAR    otherwise

Measures. C4 grid: S, L*, success in the retry trap and in the give-up trap (primary), and success in every
cell (secondary). E5: the primary contrast D1 (primary), and each prime's stop-at-once rate (secondary).
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from statistics import mean
from typing import Any, Callable, Dict, List, Optional, Tuple

from causetest.score import first_responses, steering_and_learning

SAME_MAX, SAME_CI, DIFF_MIN = 0.15, 0.25, 0.15
RETRY_TRAP, GIVE_UP_TRAP = ("transient", "fixable"), ("permanent", "transient")


def _rows(run_dir: Path) -> List[Dict[str, Any]]:
    path = run_dir / "results.jsonl"
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = [r for r in rows if r["status"] == "complete"]
    return sorted(rows, key=lambda r: (r["run_id"], r.get("attempt", 1)))


def _success(row: Dict[str, Any]) -> float:
    return mean(float(t["summary"]["success"]) for t in row["tasks"])


def _c4_units(rows) -> Dict[Tuple[str, str], List[Tuple[List[Optional[str]], float]]]:
    out: Dict[Tuple[str, str], List] = {}
    for r in rows:
        out.setdefault((r["claim"], r["fault"]), []).append((first_responses(r), _success(r)))
    return out


def c4_measures(units) -> Dict[str, Optional[float]]:
    sl = steering_and_learning({c: [u[0] for u in us] for c, us in units.items()})
    out = {"S": sl["S"], "L_star": sl["L_star"]}
    for c, us in sorted(units.items()):
        out[f"success|{c[0]}|{c[1]}"] = mean(u[1] for u in us) if us else None
    out["retry_trap_success"] = out.get(f"success|{RETRY_TRAP[0]}|{RETRY_TRAP[1]}")
    out["give_up_trap_success"] = out.get(f"success|{GIVE_UP_TRAP[0]}|{GIVE_UP_TRAP[1]}")
    return out


def _e5_units(rows):
    from causetest.e5 import run_stats
    out: Dict[Tuple[str, str, str], List] = {}
    for r in rows:
        out.setdefault((r.get("arm"), r["claim"], r["fault"]), []).append(run_stats(r))
    return out


def e5_measures(units) -> Dict[str, Optional[float]]:
    from causetest.e5 import contrasts_e5
    c = contrasts_e5(units)
    out = {"D1": c.get("none_minus_cleared|stop")}
    for (_, _, prime), us in sorted(units.items()):
        v = [u["stop"] for u in us if u["stop"] is not None]
        out[f"stop|{prime}"] = mean(v) if v else None
    return out


DESIGNS: Dict[str, Tuple[Callable, Callable, Tuple[str, ...]]] = {
    "C4": (_c4_units, c4_measures, ("S", "retry_trap_success", "give_up_trap_success")),
    "E5": (_e5_units, e5_measures, ("D1",)),
}


def verdict(d: Optional[float], lo: Optional[float], hi: Optional[float]) -> str:
    if d is None or lo is None:
        return "NOT_ESTIMABLE"
    if abs(d) < SAME_MAX and -SAME_CI < lo and hi < SAME_CI:
        return "SAME"
    if abs(d) >= DIFF_MIN and (lo > 0 or hi < 0):
        return "DIFFERENT"
    return "UNCLEAR"


def compare(a_dir: Path, b_dir: Path, design: str, reps: int = 2000, seed: int = 20261801) -> Dict[str, Any]:
    to_units, measures, primary = DESIGNS[design]
    ua, ub = to_units(_rows(a_dir)), to_units(_rows(b_dir))
    ma, mb = measures(ua), measures(ub)
    rng = random.Random(seed)
    draws: Dict[str, List[float]] = {}
    for _ in range(reps):
        ra = measures({k: [rng.choice(v) for _ in v] for k, v in ua.items() if v})
        rb = measures({k: [rng.choice(v) for _ in v] for k, v in ub.items() if v})
        for k in ma:
            if ra.get(k) is not None and rb.get(k) is not None:
                draws.setdefault(k, []).append(ra[k] - rb[k])
    rows = {}
    for k in ma:
        d = None if ma[k] is None or mb.get(k) is None else ma[k] - mb[k]
        xs = sorted(draws.get(k, []))
        lo, hi = (xs[int(0.025 * len(xs))], xs[min(len(xs) - 1, int(0.975 * len(xs)))]) if xs else (None, None)
        rows[k] = {"a": ma[k], "b": mb.get(k), "diff": d, "ci": [lo, hi], "verdict": verdict(d, lo, hi),
                   "primary": k in primary}
    prim = [rows[k]["verdict"] for k in primary]
    overall = ("SAME" if all(v == "SAME" for v in prim) else
               "DIFFERENT" if any(v == "DIFFERENT" for v in prim) else "UNCLEAR")
    return {"design": design, "a": str(a_dir.as_posix()), "b": str(b_dir.as_posix()), "measures": rows,
            "overall": overall, "bootstrap": {"reps": reps, "seed": seed}}


def _f(x) -> str:
    return "n/a" if x is None else f"{x:+.3f}"


def write_comparison(result: Dict[str, Any], out: Path, title: str) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}: {result['overall']}", "", f"- A: `{result['a']}`", f"- B: `{result['b']}`",
             f"- Δ = A − B; 95% percentile bootstrap, {result['bootstrap']['reps']} resamples, seed "
             f"{result['bootstrap']['seed']}. SAME: |Δ| < 0.15 and interval within ±0.25. DIFFERENT: |Δ| ≥ 0.15 and "
             "interval excludes 0.", "", "| Measure | Primary | A | B | Δ [95% interval] | Verdict |", "|---|---|---|---|---|---|"]
    for k, m in sorted(result["measures"].items(), key=lambda kv: (not kv[1]["primary"], kv[0])):
        ci = f"[{_f(m['ci'][0])}, {_f(m['ci'][1])}]"
        lines.append(f"| {k.replace('|', ' / ')} | {'yes' if m['primary'] else ''} | {_f(m['a'])} | {_f(m['b'])} | "
                     f"{_f(m['diff'])} {ci} | {m['verdict']} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    out.with_suffix(".json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8",
                                        newline="\n")
