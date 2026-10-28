"""The panel table (paper plan W2, analysis): every model and setting run so far, one row each, with the headline
effects side by side and how many arms show each. Descriptive only: it re-reads each run's committed summary and
adds no new verdicts.

Columns, all from the runs' own analyses:
  S and its interval, with the C4 verdict;
  success in the retry trap ("temporary" over a fixable fault) and the give-up trap ("unavailable" over a
    transient fault), with a Wilson 95% interval that counts each run once (n = runs per cell). Requests within a
    run are not independent, so this is conservative, and unlike the bootstrap it is never zero-width at 0 or 1
    (paper plan W6: the E1 degeneracy);
  E5's D1 (stopping at once after no earlier error minus after a cleared one) and E5's verdict;
  the give-up rescue of the bounded caution ("a few different attempts"; E3 or W2-B) and of "three attempts in a
    row" (E3 or W6), with their verdicts.
"""

from __future__ import annotations

import json
from math import sqrt
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

RETRY_TRAP, GIVE_UP_TRAP = "transient|fixable", "permanent|transient"

# (model, setting, {measure source: run folder}). "bounded" and "three" name the run holding that arm.
ARMS: List[Tuple[str, str, Dict[str, str]]] = [
    ("Claude Haiku 5.5", "text, no reasoning", {"c4": "live-claude-haiku-5-5"}),
    ("Claude Haiku 5.5", "native, thinking off", {"c4": "w2c-c4-claude-haiku-5-5-t0", "e5": "w2c-e5-claude-haiku-5-5-t0",
                                                  "bounded": "w2c-w6-claude-haiku-5-5-t0",
                                                  "three": "w2c-w6-claude-haiku-5-5-t0"}),
    ("Claude Haiku 5.5", "native, thinking on", {"c4": "w2c-c4-claude-haiku-5-5-t1", "e5": "w2c-e5-claude-haiku-5-5-t1",
                                                 "bounded": "w2c-w6-claude-haiku-5-5-t1",
                                                 "three": "w2c-w6-claude-haiku-5-5-t1"}),
    ("GPT-6-luna", "text, low", {"c4": "live-gpt-6-luna", "e5": "e5-live-gpt-6-luna",
                                 "bounded": "e3-live-gpt-6-luna", "three": "e3-live-gpt-6-luna"}),
    ("GPT-6-luna", "native, none", {"c4": "n1-c4-native-none-gpt-6-luna", "e5": "w5-e5-none-gpt-6-luna"}),
    ("GPT-6-luna", "native, low", {"c4": "n1-c4-native-low-gpt-6-luna", "e5": "n1-e5-native-low-gpt-6-luna",
                                   "bounded": "w6-gpt6luna-native-low", "three": "w6-gpt6luna-native-low"}),
    ("GPT-6-luna", "native, medium", {"c4": "w5-c4-medium-gpt-6-luna", "e5": "w5-e5-medium-gpt-6-luna"}),
    ("GPT-6-luna", "native, high", {"c4": "w5-c4-high-gpt-6-luna", "e5": "w5-e5-high-gpt-6-luna"}),
    ("DeepSeek V4.1 Flash", "native, r0", {"c4": "or-c4-deepseek-v4-1-flash-r0", "e5": "or-e5-deepseek-v4-1-flash-r0",
                                           "bounded": "w2b-deepseek-v4-1-flash-r0", "three": "w6-deepseek-v4-1-flash-r0"}),
    ("DeepSeek V4.1 Flash", "native, r1", {"c4": "or-c4-deepseek-v4-1-flash-r1", "e5": "or-e5-deepseek-v4-1-flash-r1",
                                           "bounded": "w2b-deepseek-v4-1-flash-r1", "three": "w6-deepseek-v4-1-flash-r1"}),
    ("Qwen3.8-27B", "native, r0", {"c4": "or-c4-qwen3-8-27b-r0", "e5": "or-e5-qwen3-8-27b-r0",
                                   "bounded": "w2b-qwen3-8-27b-r0", "three": "w6-qwen3-8-27b-r0"}),
    ("Qwen3.8-27B", "native, r1", {"c4": "or-c4-qwen3-8-27b-r1", "e5": "or-e5-qwen3-8-27b-r1",
                                   "bounded": "w2b-qwen3-8-27b-r1"}),
    ("gpt-oss-120b", "native, r1", {"c4": "or-c4-gpt-oss-120b-r1-crusoe", "e5": "or-e5-gpt-oss-120b-r1",
                                    "bounded": "w2b-gpt-oss-120b-r1", "three": "w6-gpt-oss-120b-r1"}),
]


def wilson(p: float, n: int, z: float = 1.959964) -> Tuple[float, float]:
    """Wilson score interval for a proportion p observed over n units."""
    if n <= 0:
        raise ValueError("n must be positive")
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def _summary(runs: Path, name: Optional[str]) -> Optional[Dict[str, Any]]:
    p = runs / name / "analysis" / "summary.json" if name else None
    return json.loads(p.read_text(encoding="utf-8")) if p and p.exists() else None


def _verdict(s: Dict[str, Any]) -> str:
    v = s["verdict"]
    return v if isinstance(v, str) else v["verdict"]


def _rescue(s: Optional[Dict[str, Any]], arm: str) -> Optional[Dict[str, Any]]:
    if s is None or f"{arm}|give_up_rescue" not in s.get("estimates", {}):
        return None
    return {"est": s["estimates"][f"{arm}|give_up_rescue"], "ci": s["ci"][f"{arm}|give_up_rescue"],
            "verdict": f"{s.get('design', 'E3')}: {s['contrast_verdicts'][arm]}"}  # W6's and E3's rules differ


