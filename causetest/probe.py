"""Cost probes: what a model's token use in a small pilot implies for the full design (C4, E5 and W6). Not evidence.

A probe runs only the three accurate cells, on development seeds, so it says nothing about either trap. This report
reads token use, cost and transport health, and shows no answers, success rates or next actions. The number of calls
a model would make in the full design is unknown until it runs, so the projection brackets it with the volumes
measured on two earlier subjects: Haiku (gives up early) and GPT-6.1 Sol (persists). Input per call comes from the
probe itself, because replayed reasoning can multiply it; the earlier subjects give only how much longer each design's
conversations ran than the same accurate-cell sample.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any, Dict, List

ACCURATE = {("format", "fixable"), ("transient", "transient"), ("permanent", "permanent")}
SAMPLE_SEEDS = 3  # a probe's seeds per cell, used to take the same sample from a finished C4 run
# Measured call volumes and conversation lengths per design, read from these runs' results.
VOLUMES = {"Haiku": {"C4": "w2c-c4-claude-haiku-5-5-t0", "E5": "w2c-e5-claude-haiku-5-5-t0",
                     "W6": "w2c-w6-claude-haiku-5-5-t0"},
           "Sol": {"C4": "w2d-c4-gpt-6-1-sol-low", "E5": "w2d-e5-gpt-6-1-sol-low", "W6": "w2d-w6-gpt-6-1-sol-low"}}


def tokens(usage: Dict[str, Any]) -> Dict[str, int]:
    """One call's tokens under any of the three APIs: all input, its cached and written parts, output, reasoning."""
    if "prompt_tokens" in usage:  # OpenRouter (Chat Completions)
        detail = usage.get("prompt_tokens_details") or {}
        return {"input": usage["prompt_tokens"], "cached": detail.get("cached_tokens") or 0,
                "written": detail.get("cache_write_tokens") or 0, "output": usage.get("completion_tokens", 0),
                "reasoning": (usage.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0}
    cached, written = usage.get("cache_read_input_tokens") or 0, usage.get("cache_creation_input_tokens") or 0
    detail = usage.get("output_tokens_details") or {}
    return {"input": usage.get("input_tokens", 0) + cached + written, "cached": cached, "written": written,
            "output": usage.get("output_tokens", 0),
            "reasoning": detail.get("thinking_tokens") or detail.get("reasoning_tokens") or 0}


def _rows(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _input_per_call(rows: List[Dict[str, Any]]) -> Dict[str, float]:
    used = [tokens(t["meta"].get("usage") or {})["input"] for r in rows if r["status"] == "complete"
            for task in r["tasks"] for t in task["turns"]]
    return {"calls": len(used), "per_call": sum(used) / len(used)}


def volumes_of(runs_root: Path, runs: Dict[str, str]) -> Dict[str, Dict[str, float]]:
    """Each design's calls, and its input per call relative to a probe-sized accurate-cell sample of the C4 run."""
    c4 = _rows(runs_root / runs["C4"] / "results.jsonl")
    seeds = sorted({r["seed"] for r in c4})[:SAMPLE_SEEDS]
    sample = _input_per_call([r for r in c4 if (r["claim"], r["fault"]) in ACCURATE and r["seed"] in seeds])
    out = {}
    for design, run in runs.items():
        v = _input_per_call(_rows(runs_root / run / "results.jsonl"))
        out[design] = {"calls": v["calls"], "length": v["per_call"] / sample["per_call"]}
    return out


def measure(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Token use, cost and transport health of one probe. Reads nothing about what the agent did with an error."""
    turns = [t for r in rows if r["status"] == "complete" for task in r["tasks"] for t in task["turns"]]
    used = [tokens(t["meta"].get("usage") or {}) for t in turns]
    stops = [t["meta"].get("stop_reason") or t["meta"].get("finish_reason") for t in turns]
    latency = sorted(t["meta"].get("latency_seconds", 0.0) for t in turns)
    n = len(turns)
    if not n:
        return {"runs": len(rows), "complete": 0, "calls": 0}
    total = {k: sum(u[k] for u in used) for k in ("input", "cached", "written", "output", "reasoning")}
    reasoning = sorted(u["reasoning"] for u in used)
    return {"runs": len(rows), "complete": sum(r["status"] == "complete" for r in rows), "calls": n,
            "usd": sum(t["meta"].get("cost_usd", 0.0) for t in turns), **total,
            "calls_per_run": n / sum(r["status"] == "complete" for r in rows),
            "cached_share": total["cached"] / total["input"] if total["input"] else 0.0,
            "written_share": total["written"] / total["input"] if total["input"] else 0.0,
            "output_per_call": total["output"] / n, "reasoning_per_call": total["reasoning"] / n,
            "reasoning_median": statistics.median(reasoning), "reasoning_p90": reasoning[int(0.9 * n)],
            "reasoning_max": reasoning[-1], "share_with_reasoning": sum(x > 0 for x in reasoning) / n,
            "refused": stops.count("refusal"), "cut_off": stops.count("max_tokens") + stops.count("length"),
            "latency_median": statistics.median(latency), "latency_p95": latency[int(0.95 * n)]}


def project(m: Dict[str, Any], output_price: float, volumes: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """Each design's cost: the reference's calls at the probe's input per call (scaled by the design's conversation
    length), effective input price and output per call. Caching is priced as in the probe."""
    per_input = max(0.0, m["usd"] - m["output"] * output_price / 1e6) / m["input"]
    per_call = m["input"] / m["calls"]
    out = {d: v["calls"] * (per_call * v["length"] * per_input + m["output_per_call"] * output_price / 1e6)
           for d, v in volumes.items()}
    return dict(out, total=sum(out.values()))


def report(cfgs: List[Dict[str, Any]], runs_root: Path) -> str:
    volumes = {name: volumes_of(runs_root, runs) for name, runs in VOLUMES.items()}
    lines = ["# Cost probes", "",
             "Accurate cells only, on development seeds: not evidence, and in no verdict or panel. Token use, cost and "
             "transport health only. Misleading cells may use more tokens per call than these, so the projections are "
             "planning figures, and the study's own pilot and cap still apply. Spend is every billed call; the other "
             "columns and the projections use complete runs only, so a probe stopped by its cap is understated.", "",
             "| Probe | Runs | Calls | Spend | Input/call | Cached | Written | Output/call | Reasoning/call: mean, "
             "median, p90, max | Calls with reasoning | Refused | Cut off | Latency: median, p95 |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    projections = ["", "## Projected cost of the full design, per setting", "",
                   "| Probe | Volume like | C4 | E5 | W6 | Total |", "|---|---|---|---|---|---|"]
    for cfg in cfgs:
        path = runs_root / cfg["run_name"] / "pilot" / "results.jsonl"
        if not path.exists():
            lines.append(f"| {cfg['run_name']} | not run | | | | | | | | | | | |")
            continue
        m = measure(_rows(path))
        spent = sum(e.get("cost_usd", 0.0) for e in _rows(path.parent / "journal.jsonl") if e.get("event") == "response")
        if not m["calls"]:
            lines.append(f"| {cfg['run_name']} | {m['complete']} of {m['runs']} complete | 0 | | | | | | | | | | |")
            continue
        lines.append(
            f"| {cfg['run_name']} | {m['complete']} of {m['runs']} | {m['calls']} | ${spent:.2f} | "
            f"{m['input'] / m['calls']:.0f} | {m['cached_share']:.0%} | {m['written_share']:.0%} | "
            f"{m['output_per_call']:.0f} | {m['reasoning_per_call']:.0f}, {m['reasoning_median']:.0f}, "
            f"{m['reasoning_p90']}, {m['reasoning_max']} | {m['share_with_reasoning']:.0%} | {m['refused']} | "
            f"{m['cut_off']} | {m['latency_median']:.1f} s, {m['latency_p95']:.1f} s |")
        for name, v in volumes.items():
            p = project(m, cfg["prices_usd_per_mtok"]["output"], v)
            projections.append(f"| {cfg['run_name']} | {name} | ${p['C4']:.2f} | ${p['E5']:.2f} | ${p['W6']:.2f} | "
                               f"${p['total']:.2f} |")
    return "\n".join(lines + projections) + "\n"


def write_probe(cfgs: List[Dict[str, Any]], runs_root: Path, out_dir: Path) -> str:
    text = report(cfgs, runs_root)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "PROBE.md").write_text(text, encoding="utf-8", newline="\n")
    return text
