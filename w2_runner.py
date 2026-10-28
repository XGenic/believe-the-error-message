"""Study W2-A launcher (PROTOCOL_W2.md). Loads OPENROUTER_API_KEY from this folder's .env or .env.txt (never printed),
then runs one step. Every call goes through the gated runner, so each config's cap and --live rules still apply.

    python w2_runner.py credits                      # remaining OpenRouter credit (no model call)
    python w2_runner.py probe [arm ...]              # one request per arm, logged in runs/w2-probes/
    python w2_runner.py pilot <config.json>          # development pilot
    python w2_runner.py main <config.json> ...       # main runs in order, each after the credit check below

Budget rule (PROTOCOL_W2.md): a main run starts only if 1.5x its pilot-based estimate fits the remaining credit less $1.
"""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

C4 = Path(__file__).resolve().parent
os.chdir(C4)
sys.path.insert(0, str(C4))

for name in (".env", ".env.txt"):
    f = C4 / name
    if f.exists():
        for line in f.read_text(encoding="utf-8-sig").splitlines():
            k, _, v = line.partition("=")
            if k.strip() and not k.strip().startswith("#"):
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
if not os.environ.get("OPENROUTER_API_KEY"):
    sys.exit("OPENROUTER_API_KEY not found in the environment, .env or .env.txt; nothing sent")

ARMS = ["deepseek_v4_1_flash_r0", "deepseek_v4_1_flash_r1", "qwen3_8_27b_r0", "qwen3_8_27b_r1",
        "gemma_4_31b_r0", "gemma_4_31b_r1"]


def credits():
    req = urllib.request.Request("https://openrouter.ai/api/v1/credits",
                                 headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]})
    d = json.load(urllib.request.urlopen(req, timeout=30))["data"]
    return d["total_credits"] - d["total_usage"], d


def probe(arms):
    from causetest.env import CLAIM_TEXT, make_world
    from causetest.protocol import system_prompt
    from causetest.runner import load_config, make_transport
    out = C4 / "runs" / "w2-probes"
    out.mkdir(parents=True, exist_ok=True)
    world = make_world(20269201)  # the C4 development seed; never analyzed
    system = system_prompt(world, native=True)
    for arm in arms or ARMS:
        cfg = load_config(C4 / "configs" / f"live_or_c4_{arm}.json")
        conv = make_transport(cfg, out, live=True).open(arm, system)
        rec = {"arm": arm, "model": cfg["model"], "pin": cfg["provider"], "expected_host": cfg["expected_host"],
               "request_options": cfg["request_options"], "time": time.time(), "turns": []}
        msg = world.tasks[0].text
        for _ in range(2):
            try:
                reply, meta = conv.say(msg)
            except Exception as exc:
                rec["turns"].append({"user": msg, "error": str(exc)[-600:], "meta": getattr(exc, "meta", None)})
                break
            rec["turns"].append({"user": msg, "reply": reply, "meta": meta})
            if not reply.startswith("CALL "):
                break
            msg = f"RESULT stock_lookup: ERROR: {CLAIM_TEXT['neutral']}"
        with (out / "probe.jsonl").open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
        for turn in rec["turns"]:
            m = turn.get("meta") or {}
            print(arm, "|", (turn.get("reply") or turn.get("error", ""))[:110].replace("\n", " "), "| host", m.get("host"),
                  "cost", m.get("cost_usd"), "retries", m.get("rate_limit_retries"), m.get("timeout_retries"))


def main_runs(configs):
    from causetest.runner import EXPERIMENT_DIR, load_config, run
    for name in configs:
        cfg = load_config(C4 / "configs" / name)
        d = EXPERIMENT_DIR / "runs" / cfg["run_name"]
        est = json.loads((d / "pilot" / "pilot.json").read_text(encoding="utf-8"))["kill_test_estimate_equiv_usd"]
        left, _ = credits()
        if 1.5 * est > left - 1.0:
            print(json.dumps({"config": name, "skipped": "credit", "estimate": est, "credit_left": left}), flush=True)
            continue
        s = run(cfg, d, live=True)
        print(json.dumps({"config": name, "estimate": est, "credit_before": round(left, 4), "verdict": s["verdict"],
                          "validity": s["validity"], "cost": s["cost"]}), flush=True)


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "credits":
        print(json.dumps(credits()))
    elif cmd == "probe":
        probe(args)
    elif cmd == "pilot":
        from causetest.runner import EXPERIMENT_DIR, load_config, pilot
        cfg = load_config(C4 / "configs" / args[0])
        print(json.dumps(pilot(cfg, EXPERIMENT_DIR / "runs" / cfg["run_name"], live=True)))
    elif cmd == "main":
        main_runs(args)
    else:
        sys.exit(__doc__)