def panel_rows(runs: Path) -> List[Dict[str, Any]]:
    rows = []
    for model, setting, src in ARMS:
        row: Dict[str, Any] = {"model": model, "setting": setting, "sources": src}
        c4 = _summary(runs, src.get("c4"))
        if c4 is not None:
            n = c4["runs_per_cell"]
            row["c4"] = {"verdict": _verdict(c4), "S": c4["S"], "S_ci": c4["S_ci"], "runs_per_cell": n}
            for key, cell in (("retry_trap", RETRY_TRAP), ("give_up_trap", GIVE_UP_TRAP)):
                by_request = c4["cells"][cell]["success_by_request"]  # each request has every run of the cell
                p = sum(by_request) / len(by_request)
                row["c4"][key] = {"est": p, "wilson": wilson(p, n)}
        e5 = _summary(runs, src.get("e5"))
        if e5 is not None:
            verdict = "INVALID" if _verdict(e5) == "INVALID" else e5["contrast_verdicts"]["primary"]
            row["e5"] = {"verdict": verdict, "D1": e5["estimates"]["none_minus_cleared|stop"],
                         "D1_ci": e5["ci"]["none_minus_cleared|stop"]}
        row["bounded"] = _rescue(_summary(runs, src.get("bounded")), "caution_bounded")
        row["three"] = _rescue(_summary(runs, src.get("three")), "caution_three")
        rows.append(row)
    return rows


def counts(rows: List[Dict[str, Any]], bar: float = 0.10, rescue_min: float = 0.5,
           rescue_ci_lo: float = 0.3) -> Dict[str, Tuple[int, int]]:
    """How many arms show each effect, out of the arms with that measure. `bar` is the trap-success level counted
    as "the trap holds"; the rescue bar is E3's (estimate at least 0.50 and lower bound above 0.30)."""
    c4 = [r["c4"] for r in rows if "c4" in r]
    e5 = [r["e5"] for r in rows if "e5" in r and r["e5"]["verdict"] != "INVALID"]

    def rescued(x):
        return x["est"] >= rescue_min and x["ci"][0] > rescue_ci_lo

    out = {
        "credulous (C4 verdict CONTINUE_CREDULOUS)": (sum(x["verdict"] == "CONTINUE_CREDULOUS" for x in c4), len(c4)),
        f"retry trap holds (success at most {bar:.0%})": (sum(x["retry_trap"]["est"] <= bar for x in c4), len(c4)),
        f"give-up trap holds (success at most {bar:.0%})": (sum(x["give_up_trap"]["est"] <= bar for x in c4), len(c4)),
        "first-encounter effect (E5 CONFIRMED; INVALID runs left out)": (sum(x["verdict"] == "CONFIRMED" for x in e5), len(e5)),
    }
    for key, label in (("bounded", "\"a few different attempts\""), ("three", "\"three attempts in a row\"")):
        xs = [r[key] for r in rows if r.get(key)]
        out[f"{label} rescues the give-up trap (E3's bar)"] = (sum(rescued(x) for x in xs), len(xs))
    return out


def _f(x: float) -> str:
    return f"{x:+.2f}"


def _iv(ci) -> str:
    return f"[{_f(ci[0])}, {_f(ci[1])}]"


def write_panel(runs: Path, out: Path) -> Dict[str, Any]:
    rows = panel_rows(runs)
    tally = counts(rows)
    out.mkdir(parents=True, exist_ok=True)
    result = {"rows": rows, "counts": {k: list(v) for k, v in tally.items()}}
    (out / "panel.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    lines = ["# C4 panel: every model and setting, side by side (descriptive)", "",
             "Generated by `python -m causetest panel` from each run's committed summary. No new verdicts.", "",
             "- **S:** steering, with its bootstrap interval and the C4 verdict.",
             "- **Traps:** share of requests solved; Wilson 95% interval counting each run once (n = runs per cell), "
             "so it is conservative and never zero-width.",
             "- **E5 D1:** stopping at once after no earlier error, minus after a cleared one; E5's primary verdict.",
             "- **Rescues:** give-up-trap success, the caution arm minus control, with the verdict of the study it comes from (E3's rule for E3 and W2-B, W6's for W6).", "",
             "| Model | Setting | S (C4 verdict) | Retry trap | Give-up trap | E5 D1 (verdict) | \"A few different\" rescue | "
             "\"Three in a row\" rescue |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        c4, e5 = r.get("c4"), r.get("e5")
        cells = [r["model"], r["setting"]]
        if c4:
            cells += [f"{_f(c4['S'])} {_iv(c4['S_ci'])} ({c4['verdict']})"]
            cells += [f"{c4[k]['est']:.2f} [{c4[k]['wilson'][0]:.2f}, {c4[k]['wilson'][1]:.2f}]"
                      for k in ("retry_trap", "give_up_trap")]
        else:
            cells += ["—"] * 3
        cells.append(f"{_f(e5['D1'])} {_iv(e5['D1_ci'])} ({e5['verdict']})" if e5 else "—")
        for key in ("bounded", "three"):
            x = r.get(key)
            cells.append(f"{_f(x['est'])} {_iv(x['ci'])} ({x['verdict']})" if x else "—")
        lines.append("| " + " | ".join(cells) + " |")
    lines += ["", "## How many arms show each effect", "", "| Effect | Arms |", "|---|---|"]
    lines += [f"| {k} | {a} of {n} |" for k, (a, n) in tally.items()]
    lines += ["", "Sources (run folders under `runs/`):", ""]
    lines += [f"- {r['model']}, {r['setting']}: " + ", ".join(f"{k} `{v}`" for k, v in r["sources"].items()) for r in rows]
    (out / "PANEL.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return result
