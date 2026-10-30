"""Plan, pilot, run, analyze, combine, validate and power. See README.md (overview) and NOTEBOOK.md for the tested commands."""

from __future__ import annotations

import hashlib
import json
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from causetest.env import CLAIM_TEXT, N_TASKS, ToolEnv, cells, make_world
from causetest.episode import run_episode
from causetest.protocol import system_prompt
from causetest.score import overall_verdict, pilot_check, summarize
from causetest.transports import (AnthropicNativeTransport, ClaudeCLITransport, MockTransport, OpenAINativeTransport,
                                  OpenAIResponsesTransport, OpenRouterNativeTransport, SpendCapExceeded, SpendGuard)

# Paper plan W1: native function calling
NATIVE_TRANSPORTS = ("openai_responses_native", "openrouter_chat_native", "anthropic_messages_native")

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent


def load_config(path: Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def cells_for(cfg: Dict[str, Any]) -> List[Tuple[str, ...]]:
    """The cells a config runs: all twelve by default, or the subset named in cfg["cells"] ("claim|fault").
    Extensions E2 and E3 and study W6 name (arm, claim, fault) cells as "arm|claim|fault"."""
    if cfg.get("design") in ("E2", "E3", "W6", "R1"):
        from causetest.e2 import valid_cell
        if cfg["design"] == "R1":
            from causetest.r1 import valid_cell
        chosen3 = [tuple(c.split("|")) for c in cfg["cells"]]
        bad = [c for c in chosen3 if len(c) != 3 or not valid_cell(*c)]
        if bad:
            raise ValueError(f"unknown E2 cells {bad}")
        return chosen3
    if cfg.get("design") == "E4":  # "arm|mix"; the claim slot holds "mixed" and the fault slot the mix
        from causetest.e4 import valid_cell as valid_e4
        pairs = [tuple(c.split("|")) for c in cfg["cells"]]
        bad = [c for c in pairs if len(c) != 2 or not valid_e4(*c)]
        if bad:
            raise ValueError(f"unknown E4 cells {bad}")
        return [(arm, "mixed", mix) for arm, mix in pairs]
    if cfg.get("design") == "E5":  # "arm|prime"; the claim slot holds "primed" and the fault slot the prime
        from causetest.e5 import valid_cell as valid_e5
        pairs = [tuple(c.split("|")) for c in cfg["cells"]]
        bad = [c for c in pairs if len(c) != 2 or not valid_e5(*c)]
        if bad:
            raise ValueError(f"unknown E5 cells {bad}")
        return [(arm, "primed", prime) for arm, prime in pairs]
    if cfg.get("design") == "H1":  # "arm|condition"; the claim slot holds "helpless", the fault slot the condition
        from causetest.h1 import valid_cell as valid_h1
        pairs = [tuple(c.split("|")) for c in cfg["cells"]]
        bad = [c for c in pairs if len(c) != 2 or not valid_h1(*c)]
        if bad:
            raise ValueError(f"unknown H1 cells {bad}")
        return [(arm, "helpless", cond) for arm, cond in pairs]
    if not cfg.get("cells"):
        return cells()
    chosen = [tuple(c.split("|")) for c in cfg["cells"]]
    unknown = [c for c in chosen if c not in cells()]
    if unknown:
        raise ValueError(f"unknown cells {unknown}")
    return chosen


def world_seeds(cfg: Dict[str, Any]) -> List[int]:
    """Run r of every cell uses world base_seed + r, so all cells see the same requests."""
    return [cfg["base_seed"] + r for r in range(cfg["runs_per_cell"])]


def make_transport(cfg: Dict[str, Any], run_dir: Path, live: bool):
    kind = cfg["transport"]
    if kind == "mock":
        return MockTransport(cfg["mock"]["kind"], cfg["mock"].get("params", {}))
    if not live:
        raise RuntimeError("Live transport requested without --live; nothing was sent")
    if float(cfg["max_equiv_usd"]) <= 0:
        raise RuntimeError("max_equiv_usd is 0; live calls are not authorized")
    if kind == "claude_cli":
        return ClaudeCLITransport(cfg["model"], run_dir / "subject_cwd", int(cfg.get("cli_timeout_seconds", 240)))
    if kind == "openai_responses":
        return OpenAIResponsesTransport(cfg["model"], cfg.get("request_options", {}), cfg["prices_usd_per_mtok"],
                                        bool(cfg.get("history_cut_after_first_protocol_line", False)))
    if kind == "openai_responses_native":
        return OpenAINativeTransport(cfg["model"], cfg.get("request_options", {}), cfg["prices_usd_per_mtok"])
    if kind == "openrouter_chat_native":
        return OpenRouterNativeTransport(cfg["model"], cfg["provider"], cfg.get("request_options", {}),
                                         cfg["prices_usd_per_mtok"], int(cfg.get("timeout_seconds", 180)),
                                         bool(cfg.get("pass_reasoning_back", False)), cfg.get("expected_host"),
                                         float(cfg.get("deadline_seconds", 60)))
    if kind == "anthropic_messages_native":
        return AnthropicNativeTransport(cfg["model"], cfg.get("request_options", {}), cfg["prices_usd_per_mtok"],
                                        int(cfg.get("timeout_seconds", 120)))
    raise ValueError(f"unknown transport {kind}")


def plan(cfg: Dict[str, Any]) -> Dict[str, Any]:
    est = cfg["planning"]
    runs = len(cells_for(cfg)) * cfg["runs_per_cell"]
    calls = runs * est["calls_per_run"]
    pilot_calls = len(cells_for(cfg)) * est["calls_per_run"]
    return {"cells": len(cells_for(cfg)), "agent_runs": runs, "estimated_calls": calls, "pilot_calls": pilot_calls,
            "estimated_equiv_usd": round((calls + pilot_calls) * est["usd_per_call"], 2),
            "cap_equiv_usd": cfg["max_equiv_usd"], "call_cap": cfg["max_calls"], "note": cfg.get("cost_note", "")}


class _Jsonl:
    def __init__(self, path: Path):
        self.path, self._lock = path, threading.Lock()

    def write(self, row: Dict[str, Any]) -> None:
        with self._lock, self.path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def _journal_spend(paths: List[Path]) -> Tuple[float, int]:
    """Spend and calls from every response ever journaled, failed and stopped runs included."""
    usd, calls = 0.0, 0
    for path in paths:
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                ev = json.loads(line)
                if ev.get("event") == "response":
                    usd, calls = usd + ev.get("cost_usd", 0.0), calls + 1
    return usd, calls


def _guard(cfg: Dict[str, Any], run_dir: Path) -> SpendGuard:
    """One cap covers the pilot and the kill test together, across every invocation."""
    spent, calls = _journal_spend([run_dir / "journal.jsonl", run_dir / "pilot" / "journal.jsonl"])
    return SpendGuard(cfg["max_equiv_usd"], cfg["max_calls"], cfg["worst_case_usd_per_call"], spent_usd=spent,
                      calls=calls)


class _Session:
    """Shared state for one invocation: transport, spend guard, cache and logs."""

    def __init__(self, cfg: Dict[str, Any], out_dir: Path, transport, guard: SpendGuard):
        self.cfg, self.transport, self.guard = cfg, transport, guard
        self.cache = out_dir / "cache"
        self.cache.mkdir(parents=True, exist_ok=True)
        results = out_dir / "results.jsonl"
        if results.exists():
            results.unlink()  # rebuilt from the cache; incomplete runs start again from the beginning
        self.results, self.journal = _Jsonl(results), _Jsonl(out_dir / "journal.jsonl")

    def run_one(self, claim: str, fault: str, seed: int, attempt: int = 1,
                arm: Optional[str] = None) -> Dict[str, Any]:
        """One run. `arm` (extension E2 only) sets the system-prompt notes and the error text."""
        run_id = f"{claim}|{fault}|{seed}" if arm is None else f"{arm}|{claim}|{fault}|{seed}"
        world = make_world(seed, int(self.cfg.get("n_tasks", N_TASKS)))
        schedule = None
        native = self.cfg.get("transport") in NATIVE_TRANSPORTS  # the instructions point to native tool calls
        if arm is None:
            system, error = system_prompt(world, native=native), CLAIM_TEXT[claim]
        elif claim in ("mixed", "primed", "helpless"):  # E4, E5 and H1: the fault slot names the schedule
            from causetest.e2 import system_for
            if claim == "mixed":
                from causetest.e4 import schedule_for
                schedule = schedule_for(seed, fault, len(world.tasks))
            elif claim == "helpless":
                from causetest.h1 import schedule_for as h1_schedule
                schedule = h1_schedule(fault, len(world.tasks))
            else:
                from causetest.e5 import schedule_for as primed_schedule
                schedule = primed_schedule(fault, len(world.tasks))
            system, error = system_for(world, arm, native), json.dumps(schedule)
        else:
            from causetest.e2 import error_text, system_for
            system, error = system_for(world, arm, native), error_text(arm, claim)
            if self.cfg.get("design") == "R1":  # recovery times and the client's retries are part of the run
                from causetest.r1 import attempts_per_call, schedule_for as recovery_schedule
                schedule = recovery_schedule(seed, len(world.tasks))
                error = json.dumps({"error": error, "recovery_failures": schedule, "attempts": attempts_per_call(arm)})
        key_fields = {"run": run_id, "model": self.cfg["model"], "system": system,
                      "tasks": [t.text for t in world.tasks], "error": error}
        if self.cfg.get("history_cut_after_first_protocol_line"):
            key_fields["history_cut"] = True  # only when set, so earlier runs' cache keys are unchanged
        if self.cfg.get("transport") == "openrouter_chat_native":
            key_fields["host"] = self.cfg["provider"]  # a different host is a different subject; never reuse its runs
        key = hashlib.sha256(json.dumps(key_fields).encode()).hexdigest()
        cached = self.cache / f"{key}.json"
        if cached.exists():
            row = json.loads(cached.read_text(encoding="utf-8"))
            row["cached"] = True
            self.results.write(row)
            return row
        conv = self.transport.open(run_id, system)
        out: List[Dict[str, Any]] = []
        row = {"run_id": run_id, "claim": claim, "fault": fault, "seed": seed, "model": self.cfg["model"],
               "transport": self.transport.label, "tasks": out, "cached": False, "status": "complete",
               "attempt": attempt}
        if arm is not None:
            row["arm"] = arm
        mock = self.transport.is_mock

        def before() -> float:
            return 0.0 if mock else self.guard.reserve()

        def after(reserved: float, meta: Dict[str, Any]) -> None:
            if not mock:
                self.guard.settle(reserved, meta.get("cost_usd", 0.0))
                self.journal.write({"event": "response", "run": run_id, "cost_usd": meta.get("cost_usd", 0.0),
                                    "ok": bool(meta), "time": time.time()})

        def log(ev: Dict[str, Any]) -> None:
            if not mock:
                self.journal.write(dict(ev, run=run_id))

        try:
            if self.cfg.get("design") == "R1":
                from causetest.r1 import RecoveryToolEnv, attempts_per_call
                env = RecoveryToolEnv(world, claim, fault, schedule, attempts_per_call(arm))
            elif schedule is not None and claim == "primed":
                from causetest.e5 import PrimedToolEnv
                env = PrimedToolEnv(world, schedule)
            elif schedule is not None and claim == "helpless":
                from causetest.h1 import ScheduledToolEnv
                env = ScheduledToolEnv(world, schedule)
            elif schedule is not None:
                from causetest.e4 import MixedToolEnv
                env = MixedToolEnv(world, schedule)
            else:
                env = ToolEnv(world, claim, fault, None if arm is None else error)
            run_episode(conv, world, env, out, before, after, log)
        except SpendCapExceeded as exc:
            row["status"] = "stopped"
            self.journal.write({"event": "spend_cap_stop", "run": run_id, "detail": str(exc)})
        except Exception as exc:  # preserved, never retried silently
            row["status"] = "failed"
            row["error"] = str(exc)[-500:]
            self.journal.write({"event": "transport_error", "run": run_id, "error": str(exc)[-500:]})
        if row["status"] == "complete":
            cached.write_text(json.dumps(row, sort_keys=True), encoding="utf-8", newline="\n")
        self.results.write(row)
        return row


def _run_all(session: _Session, cfg: Dict[str, Any], seeds: List[int]) -> List[Dict[str, Any]]:
    """Every cell on every seed, then one fresh re-run of each run that failed on a transport error.
    Transport failures do not depend on the agent's behavior; both attempts stay in the records."""
    # A job is (claim, fault, seed, arm); arm is None outside extension E2.
    jobs = [(c[-2], c[-1], s, c[0] if len(c) == 3 else None)
            for s in seeds for c in cells_for(cfg)]  # interleaved so drift cannot line up with a cell
    with ThreadPoolExecutor(max_workers=int(cfg.get("workers", 4))) as pool:
        rows = list(pool.map(lambda j: session.run_one(j[0], j[1], j[2], arm=j[3]), jobs))
        failed = [(r["claim"], r["fault"], r["seed"], r.get("arm")) for r in rows if r["status"] == "failed"]
        if failed and cfg.get("rerun_transport_failures_once", True):
            session.journal.write({"event": "rerun_transport_failures",
                                   "runs": ["|".join(str(x) for x in j if x is not None) for j in failed]})
            rows += list(pool.map(lambda j: session.run_one(j[0], j[1], j[2], attempt=2, arm=j[3]), failed))
    return rows


def size_runs(target_usd: float, pilot_usd: float, per_run_usd: float, n_cells: int, planned: int) -> int:
    """Pre-registered sizing rule (extension E1): the largest runs per cell, up to the planned number,
    whose estimated cost plus the pilot's own cost stays within the target."""
    fit = int((target_usd - pilot_usd) // (n_cells * per_run_usd))
    return max(0, min(planned, fit))


def pilot(cfg: Dict[str, Any], run_dir: Path, live: bool) -> Dict[str, Any]:
    """Pre-registered development pilot: one run per cell on development seeds. It measures the
    per-call cost (to set the cap) and checks the protocol; its data never enter the verdict."""
    transport = make_transport(cfg, run_dir, live)
    out_dir = run_dir / "pilot"
    out_dir.mkdir(parents=True, exist_ok=True)
    session = _Session(cfg, out_dir, transport, _guard(cfg, run_dir))
    rows = _run_all(session, cfg, [cfg["dev_seed"]])
    check = dict(pilot_check(rows), model=cfg["model"], label=cfg.get("label", ""), dev_seed=cfg["dev_seed"])
    n_cells = len(cells_for(cfg))
    per_run = (check["cost_equiv_usd"] / check["complete"]) if check["complete"] else 0.0
    check["kill_test_estimate_equiv_usd"] = round(n_cells * cfg["runs_per_cell"] * per_run, 2)
    if cfg.get("sizing_target_usd") and per_run > 0:
        check["sized_runs_per_cell"] = size_runs(cfg["sizing_target_usd"], check["cost_equiv_usd"], per_run, n_cells,
                                                 cfg["runs_per_cell"])
    (out_dir / "pilot.json").write_text(json.dumps(check, indent=2), encoding="utf-8", newline="\n")
    lines = [f"# C4 development pilot: {cfg['model']}", "",
             f"**{check['label']}**. One run per cell on development seed {cfg['dev_seed']}; not evidence.", ""]
    lines += [f"- {k}: {v}" for k, v in check.items() if k not in ("label", "model", "dev_seed")]
    (out_dir / "PILOT.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return check


def run(cfg: Dict[str, Any], run_dir: Path, live: bool) -> Dict[str, Any]:
    transport = make_transport(cfg, run_dir, live)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config.json").write_text(json.dumps(cfg, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    with (run_dir / "worlds.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for s in world_seeds(cfg):
            f.write(json.dumps(make_world(s, int(cfg.get("n_tasks", N_TASKS))).to_json()) + "\n")
    session = _Session(cfg, run_dir, transport, _guard(cfg, run_dir))
    session.journal.write({"event": "run_start", "transport": transport.label, "model": cfg["model"],
                           "runs_per_cell": cfg["runs_per_cell"], "time": time.time()})
    _run_all(session, cfg, world_seeds(cfg))
    session.journal.write({"event": "run_end", "spent_equiv_usd": session.guard.spent_usd,
                           "calls": session.guard.calls, "time": time.time()})
    return analyze(run_dir)


def analyze(run_dir: Path, out_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Score a run from its raw records. Rows are sorted by run and attempt first, so the result does not
    depend on the order in which threads finished and wrote `results.jsonl` (paper plan W0)."""
    cfg = load_config(run_dir / "config.json")
    path = run_dir / "results.jsonl"
    rows = ([json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if path.exists() else [])
    rows.sort(key=lambda r: (r["run_id"], r.get("attempt", 1)))
    if cfg.get("design") == "E1":
        from causetest.extension import summarize_e1, verdict_markdown_e1
        s = summarize_e1(rows, cfg)
        md = verdict_markdown_e1
    elif cfg.get("design") == "E2":
        from causetest.e2 import summarize_e2, verdict_markdown_e2
        s = summarize_e2(rows, cfg)
        md = verdict_markdown_e2
    elif cfg.get("design") == "E3":
        from causetest.e3 import summarize_e3, verdict_markdown_e3
        s = summarize_e3(rows, cfg)
        md = verdict_markdown_e3
    elif cfg.get("design") == "W6":
        from causetest.w6 import summarize_w6, verdict_markdown_w6
        s = summarize_w6(rows, cfg)
        md = verdict_markdown_w6
    elif cfg.get("design") == "R1":
        from causetest.r1 import summarize_r1, verdict_markdown_r1
        s = summarize_r1(rows, cfg)
        md = verdict_markdown_r1
    elif cfg.get("design") == "E4":
        from causetest.e4 import summarize_e4, verdict_markdown_e4
        s = summarize_e4(rows, cfg)
        md = verdict_markdown_e4
    elif cfg.get("design") == "E5":
        from causetest.e5 import summarize_e5, verdict_markdown_e5
        s = summarize_e5(rows, cfg)
        md = verdict_markdown_e5
    elif cfg.get("design") == "H1":
        from causetest.h1 import summarize_h1, verdict_markdown_h1
        s = summarize_h1(rows, cfg)
        md = verdict_markdown_h1
    else:
        s = summarize(rows, cfg)
        md = verdict_markdown
    s["status_counts"] = dict(Counter(r["status"] for r in rows))
    s["cost"] = {"runs_recorded": len(rows), "from_cache": sum(r.get("cached", False) for r in rows),
                 "agent_calls": sum(len(t["turns"]) for r in rows for t in r["tasks"]),
                 "equiv_usd": round(sum(turn["meta"].get("cost_usd", 0.0) for r in rows for t in r["tasks"]
                                        for turn in t["turns"]), 4)}
    out = out_dir or run_dir / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(s, indent=2, sort_keys=True, default=str), encoding="utf-8", newline="\n")
    (out / "VERDICT.md").write_text(md(s), encoding="utf-8", newline="\n")
    return s


def _f(x) -> str:
    if x is None:
        return "n/a"
    return f"{x:.3f}" if isinstance(x, float) else str(x)


def verdict_markdown(s: Dict[str, Any]) -> str:
    v, val = s["verdict"], s["validity"]
    lines = [f"# C4 kill test verdict: {v['verdict']}", "",
             f"**{s['label']}**: transport `{s['transport']}`, model `{s['model']}`; {s['runs_per_cell']} runs per cell.",
             ""] + [f"- {r}" for r in v["reasons"]]
    lines += ["", "## Steering (request 1): follow rate of the claim's strategy minus the neutral baseline", "",
              "| Misleading cell (claim, true fault) | Δ |", "|---|---|"]
    lines += [f"| {k} | {_f(d)} |" for k, d in s["deltas"].items()]
    lines += ["", f"- **S** = {_f(s['S'])} [{_f(s['S_ci'][0])}, {_f(s['S_ci'][1])}]", "",
              "## Learning: follow rate on requests 1–2 minus requests 5–6", "",
              "| Cell | Kind | L |", "|---|---|---|"]
    lines += [f"| {k} | misleading | {_f(x)} |" for k, x in s["L_misleading"].items()]
    lines += [f"| {k} | accurate | {_f(x)} |" for k, x in s["L_accurate"].items()]
    sp = s["superstition_probe"]
    lines += ["", f"- format|transient is excluded from L\\*: obeying the format claim succeeds there (any third call "
              "does), so outcomes never contradict it."]
    lines += ["", f"- **L\\*** = mean misleading L (five cells) − mean accurate L = {_f(s['L_star'])} "
              f"[{_f(s['L_star_ci'][0])}, {_f(s['L_star_ci'][1])}]", "",
              "## Per cell (secondary)", "",
              "| Cell | Runs | First response, request 1 | First response, requests 5–6 | Success by request | "
              "Calls, requests 5–6 | UNKNOWN | Unsupported |", "|---|---|---|---|---|---|---|---|"]
    for k, c in s["cells"].items():
        succ = " / ".join("n/a" if x is None else f"{x:.2f}" for x in c["success_by_request"])
        lines.append(f"| {k} | {c['runs']} | {c['first_response_request1']} | {c['first_response_late']} | {succ} | "
                     f"{_f(c['calls_late'])} | {_f(c['unknown_rate'])} | {c['unsupported_answers']} |")
    lines += ["", "## H3 (stability → expectancy): calls on requests 5–6, 'unavailable' minus 'temporary' claim", ""]
    lines += [f"- true fault {f}: {_f(h['difference'])} ({_f(h['calls_late_stable_claim'])} vs "
              f"{_f(h['calls_late_unstable_claim'])})" for f, h in s["H3_stability"].items()]
    lines += ["", "## Superstition probe (format claim over a transient fault)", "",
              f"- requests 2–6 whose first call already changes the SKU spelling: format claim {_f(sp['format_claim'])}, "
              f"neutral message {_f(sp['neutral_claim'])}; index {_f(sp['index'])}"]
    h4 = " / ".join("n/a" if x is None else f"{x:.2f}" for x in s["H4_talked_out_of_fixable"])
    lines += ["", f"## H4 (talked out of a fixable fault): success by request in permanent|fixable: {h4}", "",
              "## Validity", "", f"- completion (min over cells) {_f(val['completion_min'])}; protocol failures "
              f"{_f(val['protocol_failure_share'])}; tool use on request 1 (min over cells) {_f(val['engagement_min'])}; "
              f"unclassifiable responses {_f(val['unclassifiable_share'])}",
              f"- run statuses: {s.get('status_counts')}", f"- cost: {s.get('cost')}", ""]
    return "\n".join(lines)


def combine(run_dirs: List[Path], out_dir: Path) -> Dict[str, Any]:
    per_model = {}
    for d in run_dirs:
        s = json.loads((d / "analysis" / "summary.json").read_text(encoding="utf-8"))
        per_model[s["model"]] = s["verdict"]["verdict"]
    result = {"per_model": per_model, "overall": overall_verdict(per_model), "runs": [str(d) for d in run_dirs]}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "overall.json").write_text(json.dumps(result, indent=2), encoding="utf-8", newline="\n")
    lines = [f"# C4 kill test overall verdict: {result['overall']}", ""] + [f"- `{k}`: {v}" for k, v in per_model.items()]
    (out_dir / "OVERALL.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return result


def _in(x: Optional[float], rng: List[float]) -> bool:
    return x is not None and rng[0] <= x <= rng[1]


def validate(config_paths: List[Path], out_dir: Path) -> Dict[str, Any]:
    report = []
    for path in config_paths:
        cfg = load_config(path)
        s = run(cfg, EXPERIMENT_DIR / "runs" / cfg["run_name"], live=False)
        exp, checks = cfg.get("expect", {}), {}
        checks["verdict"] = (s["verdict"]["verdict"], s["verdict"]["verdict"] == exp["verdict"])
        for key in [k for k in exp if k.endswith("_range") and k != "superstition_range"]:
            field = key[:-len("_range")]
            x = s.get(field)
            checks[field] = (None if x is None else round(x, 3), _in(x, exp[key]))
        if "superstition_range" in exp:
            x = s["superstition_probe"]["index"]
            checks["superstition_index"] = (None if x is None else round(x, 3), _in(x, exp["superstition_range"]))
        for k, want in exp.get("contrast_verdicts", {}).items():  # extension E2
            got = s.get("contrast_verdicts", {}).get(k)
            checks[f"verdict {k}"] = (got, got == want)
        for arm, want in exp.get("costly", {}).items():  # extension E2: whether an arm raises a cost flag
            got = bool(s.get("cost_flags", {}).get(arm))
            checks[f"costly {arm}"] = (got, got == want)
        if "invalid_reason_contains" in exp:
            text = " ".join(s["verdict"]["reasons"])
            checks["invalid_reason"] = (exp["invalid_reason_contains"], exp["invalid_reason_contains"] in text)
        report.append({"run_name": cfg["run_name"], "checks": checks, "passed": all(ok for _, ok in checks.values())})
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "validation.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8", newline="\n")
    lines = ["# MOCK instrument validation (not evidence about any model)", ""]
    for r in report:
        lines.append(f"## {r['run_name']}: {'PASS' if r['passed'] else 'FAIL'}")
        lines += [f"- {n}: got {g} -> {'ok' if ok else 'MISMATCH'}" for n, (g, ok) in r["checks"].items()]
        lines.append("")
    (out_dir / "VALIDATION.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return {"passed": all(r["passed"] for r in report), "report": report}


MANIFEST = "MANIFEST.json"


def live_run_dirs(runs_root: Path) -> List[Path]:
    """Every committed live run: a folder with a config whose transport is not the MOCK one."""
    return sorted(d for d in runs_root.iterdir()
                  if (d / "config.json").exists() and load_config(d / "config.json").get("transport") != "mock")


def raw_files(run_dir: Path) -> List[Path]:
    """The raw record of a run: everything except derived analysis and the resume cache."""
    return sorted(p for p in run_dir.rglob("*") if p.is_file()
                  and not {"analysis", "cache"} & set(p.relative_to(run_dir).parts))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reproduce(runs_root: Path, run_dirs: Optional[List[Path]] = None, write_manifest: bool = False) -> Dict[str, Any]:
    """Paper plan W0: check every live run's raw files against the SHA-256 manifest, then re-score each run
    from its raw records into a scratch folder and compare the reports with the committed ones byte for byte."""
    import tempfile
    run_dirs = run_dirs if run_dirs is not None else live_run_dirs(runs_root)
    manifest_path = runs_root / MANIFEST
    hashes = {p.relative_to(runs_root).as_posix(): _sha256(p) for d in run_dirs for p in raw_files(d)}
    if write_manifest:
        manifest_path.write_text(json.dumps(hashes, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    pinned = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    report = {"raw_files": len(hashes), "raw_mismatches": sorted(k for k, h in hashes.items() if pinned.get(k) != h),
              "raw_missing": sorted(k for k in pinned if k not in hashes
                                    and any(k.startswith(d.name + "/") for d in run_dirs)),
              "runs": {}}
    with tempfile.TemporaryDirectory() as tmp:
        for d in run_dirs:
            out = Path(tmp) / d.name
            analyze(d, out)
            same = {name: (d / "analysis" / name).exists()
                    and (d / "analysis" / name).read_bytes() == (out / name).read_bytes()
                    for name in ("summary.json", "VERDICT.md")}
            report["runs"][d.name] = same
    report["passed"] = (not report["raw_mismatches"] and not report["raw_missing"] and bool(pinned)
                        and all(all(v.values()) for v in report["runs"].values()))
    return report


def power(cfg: Dict[str, Any], replications: int, out_path: Path) -> Dict[str, Any]:
    """Operating characteristics of the decision rule for a scripted agent: rerun the whole kill
    test on `replications` disjoint sets of world seeds and count verdicts. MOCK only."""
    if cfg["transport"] != "mock":
        raise RuntimeError("power analysis runs on scripted agents only")
    counts: Counter = Counter()
    per_contrast: Dict[str, Counter] = {}  # extension E2: verdict counts for each trap contrast
    for r in range(replications):
        rcfg = dict(cfg, base_seed=cfg["base_seed"] + 1000 * (r + 1))
        s = run(rcfg, EXPERIMENT_DIR / "runs" / "power-scratch" / f"{cfg['run_name']}-{r}", live=False)
        counts[s["verdict"]["verdict"]] += 1
        for k, v in s.get("contrast_verdicts", {}).items():
            per_contrast.setdefault(k, Counter())[v] += 1
    result = {"run_name": cfg["run_name"], "runs_per_cell": cfg["runs_per_cell"], "replications": replications,
              "verdicts": dict(counts)}
    if per_contrast:
        result["contrast_verdicts"] = {k: dict(v) for k, v in per_contrast.items()}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    existing[f"{cfg['run_name']}@{cfg['runs_per_cell']}"] = result
    out_path.write_text(json.dumps(existing, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    return result
