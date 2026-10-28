"""One agent run: a single continuous conversation through the six stock requests of one cell."""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional

from causetest.env import Task, ToolEnv, World
from causetest.protocol import (FORMAT_REMINDER, MAX_CALLS_PER_TASK, MAX_FORMAT_ERRORS_PER_TASK, NO_CALLS_LEFT,
                                cause_language, classify_response, normalize_answer, parse_reply, result_message,
                                spelling_of)

MAX_TURNS_PER_TASK = MAX_CALLS_PER_TASK + MAX_FORMAT_ERRORS_PER_TASK + 4


def _responses(world: World, task: Task, turns: List[Dict[str, Any]]) -> List[str]:
    """The coded response after each failed call, in order."""
    out = []
    for i, t in enumerate(turns):
        tool = t.get("tool")
        if not tool or tool["ok"]:
            continue
        nxt = next((u["action"] for u in turns[i + 1:] if u["action"]["kind"] in ("call", "answer")), None)
        out.append(classify_response(world, task, tool["args"], nxt))
    return out


def _summarize(world: World, task: Task, turns: List[Dict[str, Any]], ended_by: str,
               answer: Optional[str]) -> Dict[str, Any]:
    calls = [t["tool"] for t in turns if "tool" in t]
    first_ok = next((i for i, x in enumerate(calls) if x["ok"]), None)
    norm = normalize_answer(answer) if answer is not None else None
    responses = _responses(world, task, turns)
    langs = [cause_language(t["reply"]) for t in turns]
    return {
        "calls": len(calls), "failures": sum(not x["ok"] for x in calls), "success": first_ok is not None,
        "failures_before_success": first_ok if first_ok is not None else len(calls),
        "responses": responses, "first_response": responses[0] if responses else None,
        "first_call_spelling": spelling_of(task.sku, calls[0]["args"].get("sku")) if calls else None,
        "format_errors": sum(t["action"]["kind"] == "invalid" for t in turns),
        "over_budget": sum(t.get("over_budget", False) for t in turns),
        "extra_protocol_lines": sum(t["action"].get("extra_protocol_lines", 0) for t in turns),
        "fabricated_result_lines": sum(t["action"].get("fabricated_result_lines", 0) for t in turns),
        "agent_turns": len(turns), "ended_by": ended_by, "answer": answer, "answer_norm": norm,
        "correct": norm == task.truth, "unknown": norm == "unknown",
        "unsupported": norm not in (None, "unknown") and first_ok is None,
        "self_cause_language": any(x["self"] for x in langs),
        "service_cause_language": any(x["service"] for x in langs),
    }


def run_episode(conv, world: World, env: ToolEnv, out: List[Dict[str, Any]],
                before_call: Callable[[], float], after_call: Callable[[float, Dict[str, Any]], None],
                log: Callable[[Dict[str, Any]], None]) -> List[Dict[str, Any]]:
    """Drive the conversation through the world's requests, appending one record per request to `out`.

    A transport error or a spend-cap stop propagates to the caller after the current request's record
    is closed, so the caller keeps everything up to that point."""
    for task in world.tasks:
        msg, turns = task.text, []
        calls = fmt_errors = over = 0
        ended_by, answer = "turn_limit", None
        rec = {"index": task.index, "text": task.text, "truth": task.truth, "depot": task.depot, "turns": turns}
        if hasattr(env, "start_task"):  # extension E4: the stated cause and the true fault change per request
            rec.update(env.start_task(task.index))
        out.append(rec)
        while len(turns) < MAX_TURNS_PER_TASK:
            try:
                reserved = before_call()
            except Exception:
                rec["summary"] = _summarize(world, task, turns, "stopped", None)
                raise
            log({"event": "request", "task": task.index, "turn": len(turns), "time": time.time()})
            try:
                reply, meta = conv.say(msg)
            except Exception as exc:
                after_call(reserved, getattr(exc, "meta", {}))  # a billed failure still counts against the cap
                rec["summary"] = _summarize(world, task, turns, "transport_error", None)
                raise
            after_call(reserved, meta)
            action = parse_reply(reply)
            turn: Dict[str, Any] = {"user": msg, "reply": reply, "action": action, "meta": meta}
            turns.append(turn)
            if action["kind"] == "answer":
                ended_by, answer = "answer", action["value"]
                break
            if action["kind"] == "invalid":
                fmt_errors += 1
                if fmt_errors > MAX_FORMAT_ERRORS_PER_TASK:
                    ended_by = "protocol_failure"
                    break
                msg = FORMAT_REMINDER
                continue
            if calls >= MAX_CALLS_PER_TASK:
                over += 1
                turn["over_budget"] = True
                if over > 1:
                    ended_by = "protocol_failure"
                    break
                msg = NO_CALLS_LEFT
                continue
            ok, text, info = env.call(calls, action["args"])
            turn["tool"] = {"args": action["args"], "ok": ok, "result": text, "info": info}
            calls += 1
            msg = result_message(text)
        rec["summary"] = _summarize(world, task, turns, ended_by, answer)
    return out
