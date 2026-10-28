"""CLI: python3 -m causetest {plan,pilot,run,analyze,combine,validate,power,reproduce,compare,panel} ... (run from this experiment's folder)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from causetest.runner import (EXPERIMENT_DIR, analyze, combine, load_config, pilot, plan, power, reproduce, run,
                              validate)


def main() -> None:
    p = argparse.ArgumentParser(prog="causetest", description="C4 stated cause vs true cause kill test")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan").add_argument("--config", required=True)
    for name in ("pilot", "run"):
        sp = sub.add_parser(name)
        sp.add_argument("--config", required=True)
        sp.add_argument("--live", action="store_true", help="required for a real model")
    sub.add_parser("analyze").add_argument("--run-dir", required=True)
    sc = sub.add_parser("combine")
    sc.add_argument("--run-dirs", nargs="+", required=True)
    sc.add_argument("--out", required=True)
    sv = sub.add_parser("validate")
    sv.add_argument("--configs", nargs="+", required=True)
    sv.add_argument("--out", default=str(EXPERIMENT_DIR / "runs" / "validation"))
    sr = sub.add_parser("reproduce", help="check raw data hashes and re-score every live run against its reports")
    sr.add_argument("--write-manifest", action="store_true", help="pin the current raw files (owner's step)")
    sk = sub.add_parser("compare", help="study N1: A minus B for the same design, with fixed verdicts")
    sk.add_argument("--a", required=True)
    sk.add_argument("--b", required=True)
    sk.add_argument("--design", choices=["C4", "E5"], required=True)
    sk.add_argument("--out", required=True)
    sk.add_argument("--title", default="Comparison")
    sq = sub.add_parser("panel", help="every model and setting side by side (descriptive)")
    sq.add_argument("--out", default=str(EXPERIMENT_DIR / "runs" / "panel"))
    sp = sub.add_parser("power")
    sp.add_argument("--config", required=True)
    sp.add_argument("--replications", type=int, default=20)
    sp.add_argument("--runs-per-cell", type=int, default=None)
    sp.add_argument("--out", default=str(EXPERIMENT_DIR / "runs" / "validation" / "power.json"))
    a = p.parse_args()
    if a.cmd == "plan":
        print(json.dumps(plan(load_config(Path(a.config))), indent=2))
    elif a.cmd == "pilot":
        cfg = load_config(Path(a.config))
        print(json.dumps(pilot(cfg, EXPERIMENT_DIR / "runs" / cfg["run_name"], live=a.live), indent=2))
    elif a.cmd == "run":
        cfg = load_config(Path(a.config))
        s = run(cfg, EXPERIMENT_DIR / "runs" / cfg["run_name"], live=a.live)
        print(json.dumps({"verdict": s["verdict"], "validity": s["validity"], "cost": s["cost"]}, indent=2))
    elif a.cmd == "analyze":
        s = analyze(Path(a.run_dir))
        print(json.dumps({"verdict": s["verdict"], "validity": s["validity"]}, indent=2))
    elif a.cmd == "combine":
        print(json.dumps(combine([Path(d) for d in a.run_dirs], Path(a.out)), indent=2))
    elif a.cmd == "compare":
        from causetest.compare import compare, write_comparison
        r = compare(Path(a.a), Path(a.b), a.design)
        write_comparison(r, Path(a.out), a.title)
        print(json.dumps({"overall": r["overall"], "primary": {k: m["verdict"] for k, m in r["measures"].items()
                                                                if m["primary"]}}, indent=2))
    elif a.cmd == "panel":
        from causetest.panel import write_panel
        r = write_panel(EXPERIMENT_DIR / "runs", Path(a.out))
        print(json.dumps(r["counts"], indent=2))
    elif a.cmd == "reproduce":
        r = reproduce(EXPERIMENT_DIR / "runs", write_manifest=a.write_manifest)
        print(json.dumps(r, indent=2))
        raise SystemExit(0 if r["passed"] else 1)
    elif a.cmd == "validate":
        r = validate([Path(c) for c in a.configs], Path(a.out))
        print(json.dumps({"passed": r["passed"], "runs": {x["run_name"]: x["passed"] for x in r["report"]}}, indent=2))
    else:
        cfg = load_config(Path(a.config))
        if a.runs_per_cell:
            cfg["runs_per_cell"] = a.runs_per_cell
        print(json.dumps(power(cfg, a.replications, Path(a.out)), indent=2))


if __name__ == "__main__":
    main()
