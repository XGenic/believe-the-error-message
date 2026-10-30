"""Tests for the C4 instrument: worlds, the three true faults, the four error texts, the information
boundary, reply parsing, response coding, episode limits, S and L*, the verdict rule, spend caps and
gating, the pilot, and MOCK runs."""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from causetest.env import (CLAIM_TEXT, CLAIMS, CONFIRMABLE_MISLEADING, FAULTS, SKU_FORMS, TASK_DEPOTS,  # noqa: E402
                           ToolEnv, cell_kind, cells, make_world)
from causetest.episode import run_episode  # noqa: E402
from causetest.protocol import (FORMAT_REMINDER, NO_CALLS_LEFT, classify_response, normalize_answer,  # noqa: E402
                                parse_reply, result_message, system_prompt)
from causetest.runner import cells_for, load_config, make_transport, pilot, run, size_runs  # noqa: E402
from causetest.score import model_verdict, steering_and_learning  # noqa: E402
from causetest.transports import SpendCapExceeded, SpendGuard  # noqa: E402

DIR = Path(__file__).resolve().parent.parent
LIVE = DIR / "configs" / "live_claude_haiku.json"
W = make_world(20261201)
T = W.tasks[0]


def _args(task=T, form="given", site=None):
    sku = task.sku.lower() if form == "given" else SKU_FORMS[form](task.sku)
    return {"site": site or task.depot, "sku": sku}


class TestWorldAndFaults(unittest.TestCase):
    def test_world(self):
        self.assertEqual(len(W.tasks), 6)
        self.assertEqual(make_world(20261201).to_json(), W.to_json())
        for seed in range(20261201, 20261231):
            w = make_world(seed)
            depots = [t.depot for t in w.tasks]
            self.assertEqual(sorted(depots.count(d) for d in set(depots)), [2] * TASK_DEPOTS)
            self.assertEqual(len({w.conventions[d] for d in set(depots)}), 3, "three depots, three conventions")
            self.assertEqual(len({t.sku for t in w.tasks}), 6)
            for t in w.tasks:
                self.assertEqual(t.truth, str(w.stock[(t.depot, t.sku)]))
                self.assertIn(f"SKU {t.sku.lower()}", t.text)

    def test_fixable(self):
        env = ToolEnv(W, "neutral", "fixable")
        conv = W.conventions[T.depot]
        self.assertFalse(env.call(0, _args())[0], "the spelling in the request never works")
        for form in SKU_FORMS:
            self.assertEqual(env.call(0, _args(form=form))[0], form == conv, form)

    def test_transient_and_permanent(self):
        conv = W.conventions[T.depot]
        tr = ToolEnv(W, "neutral", "transient")
        self.assertFalse(tr.call(0, _args(form=conv))[0])
        self.assertFalse(tr.call(1, _args(form=conv))[0])
        self.assertTrue(tr.call(2, _args())[0], "any resolvable third call works")
        self.assertFalse(tr.call(2, {"site": "Nowhere", "sku": T.sku})[0])
        pm = ToolEnv(W, "neutral", "permanent")
        self.assertFalse(any(pm.call(k, _args(form=f))[0] for k in range(6) for f in SKU_FORMS))

    def test_every_failure_shows_the_cell_text(self):
        for claim, fault in cells():
            ok, text, _ = ToolEnv(W, claim, fault).call(0, _args())
            self.assertFalse(ok)
            self.assertEqual(text, CLAIM_TEXT[claim], (claim, fault))

    def test_cells(self):
        kinds = [cell_kind(c, f) for c, f in cells()]
        self.assertEqual((len(kinds), kinds.count("accurate"), kinds.count("misleading"), kinds.count("neutral")),
                         (12, 3, 6, 3))
        self.assertEqual(cell_kind(*CONFIRMABLE_MISLEADING), "misleading")


class TestAgentFacingText(unittest.TestCase):
    def test_messages_state_a_cause_and_give_no_instruction(self):
        for text in CLAIM_TEXT.values():
            words = set(re.findall(r"[a-z]+", text.lower()))
            for w in ("try", "retry", "again", "please", "check", "stop", "should", "use"):
                self.assertNotIn(w, words, (text, w))

    def test_agent_sees_no_design_information(self):
        texts = [system_prompt(W), FORMAT_REMINDER, NO_CALLS_LEFT] + [t.text for t in W.tasks]
        texts += [result_message(CLAIM_TEXT[c]) for c in CLAIMS]
        words = set(re.findall(r"[a-z]+", " ".join(texts).lower()))
        for leaked in ("claim", "fault", "cell", "misleading", "accurate", "neutral", "condition", "experiment",
                       "test", "credulous", "steer", "fixable", "transient", "permanent", "convention", "spelling",
                       "hyphen", "case"):
            self.assertNotIn(leaked, words, leaked)


class TestParsingAndCoding(unittest.TestCase):
    def test_parse_and_normalize(self):
        p = parse_reply('Checking.\nCALL stock_lookup {"site": "Kelso", "sku": "KX-4471"}')
        self.assertEqual((p["kind"], p["args"]["site"]), ("call", "Kelso"))
        self.assertEqual(parse_reply('CALL shipment_status {"tracking": "x"}')["reason"], "malformed_call")
        self.assertEqual(parse_reply("no protocol here")["reason"], "no_protocol_line")
        for raw, norm in (("132", "132"), ("There are 132 units on hand.", "132"), ("UNKNOWN", "unknown"),
                          ("unknown, the system is down", "unknown")):
            self.assertEqual(normalize_answer(raw), norm, raw)

    def test_classify_response(self):
        failed = _args()
        call = lambda a: {"kind": "call", "args": a}
        d = next(x for x in W.depots if x.name == T.depot)
        other = next(t for t in W.tasks if t.sku != T.sku)
        for nxt, code in ((None, "UNCLASSIFIABLE"), ({"kind": "answer", "value": "UNKNOWN"}, "STOP"),
                          (call(dict(failed)), "RETRY"), (call(_args(site=d.number)), "SITE_ONLY"),
                          (call(_args(form="upper")), "REFORMAT"), (call(_args(form="upper", site=d.number)), "REFORMAT"),
                          (call(_args(task=other)), "OTHER"), (call({"site": "Nowhere", "sku": T.sku}), "OTHER")):
            self.assertEqual(classify_response(W, T, failed, nxt), code, nxt)


class _Replay:
    def __init__(self, replies):
        self.replies, self.seen = list(replies), []

    def say(self, text):
        self.seen.append(text)
        return self.replies.pop(0) if self.replies else "ANSWER UNKNOWN", {"cost_usd": 0.0}


def _episode(replies, claim="format", fault="fixable"):
    out, conv = [], _Replay(replies)
    run_episode(conv, W, ToolEnv(W, claim, fault), out, lambda: 0.0, lambda r, m: None, lambda e: None)
    return out, conv


class TestEpisode(unittest.TestCase):
    def test_responses_and_success(self):
        conv = W.conventions[T.depot]
        given = "CALL stock_lookup " + json.dumps(_args())
        out, _ = _episode([given, given, "CALL stock_lookup " + json.dumps(_args(form=conv)), f"ANSWER {T.truth}"])
        s = out[0]["summary"]
        self.assertEqual((s["responses"], s["first_response"], s["success"], s["correct"]),
                         (["RETRY", "REFORMAT"], "RETRY", True, True))
        self.assertEqual(s["first_call_spelling"], "given")

    def test_budget_format_errors_and_fabrication(self):
        given = "CALL stock_lookup " + json.dumps(_args())
        out, conv = _episode([given] * 7 + ["ANSWER UNKNOWN"], fault="permanent")
        s = out[0]["summary"]
        self.assertEqual((s["calls"], s["over_budget"], s["ended_by"]), (6, 1, "answer"))
        self.assertEqual(conv.seen[7], NO_CALLS_LEFT)
        out, _ = _episode(["hmm", "hmm", "hmm"])
        self.assertEqual(out[0]["summary"]["ended_by"], "protocol_failure")
        out, _ = _episode([given, "ANSWER 250"], fault="permanent")
        self.assertTrue(out[0]["summary"]["unsupported"])
        self.assertEqual(out[0]["summary"]["first_response"], "STOP")


def _runs(code_early, code_late, n=10):
    return [[code_early, code_early, None, None, code_late, code_late] for _ in range(n)]


class TestSteeringAndLearning(unittest.TestCase):
    def test_hand_computed(self):
        by_cell = {}
        for claim, fault in cells():
            kind = cell_kind(claim, fault)
            if kind == "neutral":
                by_cell[(claim, fault)] = _runs("RETRY", "RETRY")
            elif kind == "accurate":
                implied = {"format": "REFORMAT", "transient": "RETRY", "permanent": "STOP"}[claim]
                by_cell[(claim, fault)] = _runs(implied, implied)
            else:
                implied = {"format": "REFORMAT", "transient": "RETRY", "permanent": "STOP"}[claim]
                by_cell[(claim, fault)] = _runs(implied, "OTHER")  # follows early, abandons late
        r = steering_and_learning(by_cell)
        # Neutral baseline is RETRY: transient claims add nothing, format and permanent claims add 1.
        self.assertAlmostEqual(r["deltas"]["transient|fixable"], 0.0)
        self.assertAlmostEqual(r["deltas"]["format|permanent"], 1.0)
        self.assertAlmostEqual(r["S"], 4 / 6)
        self.assertAlmostEqual(r["L_star"], 1.0, msg="five learnable misleading cells drop fully; accurate cells flat")
        by_cell[CONFIRMABLE_MISLEADING] = _runs("REFORMAT", "REFORMAT")
        self.assertAlmostEqual(steering_and_learning(by_cell)["L_star"], 1.0, msg="the confirmable cell is excluded")


def _summary(S, slo, shi, L, llo, lhi, **v):
    validity = {"completion_min": 1.0, "protocol_failure_share": 0.0, "engagement_min": 1.0, "unclassifiable_share": 0.0}
    validity.update(v)
    return {"S": S, "S_ci": (slo, shi), "L_star": L, "L_star_ci": (llo, lhi), "validity": validity}


class TestVerdict(unittest.TestCase):
    TH = load_config(LIVE)["thresholds"]

    def test_each_verdict(self):
        v = lambda *a, **k: model_verdict(_summary(*a, **k), self.TH)["verdict"]
        self.assertEqual(v(0.02, -0.05, 0.12, 0.0, -0.1, 0.1), "KILL_WORDING_IRRELEVANT")
        self.assertEqual(v(0.40, 0.25, 0.55, 0.02, -0.08, 0.12), "CONTINUE_CREDULOUS")
        self.assertEqual(v(0.40, 0.25, 0.55, 0.40, 0.20, 0.60), "CONTINUE_SELF_CORRECTING")
        self.assertEqual(v(0.40, 0.25, 0.55, 0.08, -0.05, 0.25), "INCONCLUSIVE")
        self.assertEqual(v(0.18, 0.05, 0.30, 0.0, -0.1, 0.1), "INCONCLUSIVE")
        self.assertEqual(v(-0.30, -0.45, -0.15, 0.0, -0.1, 0.1), "INCONCLUSIVE",
                         "messages that push agents the other way are not 'wording irrelevant'")
        for kw in ({"completion_min": 0.9}, {"protocol_failure_share": 0.2}, {"engagement_min": 0.5},
                   {"unclassifiable_share": 0.2}):
            self.assertEqual(v(0.40, 0.25, 0.55, 0.40, 0.2, 0.6, **kw), "INVALID", kw)


class TestCapsGatingPilot(unittest.TestCase):
    def test_spend_guard(self):
        g = SpendGuard(0.03, 10, 0.01)
        g.settle(g.reserve(), 0.012)
        g.reserve()
        with self.assertRaises(SpendCapExceeded):
            g.reserve()

    def test_live_needs_flag_and_a_budget(self):
        for name in ("live_claude_haiku.json", "live_gpt41mini.json", "live_e1_claude_haiku.json"):
            cfg = load_config(DIR / "configs" / name)
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    make_transport(cfg, Path(tmp), live=False)
                with self.assertRaises(RuntimeError, msg="a $0 cap blocks live calls"):
                    make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)
        self.assertEqual(load_config(DIR / "configs" / "live_gpt41mini.json")["max_equiv_usd"], 0.0,
                         "no budget was approved for the OpenAI config")

    def test_pilot_on_mock(self):
        cfg = load_config(DIR / "configs" / "mock_credulous.json")
        with tempfile.TemporaryDirectory() as tmp:
            r = pilot(cfg, Path(tmp), live=False)
            self.assertEqual((r["runs"], r["complete"]), (12, 12))
            self.assertTrue((Path(tmp) / "pilot" / "PILOT.md").exists())


class _FlakyTransport:
    """Fails the first conversation of one run on its first turn, as a CLI timeout would."""
    label, is_mock = "flaky", True

    def __init__(self, inner, fail_key):
        self.inner, self.fail_key, self.failed = inner, fail_key, False

    def open(self, conv_key, system, crn_seed=None):
        conv = self.inner.open(conv_key, system)
        if conv_key == self.fail_key and not self.failed:
            self.failed = True

            class Boom:
                def say(self, text):
                    raise RuntimeError("Command '[claude ...]' timed out after 480 seconds")
            return Boom()
        return conv


class TestTransportFailureRerun(unittest.TestCase):
    def test_failed_run_is_rerun_once_and_both_attempts_kept(self):
        from causetest.runner import _Session, _run_all
        from causetest.transports import MockTransport
        cfg = load_config(DIR / "configs" / "mock_credulous.json")
        cfg.update(runs_per_cell=1, workers=2)
        with tempfile.TemporaryDirectory() as tmp:
            key = f"neutral|fixable|{cfg['base_seed']}"
            t = _FlakyTransport(MockTransport("credulous", {}), key)
            session = _Session(cfg, Path(tmp), t, SpendGuard(0, 10, 0))
            rows = _run_all(session, cfg, [cfg["base_seed"]])
            mine = [r for r in rows if r["run_id"] == key]
            self.assertEqual([(r["status"], r["attempt"]) for r in mine], [("failed", 1), ("complete", 2)])
            self.assertEqual(len(rows), 13)


class TestReproducibility(unittest.TestCase):
    """Paper plan W0: analysis does not depend on row order; `reproduce` catches changed raw data."""

    def _small_run(self, tmp):
        cfg = load_config(DIR / "configs" / "mock_credulous.json")
        cfg.update(runs_per_cell=4, bootstrap_reps=200, workers=3)
        d = Path(tmp) / "runs" / "r"
        run(cfg, d, live=False)
        return d

    def test_analysis_is_order_independent(self):
        import random as _r
        from causetest.runner import analyze
        with tempfile.TemporaryDirectory() as tmp:
            d = self._small_run(tmp)
            first = (d / "analysis" / "summary.json").read_bytes()
            lines = (d / "results.jsonl").read_text(encoding="utf-8").splitlines()
            _r.Random(7).shuffle(lines)
            (d / "results.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
            analyze(d)
            self.assertEqual((d / "analysis" / "summary.json").read_bytes(), first)
            self.assertNotIn(b"\r\n", first)  # reports are written with LF on every platform

    def test_reproduce_catches_changed_raw_data(self):
        from causetest.runner import reproduce
        with tempfile.TemporaryDirectory() as tmp:
            d = self._small_run(tmp)
            root = d.parent
            self.assertTrue(reproduce(root, [d], write_manifest=True)["passed"])
            self.assertTrue(reproduce(root, [d])["passed"])
            lines = (d / "results.jsonl").read_text(encoding="utf-8").splitlines()
            lines[0] += " "  # still valid JSON, but not the pinned bytes
            (d / "results.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
            r = reproduce(root, [d])
            self.assertFalse(r["passed"])
            self.assertEqual(r["raw_mismatches"], ["r/results.jsonl"])
            (d / "analysis" / "VERDICT.md").write_text("edited\n", encoding="utf-8")
            self.assertFalse(reproduce(root, [d], write_manifest=True)["runs"]["r"]["VERDICT.md"])


class TestNativeToolCalling(unittest.TestCase):
    """Paper plan W1: native function calls are translated to and from the episode's text protocol."""

    @staticmethod
    def _fake(payloads, sent):
        import io

        def urlopen(req, timeout=None, context=None):
            sent.append(json.loads(req.data.decode()))
            return io.BytesIO(json.dumps(payloads.pop(0)).encode())
        return urlopen

    def test_prompt_changes_only_the_call_rule(self):
        from causetest.e2 import system_for
        from causetest.protocol import NATIVE_CALL_RULE, TEXT_CALL_RULE
        text, native = system_prompt(W), system_prompt(W, native=True)
        self.assertEqual(native.replace(NATIVE_CALL_RULE, TEXT_CALL_RULE), text)
        self.assertNotIn("CALL stock_lookup", native)
        self.assertIn(NATIVE_CALL_RULE, system_for(W, "caution_bounded", native=True))

    def test_translation_both_ways(self):
        from unittest import mock
        from causetest.transports import OpenAINativeTransport
        call = {"type": "function_call", "call_id": "c1", "name": "stock_lookup",
                "arguments": '{"site": "Penrith",\n "sku": "wm-9610"}'}
        answer = {"type": "message", "content": [{"type": "output_text", "text": "ANSWER UNKNOWN"}]}
        usage = {"input_tokens": 10, "output_tokens": 2}
        payloads = [{"output": [call], "usage": usage}, {"output": [answer], "usage": usage},
                    {"output": [dict(call, call_id="c2")], "usage": usage}, {"output": [answer], "usage": usage}]
        sent = []
        conv = OpenAINativeTransport("m", {"reasoning": {"effort": "low"}}, {"input": 1.0, "output": 1.0}).open("k", "sys")
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), \
                mock.patch("urllib.request.urlopen", self._fake(payloads, sent)):
            reply, meta = conv.say("New request: one")
            self.assertEqual(reply, 'CALL stock_lookup {"site": "Penrith", "sku": "wm-9610"}')  # one line
            self.assertEqual(parse_reply(reply)["kind"], "call")
            self.assertEqual((sent[0]["parallel_tool_calls"], sent[0]["tools"][0]["name"]), (False, "stock_lookup"))
            self.assertEqual(sent[0]["reasoning"], {"effort": "low"})
            reply, _ = conv.say("RESULT stock_lookup: ERROR: temporary service problem.")
            self.assertEqual(reply, "ANSWER UNKNOWN")
            last = sent[1]["input"][-2:]
            self.assertEqual(last[0]["type"], "function_call")
            self.assertEqual(last[1], {"type": "function_call_output", "call_id": "c1",
                                       "output": "ERROR: temporary service problem."})
            conv.say("New request: two")  # returns a call (c2) that the harness never answers...
            conv.say("New request: three")  # ...so it is closed before the next request's user message
            tail = sent[3]["input"][-3:]
            self.assertEqual(tail[1], {"type": "function_call_output", "call_id": "c2", "output": NO_CALLS_LEFT})
            self.assertEqual(tail[2], {"role": "user", "content": "New request: three"})

    def test_comparison_rule_and_self_comparison(self):
        from causetest.compare import compare, verdict
        self.assertEqual(verdict(0.05, -0.1, 0.2), "SAME")
        self.assertEqual(verdict(0.05, -0.1, 0.3), "UNCLEAR")  # interval too wide to call it the same
        self.assertEqual(verdict(0.4, 0.2, 0.6), "DIFFERENT")
        self.assertEqual(verdict(0.12, 0.02, 0.22), "SAME")
        self.assertEqual(verdict(0.2, -0.05, 0.45), "UNCLEAR")
        self.assertEqual(verdict(None, None, None), "NOT_ESTIMABLE")
        cfg = load_config(DIR / "configs" / "mock_credulous.json")
        cfg.update(runs_per_cell=6, bootstrap_reps=100, workers=2)
        with tempfile.TemporaryDirectory() as tmp:
            run(cfg, Path(tmp) / "a", live=False)
            r = compare(Path(tmp) / "a", Path(tmp) / "a", "C4", reps=200)
        self.assertTrue(all(m["diff"] in (0.0, None) for m in r["measures"].values()))
        self.assertEqual(set(k for k, m in r["measures"].items() if m["primary"]),
                         {"S", "retry_trap_success", "give_up_trap_success"})

    def test_native_transport_is_gated(self):
        cfg = load_config(DIR / "configs" / "live_gpt6luna.json")
        native = dict(cfg, transport="openai_responses_native")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                make_transport(native, Path(tmp), live=False)
            with self.assertRaises(RuntimeError):
                make_transport(dict(native, max_equiv_usd=0.0), Path(tmp), live=True)


class TestOpenRouterTransport(unittest.TestCase):
    """Paper plan W2: the OpenRouter transport pins one host, logs the billed cost and translates tool calls.
    Every test answers from a fake server; nothing is sent."""
    DRAFT = DIR / "configs" / "live_or_c4_deepseek_v4_1_flash_r0.json"
    PANEL = sorted((DIR / "configs").glob("live_or_*.json"))
    HOST = "DeepInfra"

    @classmethod
    def _server(cls, sent, host=None, cost=0.0002, extra=None):
        """A fake OpenRouter: a tool call after each user message, then ANSWER UNKNOWN after the tool result."""
        import io
        n = [0]

        def urlopen(req, timeout=None, context=None):
            body = json.loads(req.data.decode())
            sent.append(body)
            n[0] += 1
            if body["messages"][-1]["role"] == "user":
                fn = {"name": "stock_lookup", "arguments": '{"site": "Penrith",\n "sku": "wm-9610"}'}
                msg = {"role": "assistant", "content": None, "reasoning_details": [{"type": "reasoning.text"}],
                       "tool_calls": [{"id": f"t{n[0]}", "type": "function", "function": fn}]}
            else:
                msg = {"role": "assistant", "content": "ANSWER UNKNOWN", "reasoning": "thinking"}
            usage = {"prompt_tokens": 100, "completion_tokens": 10}
            if cost is not None:
                usage["cost"] = cost
            payload = {"id": f"gen-{n[0]}", "provider": host or cls.HOST, "model": body["model"],
                       "choices": [{"message": msg, "finish_reason": "stop"}], "usage": usage}
            payload.update(extra or {})
            return io.BytesIO(json.dumps(payload).encode())
        return urlopen

    def _open(self, **kw):
        from causetest.transports import OpenRouterNativeTransport
        t = OpenRouterNativeTransport("m", {"order": [self.HOST]}, {"temperature": 1.0}, {"input": 1.0, "output": 1.0}, **kw)
        return t.open("k", "sys")

    def test_translation_pin_and_billed_cost(self):
        from unittest import mock
        sent = []
        conv = self._open()
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch("urllib.request.urlopen", self._server(sent)):
            reply, meta = conv.say("New request: one")
            self.assertEqual(reply, 'CALL stock_lookup {"site": "Penrith", "sku": "wm-9610"}')  # one line
            self.assertEqual(parse_reply(reply)["kind"], "call")
            b = sent[0]
            self.assertEqual(b["provider"], {"order": [self.HOST], "allow_fallbacks": False, "require_parameters": True})
            self.assertEqual((b["tools"][0]["function"]["name"], b["temperature"]), ("stock_lookup", 1.0))
            self.assertNotIn("parallel_tool_calls", b)  # no open-model host lists it; it could block routing
            self.assertEqual(b["messages"][0], {"role": "system", "content": "sys"})
            self.assertEqual((meta["cost_usd"], meta["cost_source"], meta["host"], meta["generation_id"]),
                             (0.0002, "billed", self.HOST, "gen-1"))
            reply, meta = conv.say("RESULT stock_lookup: ERROR: temporary service problem.")
            self.assertEqual((reply, meta["reasoning_chars"]), ("ANSWER UNKNOWN", 8))
            self.assertEqual(sent[1]["messages"][-2]["tool_calls"][0]["id"], "t1")
            self.assertEqual(sent[1]["messages"][-1], {"role": "tool", "tool_call_id": "t1",
                                                       "content": "ERROR: temporary service problem."})
            self.assertNotIn("reasoning_details", sent[1]["messages"][-2])  # reasoning is not passed back
            conv.say("New request: two")  # returns a call (t3) that the harness never answers...
            self.assertEqual(sent[2]["messages"][-2], {"role": "assistant", "content": "ANSWER UNKNOWN"})
            conv.say("New request: three")  # ...so it is closed before the next request's user message
            tail = sent[3]["messages"][-2:]
            self.assertEqual(tail, [{"role": "tool", "tool_call_id": "t3", "content": NO_CALLS_LEFT},
                                    {"role": "user", "content": "New request: three"}])

    def test_pin_must_be_one_host_without_fallbacks(self):
        from causetest.transports import openrouter_pin
        for bad in ({}, {"order": []}, {"order": ["A", "B"]}, {"order": ["A"], "allow_fallbacks": True},
                    {"order": ["A"], "require_parameters": False}, None):
            with self.assertRaises(ValueError, msg=bad):
                openrouter_pin(bad)
        self.assertEqual(openrouter_pin({"order": ["A"], "quantizations": ["fp8"]})["quantizations"], ["fp8"])

    def test_endpoint_tag_pin_matches_the_host_name(self):
        from causetest.transports import OpenRouterNativeTransport
        t = OpenRouterNativeTransport("m", {"order": ["deepinfra/fp8"]}, {}, {"input": 1, "output": 1})
        self.assertEqual([t.served_by_pin(h) for h in ("DeepInfra", "deepinfra", "Together", None)],
                         [True, True, False, False])
        z = OpenRouterNativeTransport("m", {"order": ["z-ai/fp8"]}, {}, {"input": 1, "output": 1}, expected_host="Z.AI")
        self.assertEqual([z.served_by_pin(h) for h in ("Z.AI", "z-ai", "Zhipu")], [True, True, False])

    def test_wrong_host_fails_but_its_cost_counts(self):
        from unittest import mock
        from causetest.transports import BilledTransportError
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch("urllib.request.urlopen", self._server([], host="Other", cost=0.003)):
            with self.assertRaises(BilledTransportError) as ctx:
                self._open().say("New request: one")
        self.assertEqual((ctx.exception.meta["cost_usd"], ctx.exception.meta["host"]), (0.003, "Other"))

    def test_estimate_when_unbilled_and_errors_inside_200(self):
        from unittest import mock
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch("urllib.request.urlopen", self._server([], cost=None)):
            _, meta = self._open().say("New request: one")
        self.assertEqual((meta["cost_source"], meta["cost_usd"]), ("price_estimate", 110 / 1e6))
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch("urllib.request.urlopen", self._server([], extra={"error": {"code": 502, "message": "x"}})):
            with self.assertRaises(RuntimeError):
                self._open().say("New request: one")

    def test_rate_limits_are_retried_and_counted(self):
        import io
        import urllib.error
        from unittest import mock
        ok = self._server([])
        calls = []

        def flaky(req, timeout=None, context=None):  # two 429s, then a normal answer
            calls.append(1)
            if len(calls) <= 2:
                raise urllib.error.HTTPError("u", 429, "rate limited", {}, io.BytesIO(b'{"error": "rate"}'))
            return ok(req, timeout, context)

        def always(req, timeout=None, context=None):
            raise urllib.error.HTTPError("u", 429, "rate limited", {}, io.BytesIO(b'{"error": "rate"}'))
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), mock.patch("time.sleep") as slept:
            with mock.patch("urllib.request.urlopen", flaky):
                reply, meta = self._open().say("New request: one")
            self.assertEqual((meta["rate_limit_retries"], slept.call_count), (2, 2))
            self.assertTrue(reply.startswith("CALL "))
            with mock.patch("urllib.request.urlopen", always), self.assertRaises(RuntimeError) as ctx:
                self._open().say("New request: one")
            self.assertIn("HTTP 429", str(ctx.exception))

    def test_timeouts_are_retried_and_counted(self):
        """Deviation W2-3: an HTTP 504, a 504 inside a 200 response, and a response still trickling in past the
        deadline are each retried and counted; the next answer goes through unchanged."""
        import io
        import itertools
        import urllib.error
        from unittest import mock
        ok, calls = self._server([]), []

        class Trickle:  # keep-alive whitespace that never ends
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read1(self, n):
                return b" "

        def flaky(req, timeout=None, context=None):
            calls.append(timeout)
            if len(calls) == 1:
                raise urllib.error.HTTPError("u", 504, "timeout", {}, io.BytesIO(b'{"error": "timeout"}'))
            if len(calls) == 2:
                return io.BytesIO(json.dumps({"error": {"code": 504, "message": "Provider timed out",
                                                        "metadata": {"error_type": "timeout"}}}).encode())
            if len(calls) == 3:
                return Trickle()
            return ok(req, timeout, context)
        clock = itertools.count(0, 7)  # every clock read moves 7 s, so the trickle passes the 60 s deadline
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), mock.patch("time.sleep") as slept, \
                mock.patch("causetest.transports.time.monotonic", lambda: next(clock)), \
                mock.patch("urllib.request.urlopen", flaky):
            reply, meta = self._open().say("New request: one")
        self.assertTrue(reply.startswith("CALL "))
        self.assertEqual((meta["timeout_retries"], meta["rate_limit_retries"], slept.call_count), (3, 0, 3))
        self.assertEqual(calls[0], 60, "the socket timeout is capped at the deadline")
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), mock.patch("time.sleep"), \
                mock.patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError(
                    "u", 504, "timeout", {}, io.BytesIO(b"{}"))), self.assertRaises(RuntimeError) as ctx:
            self._open().say("New request: one")
        self.assertIn("'timeout': 6", str(ctx.exception))
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), mock.patch("time.sleep") as slept, \
                mock.patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError(
                    "u", 500, "boom", {}, io.BytesIO(b"{}"))), self.assertRaises(RuntimeError):
            self._open().say("New request: one")  # any other error is not retried
        self.assertEqual(slept.call_count, 0)

    def test_no_key_sends_nothing(self):
        from unittest import mock
        sent = []
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": ""}), \
                mock.patch("urllib.request.urlopen", self._server(sent)):
            with self.assertRaises(RuntimeError):
                self._open().say("New request: one")
        self.assertEqual(sent, [])

    def test_reasoning_passed_back_only_when_set(self):
        from unittest import mock
        sent = []
        conv = self._open(pass_reasoning_back=True)
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}),                 mock.patch("urllib.request.urlopen", self._server(sent)):
            conv.say("New request: one")
            conv.say("RESULT stock_lookup: 4")
        self.assertEqual(sent[1]["messages"][-2]["reasoning_details"], [{"type": "reasoning.text"}])

    def test_panel_configs_are_gated_and_well_formed(self):
        from causetest.runner import plan
        # 10 model-reasoning arms x (C4, E5), plus gpt-oss C4 on a second host (deviation W2-7)
        self.assertEqual(len(self.PANEL), 21)
        names = set()
        for path in self.PANEL:
            cfg = load_config(path)
            names.add(cfg["run_name"])
            # W2-A, owner's choice 2026-10-22; gpt-oss-120b added by deviation W2-6 (2026-10-23)
            approved = any(m in path.name for m in ("deepseek", "qwen", "gemma", "gpt_oss"))
            self.assertEqual(cfg["max_equiv_usd"], float(cfg["planning"]["proposed_cap_usd"]) if approved else 0.0,
                             f"{path.name}: only the W2-A configs have an approved budget")
            self.assertEqual((cfg["transport"], cfg["request_options"]["temperature"]), ("openrouter_chat_native", 1.0))
            self.assertIn("reasoning", cfg["request_options"], "reasoning is set explicitly, never a host default")
            self.assertEqual(len(cells_for(cfg)), 3 if cfg.get("design") == "E5" else 12)
            self.assertGreater(plan(cfg)["estimated_equiv_usd"], 0)
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    make_transport(cfg, Path(tmp), live=False)
                with self.assertRaises(RuntimeError):
                    make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)
                t = make_transport(dict(cfg, max_equiv_usd=1.0), Path(tmp), live=True)  # builds; sends nothing
                self.assertTrue(t.served_by_pin(cfg["expected_host"]), path.name)
        self.assertEqual(len(names), len(self.PANEL), "every config writes to its own run folder")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                make_transport(dict(load_config(self.DRAFT), max_equiv_usd=1.0, provider={"order": ["A", "B"]}),
                               Path(tmp), live=True)

    def test_run_through_the_runner(self):
        """A whole (fake) run: native prompt, host and billed cost in the records, the journal's spend, the cache
        key's host, and a wrong host failing the run while its billed cost still counts against the cap."""
        from unittest import mock
        from causetest.protocol import NATIVE_CALL_RULE
        cfg = dict(load_config(self.DRAFT), max_equiv_usd=1.0, runs_per_cell=2, workers=1, bootstrap_reps=50,
                   cells=["|".join(cells()[0])])
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            sent = []
            with mock.patch("urllib.request.urlopen", self._server(sent)):
                run(cfg, Path(tmp) / "ok", live=True)
            self.assertIn(NATIVE_CALL_RULE, sent[0]["messages"][0]["content"])
            rows = [json.loads(x) for x in (Path(tmp) / "ok" / "results.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual([r["status"] for r in rows], ["complete", "complete"])
            metas = [t["meta"] for r in rows for task in r["tasks"] for t in task["turns"]]
            self.assertEqual({(m["host"], m["cost_source"]) for m in metas}, {(self.HOST, "billed")})
            journal = (Path(tmp) / "ok" / "journal.jsonl").read_text(encoding="utf-8").splitlines()
            spent = sum(json.loads(x).get("cost_usd", 0) for x in journal if '"response"' in x)
            self.assertAlmostEqual(spent, 0.0002 * len(sent))
            with mock.patch("urllib.request.urlopen", self._server(sent)):  # same config: every run from the cache
                self.assertEqual(run(cfg, Path(tmp) / "ok", live=True)["cost"]["from_cache"], 2)
            moved = dict(cfg, provider={"order": ["Other"]}, expected_host="Other")  # another host never reuses those runs
            with mock.patch("urllib.request.urlopen", self._server([], host="Other")):
                self.assertEqual(run(moved, Path(tmp) / "ok", live=True)["cost"]["from_cache"], 0)
            with mock.patch("urllib.request.urlopen", self._server([], host="Other", cost=0.003)):
                run(cfg, Path(tmp) / "bad", live=True)
            rows = [json.loads(x) for x in (Path(tmp) / "bad" / "results.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), 4)  # two runs, each failed and re-run once
            self.assertTrue(all(r["status"] == "failed" and "not the pinned" in r["error"] for r in rows))
            journal = (Path(tmp) / "bad" / "journal.jsonl").read_text(encoding="utf-8").splitlines()
            spent = sum(json.loads(x).get("cost_usd", 0) for x in journal if '"response"' in x)
            self.assertAlmostEqual(spent, 4 * 0.003)


class TestEndToEndMock(unittest.TestCase):
    def test_small_run_and_cache(self):
        cfg = load_config(DIR / "configs" / "mock_credulous.json")
        cfg.update(runs_per_cell=6, bootstrap_reps=200, workers=2)
        with tempfile.TemporaryDirectory() as tmp:
            s = run(cfg, Path(tmp) / "r", live=False)
            self.assertGreater(s["S"], 0.25)
            self.assertEqual(s["cost"]["runs_recorded"], 72)
            again = run(cfg, Path(tmp) / "r", live=False)
            self.assertEqual(again["cost"]["from_cache"], 72)


class TestExtensionE1(unittest.TestCase):
    CELLS = [("transient", "fixable"), ("transient", "transient"), ("permanent", "transient"), ("permanent", "permanent")]

    def test_default_worlds_unchanged(self):
        saved = DIR / "runs" / "live-claude-haiku-5-5" / "worlds.jsonl"
        if not saved.exists():
            self.skipTest("kill-test worlds not present")
        for line in saved.read_text().splitlines():
            w = json.loads(line)
            self.assertEqual(make_world(w["seed"]).to_json(), w, w["seed"])

    def test_long_worlds(self):
        for seed in range(20261301, 20261313):
            w = make_world(seed, 18)
            depots = [t.depot for t in w.tasks]
            self.assertEqual(sorted(depots.count(d) for d in set(depots)), [6, 6, 6])
            self.assertEqual(len({t.sku for t in w.tasks}), 18)
            self.assertEqual(len({w.conventions[d] for d in set(depots)}), 3)
        with self.assertRaises(ValueError):
            make_world(1, 7)

    def test_cells_for(self):
        cfg = load_config(DIR / "configs" / "live_e1_claude_haiku.json")
        self.assertEqual(cells_for(cfg), self.CELLS)
        self.assertEqual(len(cells_for({})), 12)
        with self.assertRaises(ValueError):
            cells_for({"cells": ["format|nonsense"]})

    def test_learning_hand_computed(self):
        from causetest.extension import learning
        follow = {"transient": "RETRY", "permanent": "STOP"}

        def runs(early, late):
            return [[early] * 3 + [None] * 12 + [late] * 3 for _ in range(5)]
        by_cell = {("transient", "fixable"): runs("RETRY", "REFORMAT"),     # abandons the claim: L = 1
                   ("transient", "transient"): runs("RETRY", "RETRY"),      # accurate, stays: L = 0
                   ("permanent", "transient"): runs("RETRY", "STOP"),       # follows more: L = -1
                   ("permanent", "permanent"): runs("RETRY", "STOP")}       # same drift in the accurate cell
        r = learning(by_cell, self.CELLS, 18)
        self.assertEqual(r["L"]["transient|fixable"], 1.0)
        self.assertEqual(r["contrasts"]["permanent: transient vs permanent"], 0.0, "claim-wide drift cancels")
        self.assertAlmostEqual(r["L_E1"], 0.5)
        self.assertEqual(set(follow), {c for c, _ in self.CELLS})

    def test_verdict_e1(self):
        from causetest.extension import verdict_e1
        th = load_config(DIR / "configs" / "live_e1_claude_haiku.json")["thresholds"]
        ok = {"completion_min": 1.0, "protocol_failure_share": 0.0, "engagement_min": 1.0, "unclassifiable_share": 0.0}
        v = lambda L, lo, hi, **kw: verdict_e1({"L_E1": L, "L_E1_ci": (lo, hi), "validity": dict(ok, **kw)}, th)["verdict"]
        self.assertEqual(v(0.4, 0.2, 0.6), "LEARNS")
        self.assertEqual(v(-0.4, -0.6, -0.2), "ENTRENCHMENT")
        self.assertEqual(v(0.02, -0.1, 0.12), "NO_LEARNING")
        self.assertEqual(v(0.12, -0.05, 0.3), "INCONCLUSIVE")
        self.assertEqual(v(0.4, 0.2, 0.6, completion_min=0.8), "INVALID")

    def test_sizing_rule(self):
        self.assertEqual(size_runs(20.0, 1.6, 0.40, 4, 12), 11)   # (20 - 1.6) // 1.6 = 11
        self.assertEqual(size_runs(20.0, 1.0, 0.20, 4, 12), 12)   # capped at the planned number
        self.assertEqual(size_runs(20.0, 1.0, 10.0, 4, 12), 0)


class TestLunaHistoryCut(unittest.TestCase):
    """Luna deviation L1: the agent's history keeps each reply only up to its first CALL or ANSWER line."""

    def test_cut(self):
        from causetest.protocol import cut_after_first_protocol_line as cut
        call = 'CALL stock_lookup {"site": "Penrith", "sku": "wm-9610"}'
        self.assertEqual(cut(call + " \nANSWER UNKNOWN \nANSWER UNKNOWN"), call + " ")
        self.assertEqual(cut("Let me check.\n" + call + "\nANSWER 5"), "Let me check.\n" + call)
        self.assertEqual(cut("ANSWER 75"), "ANSWER 75")
        self.assertEqual(cut("no protocol line here\nsecond"), "no protocol line here\nsecond")
        glued = call + "ANSWER UNKNOWN"  # one line: kept whole, still a protocol failure
        self.assertEqual(cut(glued), glued)
        self.assertEqual(parse_reply(cut(call + "\nANSWER 1"))["kind"], parse_reply(call + "\nANSWER 1")["kind"])

    def test_transport_history_and_cache_key(self):
        import io
        from unittest import mock
        from causetest.transports import OpenAIResponsesTransport
        reply = 'CALL stock_lookup {"site": "1", "sku": "a"}\nANSWER UNKNOWN'
        body = json.dumps({"output": [{"type": "message", "content": [{"type": "output_text", "text": reply}]}],
                           "usage": {"input_tokens": 10, "output_tokens": 5}}).encode()
        for cut_on, expect in ((True, 'CALL stock_lookup {"site": "1", "sku": "a"}'), (False, reply)):
            conv = OpenAIResponsesTransport("m", {}, {"input": 1.0, "output": 1.0}, history_cut=cut_on).open("k", "sys")
            with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), \
                    mock.patch("urllib.request.urlopen", return_value=io.BytesIO(body)):
                got, meta = conv.say("hi")
            self.assertEqual(got, reply)                       # the recorded reply is the full text
            self.assertEqual(conv.messages[-1]["content"], expect)
            self.assertEqual(meta.get("history_reply_cut"), True if cut_on else None)
        for name in ("live_gpt6luna.json", "live_e1_gpt6luna.json"):
            cfg = load_config(DIR / "configs" / name)
            self.assertTrue(cfg["history_cut_after_first_protocol_line"])
            opts = cfg["request_options"]  # deviation L2; Luna accepts temperature only with reasoning off
            self.assertEqual(opts["reasoning"]["effort"], "low")
            self.assertNotIn("temperature", opts)
        self.assertNotIn("history_cut_after_first_protocol_line", load_config(LIVE))


class TestExtensionE2(unittest.TestCase):
    """Extension E2: one sentence in the system prompt or the error message (PROTOCOL_E2.md)."""
    E2_LIVE = DIR / "configs" / "live_e2_gpt6luna.json"

    def test_prompts(self):
        from causetest.e2 import CAUTION, STRATEGY, system_for
        base = system_prompt(W)
        self.assertEqual(system_prompt(W, None), base)
        self.assertEqual(system_prompt(W, ()), base)
        for arm in ("control", "mixed", "honest"):
            self.assertEqual(system_for(W, arm), base, arm)
        caution, both = system_for(W, "caution"), system_for(W, "caution_strategy")
        self.assertIn(f"\n\nErrors\n- {CAUTION}\n\nDepot directory:", caution)
        self.assertIn(f"\n\nErrors\n- {CAUTION}\n- {STRATEGY}\n\nDepot directory:", both)
        self.assertEqual(caution.replace(f"\n\nErrors\n- {CAUTION}", ""), base)

    def test_error_texts(self):
        from causetest.e2 import HONEST, INSTRUCTION, error_text
        for claim in CLAIMS:
            self.assertEqual(error_text("control", claim), CLAIM_TEXT[claim])
            self.assertEqual(error_text("caution", claim), CLAIM_TEXT[claim])
            self.assertEqual(error_text("mixed", claim), f"{CLAIM_TEXT[claim]} {INSTRUCTION}")
        self.assertEqual(error_text("honest", "unknown"), HONEST)
        words = set(re.findall(r"[a-z]+", HONEST.lower()))
        for w in ("temporary", "unavailable", "written", "service", "try", "check", "again"):
            self.assertNotIn(w, words, w)
        env = ToolEnv(W, "unknown", "fixable", HONEST)
        self.assertEqual(env.call(0, _args())[1], HONEST)
        with self.assertRaises(ValueError):
            ToolEnv(W, "unknown", "fixable")  # a claim outside C4 needs an explicit message

    def test_agent_sees_no_design_information(self):
        from causetest.e2 import ARMS, error_text, system_for
        texts = [system_for(W, a) for a in ARMS] + [result_message(error_text(a, c)) for a in ARMS
                                                    for c in (("unknown",) if a == "honest" else CLAIMS)]
        words = set(re.findall(r"[a-z]+", " ".join(texts).lower()))
        for leaked in ("claim", "fault", "cell", "misleading", "accurate", "neutral", "condition", "experiment",
                       "test", "credulous", "trap", "arm", "caution", "honest", "intervention", "fixable",
                       "transient", "permanent", "convention", "spelling", "hyphen", "case"):
            self.assertNotIn(leaked, words, leaked)

    def test_cells(self):
        from causetest.e2 import valid_cell
        cfg = load_config(self.E2_LIVE)
        cs = cells_for(cfg)
        self.assertEqual(len(cs), 21)
        self.assertEqual(len(set(cs)), 21)
        self.assertTrue(all(valid_cell(*c) for c in cs))
        self.assertFalse(valid_cell("honest", "transient", "fixable"))
        self.assertFalse(valid_cell("caution", "unknown", "fixable"))
        with self.assertRaises(ValueError):
            cells_for(dict(cfg, cells=["caution|unknown|fixable"]))

    def test_contrasts_and_rule(self):
        from causetest.e2 import contrast_verdict, contrasts
        th = load_config(self.E2_LIVE)["thresholds"]
        stats = {("control", "transient", "fixable"): [(0.0, 6.0), (0.0, 6.0)],
                 ("caution", "transient", "fixable"): [(0.5, 4.0), (1.0, 2.0)],
                 ("control", "permanent", "permanent"): [(0.0, 1.0)] * 2,
                 ("caution", "permanent", "permanent"): [(0.0, 3.0), (0.0, 4.0)],
                 ("control", "transient", "transient"): [(1.0, 3.0)] * 2,
                 ("caution", "transient", "transient"): [(1.0, 3.0), (0.5, 4.0)],
                 ("control", "neutral", "fixable"): [(0.25, 3.0)],
                 ("honest", "unknown", "fixable"): [(0.75, 3.0)]}
        c = contrasts(stats)
        self.assertAlmostEqual(c["caution|retry_trap"], 0.75)
        self.assertAlmostEqual(c["caution|cost_calls_accurate_unavailable"], 2.5)
        self.assertAlmostEqual(c["caution|cost_success_accurate_temporary"], -0.25)
        self.assertAlmostEqual(c["honest|retry_trap"], 0.75)  # the honest cell stands in for the trap cell
        self.assertAlmostEqual(c["honest_vs_neutral|fixable"], 0.5)
        self.assertNotIn("caution|give_up_trap", c)
        v = lambda x, lo, hi: contrast_verdict(x, (lo, hi), th)
        self.assertEqual(v(0.8, 0.6, 0.9), "RESCUES")
        self.assertEqual(v(0.6, 0.2, 0.8), "HELPS")
        self.assertEqual(v(0.3, 0.1, 0.5), "HELPS")
        self.assertEqual(v(-0.3, -0.5, -0.1), "HARMS")
        self.assertEqual(v(0.02, -0.05, 0.1), "NO_EFFECT")
        self.assertEqual(v(0.12, -0.05, 0.3), "INCONCLUSIVE")
        self.assertEqual(v(None, None, None), "NOT_ESTIMABLE")

    def test_small_mock_run_keeps_the_arm(self):
        cfg = load_config(DIR / "configs" / "mock_e2_prompt_responsive.json")
        cfg.update(runs_per_cell=3, bootstrap_reps=100, workers=2)
        with tempfile.TemporaryDirectory() as tmp:
            s = run(cfg, Path(tmp) / "r", live=False)
            rows = [json.loads(x) for x in (Path(tmp) / "r" / "results.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 63)
        self.assertTrue(all(r["run_id"].startswith(r["arm"] + "|") for r in rows))
        self.assertEqual(s["design"], "E2")
        self.assertEqual(set(s["contrast_verdicts"]), {f"{a}|{t}" for a in ("caution", "caution_strategy", "mixed", "honest")
                                                       for t in ("retry_trap", "give_up_trap")})

    def test_live_config_is_gated(self):
        cfg = load_config(self.E2_LIVE)
        self.assertLessEqual(cfg["max_equiv_usd"], 4.0, "approved: $0.25 pilot cap, then $4 for pilot and main run")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                make_transport(cfg, Path(tmp), live=False)
            with self.assertRaises(RuntimeError, msg="a $0 cap blocks live calls"):
                make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)
        self.assertTrue(cfg["history_cut_after_first_protocol_line"])
        self.assertEqual(cfg["request_options"]["reasoning"]["effort"], "low")
        self.assertNotIn("temperature", cfg["request_options"])


class TestExtensionE3(unittest.TestCase):
    """Extension E3: the caution with a stopping rule (PROTOCOL_E3.md)."""
    E3_LIVE = DIR / "configs" / "live_e3_gpt6luna.json"

    def test_prompts(self):
        from causetest.e2 import BOUND_FEW, BOUND_THREE, CAUTION, system_for
        self.assertIn(f"\n\nErrors\n- {CAUTION}\n- {BOUND_FEW}\n\nDepot directory:", system_for(W, "caution_bounded"))
        self.assertIn(f"\n\nErrors\n- {CAUTION}\n- {BOUND_THREE}\n\nDepot directory:", system_for(W, "caution_three"))
        for text in (BOUND_FEW, BOUND_THREE):  # a stopping rule, with no hint about which cause is true
            words = set(re.findall(r"[a-z]+", text.lower()))
            for w in ("temporary", "unavailable", "outage", "service", "spelling", "format", "sku", "depot"):
                self.assertNotIn(w, words, (text, w))

    def test_cells(self):
        cs = cells_for(load_config(self.E3_LIVE))
        self.assertEqual(len(cs), 16)
        self.assertEqual({c[0] for c in cs}, {"control", "caution", "caution_bounded", "caution_three"})

    def test_contrasts_and_rule(self):
        from causetest.e3 import arm_verdict, contrasts_e3
        th = load_config(self.E3_LIVE)["thresholds"]
        stats = {("control", "permanent", "transient"): [(0.0, 1.0)] * 2,
                 ("control", "permanent", "permanent"): [(0.0, 1.0)] * 2,
                 ("control", "transient", "transient"): [(1.0, 3.0)] * 2,
                 ("control", "transient", "fixable"): [(0.0, 6.0)] * 2,
                 ("caution", "permanent", "transient"): [(1.0, 3.0)] * 2,
                 ("caution", "permanent", "permanent"): [(0.0, 5.0), (0.0, 6.0)],
                 ("caution", "transient", "transient"): [(1.0, 3.0)] * 2,
                 ("caution", "transient", "fixable"): [(0.0, 6.0)] * 2,
                 ("caution_three", "permanent", "transient"): [(1.0, 3.0), (0.5, 3.0)],
                 ("caution_three", "permanent", "permanent"): [(0.0, 3.0)] * 2,
                 ("caution_three", "transient", "transient"): [(1.0, 3.0)] * 2,
                 ("caution_three", "transient", "fixable"): [(0.5, 3.0)] * 2}
        c = contrasts_e3(stats)
        self.assertAlmostEqual(c["caution_three|give_up_rescue"], 0.75)
        self.assertAlmostEqual(c["caution_three|outage_calls_vs_caution"], -2.5)
        self.assertAlmostEqual(c["caution_three|outage_calls_vs_control"], 2.0)
        self.assertAlmostEqual(c["caution_three|true_temporary_success"], 0.0)
        self.assertAlmostEqual(c["caution_three|retry_trap"], 0.5)
        self.assertNotIn("caution|outage_calls_vs_caution", c)
        self.assertNotIn("caution_bounded|give_up_rescue", c)

        def v(r, r_ci, cut, cut_ci, h, h_ci):
            est = {"a|give_up_rescue": r, "a|outage_calls_vs_caution": cut, "a|true_temporary_success": h}
            ci = {"a|give_up_rescue": r_ci, "a|outage_calls_vs_caution": cut_ci, "a|true_temporary_success": h_ci}
            return arm_verdict("a", est, ci, th)
        ok_h = (0.0, (-0.05, 0.05))
        self.assertEqual(v(0.9, (0.8, 1.0), -2.0, (-2.5, -1.5), *ok_h), "COST_AWARE")
        self.assertEqual(v(0.9, (0.8, 1.0), -0.3, (-0.8, 0.2), *ok_h), "RESCUE_ONLY")
        self.assertEqual(v(0.2, (0.0, 0.4), -3.0, (-3.5, -2.5), *ok_h), "LOSES_RESCUE")
        self.assertEqual(v(0.0, (-0.1, 0.1), 0.0, (-0.3, 0.3), *ok_h), "NO_GAIN")
        self.assertEqual(v(0.9, (0.8, 1.0), -2.0, (-2.5, -1.5), -0.5, (-0.7, -0.3)), "HARMS_TRUE_TEMPORARY")
        self.assertEqual(v(None, (None, None), -2.0, (-2.5, -1.5), *ok_h), "NOT_ESTIMABLE")

    def test_small_mock_run(self):
        cfg = load_config(DIR / "configs" / "mock_e3_bounded.json")
        cfg.update(runs_per_cell=3, bootstrap_reps=100, workers=2)
        with tempfile.TemporaryDirectory() as tmp:
            s = run(cfg, Path(tmp) / "r", live=False)
        self.assertEqual((s["design"], s["cost"]["runs_recorded"]), ("E3", 48))
        self.assertEqual(set(s["contrast_verdicts"]), {"caution_bounded", "caution_three"})

    def test_live_config_is_gated(self):
        cfg = load_config(self.E3_LIVE)
        self.assertLessEqual(cfg["max_equiv_usd"], 3.5, "approved: $0.25 pilot, then $3.50 if the pilot is healthy")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                make_transport(cfg, Path(tmp), live=False)
            with self.assertRaises(RuntimeError, msg="a $0 cap blocks live calls"):
                make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)
        self.assertTrue(cfg["history_cut_after_first_protocol_line"])
        self.assertEqual(cfg["request_options"]["reasoning"]["effort"], "low")
        self.assertNotIn("temperature", cfg["request_options"])


class TestExtensionE4(unittest.TestCase):
    """Extension E4: mixed accurate and misleading errors (PROTOCOL_E4.md)."""
    E4_LIVE = DIR / "configs" / "live_e4_gpt6luna.json"

    def test_schedules(self):
        from collections import Counter
        from causetest.e4 import KIND_OF, MIXES, schedule_for
        for mix, counts in MIXES.items():
            s = schedule_for(20261601, mix)
            self.assertEqual(Counter(KIND_OF[c] for c in s), Counter(counts))
            self.assertEqual(s, schedule_for(20261601, mix))  # reproducible, and independent of the arm
            claims = Counter(c for c, _ in s)  # each message type appears equally often in both mixes
            self.assertEqual(claims, Counter({"permanent": 4, "transient": 4, "format": 4}))
        self.assertNotEqual(schedule_for(20261601, "rare"), schedule_for(20261602, "rare"))
        with self.assertRaises(ValueError):
            schedule_for(1, "rare", n_tasks=6)

    def test_mixed_env_changes_per_request(self):
        from causetest.e4 import MixedToolEnv
        w = make_world(20261601, 12)
        sched = [("permanent", "transient"), ("format", "fixable")] + [("transient", "transient")] * 10
        out, conv = [], _Replay(["CALL stock_lookup " + json.dumps({"site": w.tasks[0].depot, "sku": w.tasks[0].sku.lower()})] * 3
                                + ["ANSWER UNKNOWN"])
        run_episode(conv, w, MixedToolEnv(w, sched), out, lambda: 0.0, lambda r, m: None, lambda e: None)
        self.assertEqual((out[0]["kind"], out[1]["kind"], out[2]["kind"]), ("give_up_trap", "true_format", "true_temporary"))
        self.assertTrue(out[0]["summary"]["success"])  # the transient fault clears on the third call
        self.assertIn(CLAIM_TEXT["permanent"], conv.seen[1])

    def test_cells_and_contrasts(self):
        from causetest.e4 import contrasts_e4, mix_verdict
        cfg = load_config(self.E4_LIVE)
        self.assertEqual(cells_for(cfg), [("control", "mixed", "rare"), ("control", "mixed", "common"),
                                          ("caution_bounded", "mixed", "rare"), ("caution_bounded", "mixed", "common")])
        with self.assertRaises(ValueError):
            cells_for(dict(cfg, cells=["caution|rare"]))
        base = {"true_unavailable": (0.0, 1.0), "give_up_trap": (0.0, 1.0), "true_temporary": (1.0, 3.0),
                "retry_trap": (0.0, 6.0), "true_format": (1.0, 3.0), "all": (0.5, 2.5)}
        bounded = dict(base, true_unavailable=(0.0, 3.0), give_up_trap=(1.0, 3.0), true_format=(0.5, 3.0),
                       all=(0.6, 2.8))
        f = {f"follow_{m}_{p}": 1.0 for m in ("unavailable", "temporary") for p in ("early", "late", "all")}
        stats = {("control", "mixed", "rare"): [dict(base, **f)] * 2,
                 ("caution_bounded", "mixed", "rare"): [dict(bounded, **f)] * 2}
        c = contrasts_e4(stats)
        self.assertAlmostEqual(c["rare|give_up_rescue"], 1.0)
        self.assertAlmostEqual(c["rare|true_unavailable_calls"], 2.0)
        self.assertAlmostEqual(c["rare|true_format_success"], -0.5)
        self.assertAlmostEqual(c["rare|calls_per_extra_success"], 0.3 / 0.1)
        self.assertNotIn("common|give_up_rescue", c)
        th = cfg["thresholds"]
        v = lambda r, rci, cc, cci: mix_verdict("m", {"m|give_up_rescue": r, "m|true_unavailable_calls": cc},
                                                {"m|give_up_rescue": rci, "m|true_unavailable_calls": cci}, th)
        self.assertEqual(v(0.9, (0.8, 1.0), 2.0, (1.8, 2.2)), "HOLDS")
        self.assertEqual(v(0.9, (0.8, 1.0), 4.0, (3.6, 4.4)), "RESCUE_ONLY")
        self.assertEqual(v(0.2, (0.0, 0.4), 2.0, (1.8, 2.2)), "FADES")

    def test_small_mock_run(self):
        cfg = load_config(DIR / "configs" / "mock_e4_bounded.json")
        cfg.update(runs_per_cell=3, bootstrap_reps=100, workers=2)
        with tempfile.TemporaryDirectory() as tmp:
            s = run(cfg, Path(tmp) / "r", live=False)
            rows = [json.loads(x) for x in (Path(tmp) / "r" / "results.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual((s["design"], len(rows)), ("E4", 12))
        self.assertTrue(all(len(r["tasks"]) == 12 and all("kind" in t for t in r["tasks"]) for r in rows))
        self.assertEqual(set(s["contrast_verdicts"]), {"rare", "common"})

    def test_live_config_is_gated(self):
        cfg = load_config(self.E4_LIVE)
        self.assertLessEqual(cfg["max_equiv_usd"], 4.0)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                make_transport(cfg, Path(tmp), live=False)
            with self.assertRaises(RuntimeError, msg="a $0 cap blocks live calls"):
                make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)
        self.assertTrue(cfg["history_cut_after_first_protocol_line"])
        self.assertEqual(cfg["request_options"]["reasoning"]["effort"], "low")


class TestExtensionE5(unittest.TestCase):
    """Extension E5: does one cleared error make a plain agent persist? (PROTOCOL_E5.md)"""
    E5_LIVE = DIR / "configs" / "live_e5_gpt6luna.json"

    def test_schedules_and_env(self):
        from causetest.e5 import PRIMES, PrimedToolEnv, schedule_for
        for prime in PRIMES:
            s = schedule_for(prime)
            self.assertEqual(s[1:], [("permanent", "transient"), ("permanent", "permanent")])  # same target everywhere
        w = make_world(20261701, 3)
        good = lambda i: "CALL stock_lookup " + json.dumps({"site": w.tasks[i].depot, "sku": w.tasks[i].sku.lower()})
        out, conv = [], _Replay([good(0)] + ["ANSWER UNKNOWN"] * 3)
        run_episode(conv, w, PrimedToolEnv(w, schedule_for("none")), out, lambda: 0.0, lambda r, m: None,
                    lambda e: None)
        self.assertTrue(out[0]["summary"]["success"])  # no fault: the first call works as written
        self.assertEqual([t["kind"] for t in out], ["prime", "target", "after"])
        out, _ = [], None
        run_episode(_Replay([good(0)] * 3 + ["ANSWER 1"]), w, PrimedToolEnv(w, schedule_for("cleared")), out,
                    lambda: 0.0, lambda r, m: None, lambda e: None)
        self.assertEqual((out[0]["summary"]["success"], out[0]["summary"]["failures_before_success"]), (True, 2))

    def test_manipulation_and_rule(self):
        from causetest.e5 import manipulation_ok, verdicts_e5
        self.assertTrue(manipulation_ok("none", {"success": True, "failures_before_success": 0, "failures": 0}))
        self.assertFalse(manipulation_ok("cleared", {"success": True, "failures_before_success": 0, "failures": 0}))
        self.assertTrue(manipulation_ok("cleared", {"success": True, "failures_before_success": 2, "failures": 2}))
        self.assertTrue(manipulation_ok("not_cleared", {"success": False, "failures_before_success": 5, "failures": 5}))
        self.assertFalse(manipulation_ok("not_cleared", {"success": False, "failures_before_success": 1, "failures": 1}))
        th = load_config(self.E5_LIVE)["thresholds"]

        def v(d1, ci1, d2=0.0, ci2=(-0.05, 0.05)):
            est = {"none_minus_cleared|stop": d1, "not_cleared_minus_cleared|stop": d2}
            ci = {"none_minus_cleared|stop": ci1, "not_cleared_minus_cleared|stop": ci2}
            return verdicts_e5(est, ci, th)
        self.assertEqual(v(0.6, (0.45, 0.75), 0.6, (0.45, 0.75)), {"primary": "CONFIRMED", "secondary": "CLEARING_SPECIFIC"})
        self.assertEqual(v(0.6, (0.45, 0.75)), {"primary": "CONFIRMED", "secondary": "EXPOSURE_GENERAL"})
        self.assertEqual(v(0.0, (-0.1, 0.1)), {"primary": "NOT_CONFIRMED", "secondary": "NOT_APPLICABLE"})
        self.assertEqual(v(0.2, (0.05, 0.35))["primary"], "INCONCLUSIVE")

    def test_small_mock_run_and_gating(self):
        cfg = load_config(DIR / "configs" / "mock_e5_clear_learner.json")
        cfg.update(runs_per_cell=4, bootstrap_reps=100, workers=2)
        with tempfile.TemporaryDirectory() as tmp:
            s = run(cfg, Path(tmp) / "r", live=False)
        self.assertEqual((s["design"], s["cost"]["runs_recorded"]), ("E5", 12))
        live = load_config(self.E5_LIVE)
        self.assertEqual(cells_for(live), [("control", "primed", p) for p in ("none", "cleared", "not_cleared")])
        self.assertLessEqual(live["max_equiv_usd"], 1.5)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                make_transport(live, Path(tmp), live=False)
            with self.assertRaises(RuntimeError):
                make_transport(dict(live, max_equiv_usd=0.0), Path(tmp), live=True)


class TestStudyH1(unittest.TestCase):
    """Study H1: does tool withdrawal carry over to a tool that works? (PROTOCOL_H1.md)"""
    LIVE = [DIR / "configs" / "live_h1_gpt_oss_120b.json", DIR / "configs" / "live_h1_gpt6luna.json"]

    def test_schedules_and_env(self):
        from causetest.h1 import N_TEST, N_TRAIN, ScheduledToolEnv, TRAINING, schedule_for
        for cond, cell in TRAINING.items():
            s = schedule_for(cond)
            self.assertEqual((len(s), s[:N_TRAIN], s[N_TRAIN:]), (12, [cell] * N_TRAIN, [("neutral", "none")] * N_TEST))
        # controllable and uncontrollable show the same message; only the fault differs
        self.assertEqual(TRAINING["controllable"][0], TRAINING["uncontrollable"][0])
        w = make_world(20261901, 12)
        given = lambda i: "CALL stock_lookup " + json.dumps({"site": w.tasks[i].depot, "sku": w.tasks[i].sku.lower()})
        out = []
        run_episode(_Replay([given(0)] * 6 + ["ANSWER UNKNOWN"] + ["ANSWER UNKNOWN"] * 7 + [given(8), "ANSWER 1"]),
                    w, ScheduledToolEnv(w, schedule_for("uncontrollable")), out, lambda: 0.0, lambda r, m: None,
                    lambda e: None)
        self.assertEqual(out[0]["summary"]["failures"], 6)  # the permanent fault: nothing works in training
        self.assertEqual([t["kind"] for t in out], ["train"] * 8 + ["test"] * 4)
        self.assertEqual(out[1]["summary"]["calls"], 0)  # answered without calling: withdrawal
        self.assertTrue(out[8]["summary"]["success"])  # the test block's tool works as written
        with self.assertRaises(ValueError):
            schedule_for("controllable", 6)

    def test_measures_and_rule(self):
        from causetest.h1 import contrasts_h1, verdicts_h1
        th = load_config(self.LIVE[0])["thresholds"]

        def stats(test_nc, train_success=0.9):
            return [{"test_no_call": test_nc, "test_success": 1 - test_nc, "train_late_no_call": test_nc,
                     "train_success": train_success}] * 3
        st = {("control", "helpless", "no_failure"): stats(0.0), ("control", "helpless", "controllable"): stats(0.1),
              ("control", "helpless", "uncontrollable"): stats(0.6, 0.0),
              ("control", "helpless", "uncontrollable_temporary"): stats(0.7, 0.0)}
        c = contrasts_h1(st)
        self.assertAlmostEqual(c["uncontrollable_minus_no_failure|test_no_call"], 0.6)
        self.assertAlmostEqual(c["uncontrollable_minus_controllable|test_no_call"], 0.5)
        self.assertAlmostEqual(c["temporary_minus_uncontrollable|test_no_call"], 0.1)
        ci = {k: (v - 0.1, v + 0.1) for k, v in c.items()}
        per = {"controllable": {"train_success": 0.9}}
        self.assertEqual(verdicts_h1(c, ci, per, th), {"primary": "CARRYOVER", "secondary": "CONTROLLABILITY_MATTERS"})
        self.assertEqual(verdicts_h1(c, ci, {"controllable": {"train_success": 0.2}}, th)["secondary"],
                         "NOT_APPLICABLE_CONTROLLABLE_FAILED")
        flat = {k: 0.0 for k in c}
        self.assertEqual(verdicts_h1(flat, {k: (-0.05, 0.05) for k in c}, per, th),
                         {"primary": "NO_CARRYOVER", "secondary": "NOT_APPLICABLE"})

    def test_withdrawal_mock_and_gating(self):
        cfg = load_config(DIR / "configs" / "mock_h1_helpless.json")
        cfg.update(runs_per_cell=4, bootstrap_reps=100, workers=2)
        with tempfile.TemporaryDirectory() as tmp:
            s = run(cfg, Path(tmp) / "r", live=False)
        self.assertEqual((s["design"], s["cost"]["runs_recorded"]), ("H1", 16))
        self.assertGreater(s["per_condition"]["uncontrollable"]["test_no_call"],
                           s["per_condition"]["no_failure"]["test_no_call"])
        for path in self.LIVE:
            live = load_config(path)
            self.assertEqual(cells_for(live), [("control", "helpless", c) for c in
                                               ("no_failure", "controllable", "uncontrollable", "uncontrollable_temporary")])
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    make_transport(live, Path(tmp), live=False)
                with self.assertRaises(RuntimeError):
                    make_transport(dict(live, max_equiv_usd=0.0), Path(tmp), live=True)


class TestStudyW2B(unittest.TestCase):
    """Study W2-B: E3's bounded caution on the open-weight panel (PROTOCOL_W2B.md)."""

    def test_configs(self):
        paths = sorted((DIR / "configs").glob("live_w2b_*.json"))
        self.assertEqual(len(paths), 5)
        for path in paths:
            cfg = load_config(path)
            src = load_config(DIR / "configs" / cfg["cost_note"].split("Settings as ")[1].split(".json")[0].strip()
                              .__add__(".json"))
            for k in ("transport", "model", "request_options", "provider", "expected_host"):
                self.assertEqual(cfg[k], src[k], f"{path.name}: {k} differs from its C4 arm")
            self.assertEqual((cfg["design"], len(cells_for(cfg))), ("E3", 12))
            self.assertEqual({c[0] for c in cells_for(cfg)}, {"control", "caution", "caution_bounded"})
            self.assertLessEqual(cfg["max_equiv_usd"], cfg["planning"]["proposed_cap_usd"])
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    make_transport(cfg, Path(tmp), live=False)
                with self.assertRaises(RuntimeError):
                    make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)


class TestStudyW6(unittest.TestCase):
    """Study W6: three wordings of the bounded caution (PROTOCOL_W6.md)."""

    def test_wording(self):
        from causetest.e2 import BOUND_FEW, BOUND_FEW_PLAIN, CAUTION, system_for
        self.assertEqual(BOUND_FEW_PLAIN, BOUND_FEW.replace(" different", ""))  # the minimal pair
        self.assertIn(f"\n\nErrors\n- {CAUTION}\n- {BOUND_FEW_PLAIN}\n\nDepot directory:", system_for(W, "caution_few"))
        self.assertNotIn(BOUND_FEW_PLAIN, system_for(W, "caution_bounded"))

    def test_configs(self):
        paths = sorted((DIR / "configs").glob("live_w6_*.json"))
        self.assertEqual(len(paths), 5)
        for path in paths:
            cfg = load_config(path)
            src = load_config(DIR / "configs" / cfg["cost_note"].split("Settings as ")[1].split(".json")[0].strip()
                              .__add__(".json"))
            for k in ("transport", "model", "request_options", "provider", "expected_host"):
                self.assertEqual(cfg.get(k), src.get(k), f"{path.name}: {k} differs from its source")
            self.assertEqual((cfg["design"], len(cells_for(cfg))), ("W6", 20))
            self.assertEqual({c[0] for c in cells_for(cfg)},
                             {"control", "caution", "caution_bounded", "caution_few", "caution_three"})
            self.assertEqual((cfg["base_seed"], cfg["dev_seed"]), (20262001, 20262901))  # new seeds, not E3's
            self.assertGreaterEqual(cfg["max_calls"], 600 * 36)  # never cut short by the call cap
            self.assertLessEqual(cfg["max_equiv_usd"], cfg["planning"]["proposed_cap_usd"])
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    make_transport(cfg, Path(tmp), live=False)
                with self.assertRaises(RuntimeError):
                    make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)

    def test_decision_rule(self):
        from causetest.w6 import pair_label, wording_verdict
        th = load_config(DIR / "configs" / "live_w6_qwen3_8_27b_r0.json")["thresholds"]

        def v(r, c, h, r_ci=(0.4, 0.8), c_ci=(2.8, 3.2), h_ci=(-0.05, 0.02)):
            est = {"a|give_up_rescue": r, "a|outage_calls": c, "a|true_temporary_success": h}
            ci = {"a|give_up_rescue": r_ci, "a|outage_calls": c_ci, "a|true_temporary_success": h_ci}
            return wording_verdict("a", est, ci, th)

        self.assertEqual(v(0.6, 3.0, 0.0), "RECOMMENDABLE")
        self.assertEqual(v(0.6, 3.6, 0.0, c_ci=(3.3, 3.9)), "RESCUE_COSTLY")
        self.assertEqual(v(0.6, 3.4, 0.0, c_ci=(3.0, 4.1)), "RESCUE_COSTLY")
        self.assertEqual(v(0.45, 3.0, 0.0), "WEAK_RESCUE")
        self.assertEqual(v(0.9, 3.0, -0.17, h_ci=(-0.29, -0.06)), "HARMS_TRUE_TEMPORARY")
        self.assertEqual(v(0.6, 3.0, -0.17, h_ci=(-0.29, 0.01)), "RECOMMENDABLE")  # harm not shown
        self.assertEqual(pair_label(0.2, (0.05, 0.35)), "DIFFERENT")
        self.assertEqual(pair_label(0.05, (-0.1, 0.2)), "SAME")
        self.assertEqual(pair_label(0.1, (-0.1, 0.3)), "UNCLEAR")


class TestAnthropicTransport(unittest.TestCase):
    """Paper plan W2: the Anthropic Messages transport translates tool use both ways, sends no sampling parameters,
    and retries only unbilled failures. Every test answers from a fake server; nothing is sent."""
    OPTS = {"max_tokens": 2000, "thinking": {"type": "disabled"}}
    PRICES = {"input": 0.10, "output": 0.50}

    @staticmethod
    def _server(sent, headers_seen=None, thinking=False, extra_call=False):
        """A tool call (after a thinking block, if asked) after each user text; ANSWER UNKNOWN after a result."""
        import io
        n = [0]

        class Resp(io.BytesIO):
            headers = {"request-id": "req_test"}

        def urlopen(req, timeout=None, context=None):
            body = json.loads(req.data.decode())
            sent.append(body)
            if headers_seen is not None:
                headers_seen.append({k.lower(): v for k, v in req.header_items()})
            n[0] += 1
            last = body["messages"][-1]["content"]
            if last[-1]["type"] == "text":
                content = [{"type": "thinking", "thinking": "", "signature": "sig"}] if thinking else []
                content += [{"type": "text", "text": "Checking."},
                            {"type": "tool_use", "id": f"toolu_{n[0]}", "name": "stock_lookup",
                             "input": {"site": "Penrith", "sku": "wm-9610"}}]
                if extra_call:
                    content.append({"type": "tool_use", "id": f"toolu_x{n[0]}", "name": "stock_lookup",
                                    "input": {"site": "Albury", "sku": "wm-9610"}})
                stop = "tool_use"
            else:
                content, stop = [{"type": "text", "text": "ANSWER UNKNOWN"}], "end_turn"
            payload = {"id": f"msg_{n[0]}", "model": body["model"], "content": content, "stop_reason": stop,
                       "usage": {"input_tokens": 1000, "output_tokens": 20}}
            return Resp(json.dumps(payload).encode())
        return urlopen

    def test_translation_both_ways(self):
        from unittest import mock
        from causetest.transports import AnthropicNativeTransport
        sent, heads = [], []
        conv = AnthropicNativeTransport("claude-haiku-5-5", self.OPTS, self.PRICES).open("k", "sys")
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                mock.patch("urllib.request.urlopen", self._server(sent, heads)):
            reply, meta = conv.say("New request: one")
            self.assertEqual(reply, 'CALL stock_lookup {"site": "Penrith", "sku": "wm-9610"}')
            self.assertEqual(parse_reply(reply)["kind"], "call")
            self.assertEqual((heads[0]["anthropic-version"], heads[0]["x-api-key"]), ("2026-10-21", "test-key"))
            b = sent[0]
            self.assertEqual((b["system"], b["tool_choice"]),
                             ("sys", {"type": "auto", "disable_parallel_tool_use": True}))
            self.assertEqual(b["tools"][0]["input_schema"]["required"], ["site", "sku"])
            self.assertTrue(b["tools"][0]["strict"])
            self.assertFalse({"temperature", "top_p", "top_k"} & set(b))
            self.assertEqual((meta["text_with_call"], meta["request_id"]), ("Checking.", "req_test"))
            self.assertAlmostEqual(meta["cost_usd"], (1000 * 0.10 + 20 * 0.50) / 1e6)
            reply, _ = conv.say("RESULT stock_lookup: ERROR: temporary service problem.")
            self.assertEqual(reply, "ANSWER UNKNOWN")
            self.assertEqual(sent[1]["messages"][-1]["content"],
                             [{"type": "tool_result", "tool_use_id": "toolu_1",
                               "content": "ERROR: temporary service problem."}])
            self.assertEqual(sent[1]["messages"][-2]["content"][0]["text"], "Checking.")  # the turn goes back whole
            conv.say("New request: two")  # returns a call (toolu_3) that the harness never answers...
            conv.say("New request: three")  # ...so its result and the new request share one user message
            self.assertEqual(sent[3]["messages"][-1]["content"],
                             [{"type": "tool_result", "tool_use_id": "toolu_3", "content": NO_CALLS_LEFT},
                              {"type": "text", "text": "New request: three"}])
            roles = [m["role"] for m in sent[3]["messages"]]
            self.assertEqual(roles, ["user", "assistant"] * (len(roles) // 2) + ["user"])  # strictly alternating

    def test_thinking_blocks_and_extra_calls_go_back(self):
        from unittest import mock
        from causetest.transports import AnthropicNativeTransport
        sent = []
        opts = {"max_tokens": 8000, "thinking": {"type": "adaptive"}, "output_config": {"effort": "low"}}
        conv = AnthropicNativeTransport("claude-haiku-5-5", opts, self.PRICES).open("k", "sys")
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                mock.patch("urllib.request.urlopen", self._server(sent, thinking=True, extra_call=True)):
            _, meta = conv.say("New request: one")
            self.assertEqual((meta["thinking_blocks"], meta["native_calls"]), (1, 2))
            conv.say("RESULT stock_lookup: 4")
            self.assertEqual(sent[0]["output_config"], {"effort": "low"})
            self.assertEqual(sent[1]["messages"][1]["content"][0]["type"], "thinking")  # unchanged, signature kept
            self.assertEqual(sent[1]["messages"][-1]["content"],
                             [{"type": "tool_result", "tool_use_id": "toolu_1", "content": "4"},
                              {"type": "tool_result", "tool_use_id": "toolu_x1",
                               "content": "Not run: make one call at a time."}])

    def test_refusals_and_retries(self):
        import io
        import urllib.error
        from unittest import mock
        from causetest.transports import AnthropicNativeTransport
        with self.assertRaises(ValueError):
            AnthropicNativeTransport("m", dict(self.OPTS, temperature=1.0), self.PRICES)  # 2026-10-21 rejects it
        with self.assertRaises(ValueError):
            AnthropicNativeTransport("m", {"thinking": {"type": "disabled"}}, self.PRICES)  # no max_tokens
        conv = AnthropicNativeTransport("m", self.OPTS, self.PRICES).open("k", "sys")
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": ""}), self.assertRaises(RuntimeError):
            conv.say("New request: one")  # no key: nothing sent

        def error(code):
            return urllib.error.HTTPError("u", code, "x", {}, io.BytesIO(b'{"error": "test-key bad"}'))
        ok = self._server([])
        calls = [0]

        def flaky(req, timeout=None, context=None):
            calls[0] += 1
            if calls[0] <= 2:
                raise error(529 if calls[0] == 1 else 429)
            return ok(req, timeout, context)
        conv = AnthropicNativeTransport("m", self.OPTS, self.PRICES).open("k", "sys")
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}), mock.patch("time.sleep"), \
                mock.patch("urllib.request.urlopen", flaky):
            _, meta = conv.say("New request: one")
        self.assertEqual((meta["overloaded_retries"], meta["rate_limit_retries"]), (1, 1))
        conv = AnthropicNativeTransport("m", self.OPTS, self.PRICES).open("k", "sys")
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                mock.patch("urllib.request.urlopen", side_effect=error(400)), self.assertRaises(RuntimeError) as ctx:
            conv.say("New request: one")
        self.assertNotIn("test-key", str(ctx.exception))  # the key is redacted from error text

    def test_gated_and_native_prompt(self):
        from causetest.runner import NATIVE_TRANSPORTS
        cfg = {"transport": "anthropic_messages_native", "model": "claude-haiku-5-5", "request_options": self.OPTS,
               "prices_usd_per_mtok": self.PRICES, "max_equiv_usd": 1.0}
        self.assertIn("anthropic_messages_native", NATIVE_TRANSPORTS)  # the instructions point to native calls
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                make_transport(cfg, Path(tmp), live=False)
            with self.assertRaises(RuntimeError):
                make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)
            self.assertEqual(make_transport(cfg, Path(tmp), live=True).label, "anthropic_messages_native")

class TestStudyW2C(unittest.TestCase):
    """Study W2-C: Claude Haiku 5.5 through native tool use (PROTOCOL_W2C.md)."""
    SOURCES = {"c4": "live_n1_c4_native_low.json", "e5": "live_n1_e5_native_low.json",
               "w6": "live_w6_gpt6luna_native_low.json"}

    def test_configs(self):
        from causetest.transports import AnthropicNativeTransport
        paths = sorted((DIR / "configs").glob("live_w2c_*.json"))
        self.assertEqual([p.stem for p in paths], [f"live_w2c_{d}_haiku_{a}" for d in ("c4", "e5", "w6")
                                                   for a in ("t0", "t1")])
        caps = 0.0
        for path in paths:
            cfg = load_config(path)
            design, arm = path.stem.split("_")[2], path.stem.split("_")[-1]
            src = load_config(DIR / "configs" / self.SOURCES[design])
            for k in ("design", "cells", "n_tasks", "base_seed", "dev_seed", "runs_per_cell", "thresholds",
                      "bootstrap_seed", "bootstrap_reps"):
                self.assertEqual(cfg.get(k), src.get(k), f"{path.name}: {k} differs from {self.SOURCES[design]}")
            self.assertEqual((cfg["transport"], cfg["model"]), ("anthropic_messages_native", "claude-haiku-5-5"))
            opts = cfg["request_options"]
            self.assertEqual(opts["thinking"], {"type": "disabled"} if arm == "t0" else {"type": "adaptive"})
            self.assertEqual(opts["max_tokens"], 2000 if arm == "t0" else 8000)
            self.assertEqual(set(opts), {"max_tokens", "thinking", "cache_control"})  # default effort, no sampling
            AnthropicNativeTransport(cfg["model"], opts, cfg["prices_usd_per_mtok"])  # accepted by the transport
            self.assertGreaterEqual(cfg["max_calls"], len(cells_for(cfg)) * cfg["runs_per_cell"] * cfg.get("n_tasks", 6) * 6)
            self.assertLessEqual(cfg["max_equiv_usd"], cfg["planning"]["proposed_cap_usd"])
            caps += cfg["planning"]["proposed_cap_usd"]
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    make_transport(cfg, Path(tmp), live=False)
                with self.assertRaises(RuntimeError):
                    make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)
        self.assertLessEqual(round(caps, 2), 10.0)  # the owner's approval: $10 for the whole study

class TestStudyW5(unittest.TestCase):
    """Study W5: Luna's reasoning effort through native calls (PROTOCOL_W5.md)."""

    def test_configs(self):
        paths = sorted((DIR / "configs").glob("live_w5_*.json"))
        self.assertEqual([p.stem for p in paths], ["live_w5_c4_high", "live_w5_c4_low", "live_w5_c4_medium",
                                                   "live_w5_e5_high", "live_w5_e5_low", "live_w5_e5_medium",
                                                   "live_w5_e5_none"])
        none = load_config(DIR / "configs" / "live_n1_c4_native_none.json")["request_options"]
        for path in paths:
            cfg = load_config(path)
            design, effort = path.stem.split("_")[2:]
            src = load_config(DIR / "configs" / f"live_n1_{design}_native_low.json")
            for k in ("transport", "model", "cells", "design", "n_tasks", "base_seed", "dev_seed", "runs_per_cell",
                      "thresholds", "prices_usd_per_mtok", "bootstrap_seed", "bootstrap_reps"):
                self.assertEqual(cfg.get(k), src.get(k), f"{path.name}: {k} differs from N1")  # N1's worlds and rules
            opts = cfg["request_options"]
            if effort == "none":
                self.assertEqual(opts, none)  # N1-C's settings
            else:
                self.assertEqual(opts["reasoning"], {"effort": effort})
                self.assertNotIn("temperature", opts)
                self.assertEqual(opts["max_output_tokens"], 2000 if effort == "low" else 8000)
            self.assertGreaterEqual(cfg["max_calls"], len(cells_for(cfg)) * cfg["runs_per_cell"] * cfg.get("n_tasks", 6) * 6)
            self.assertLessEqual(cfg["max_equiv_usd"], cfg["planning"]["proposed_cap_usd"])
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    make_transport(cfg, Path(tmp), live=False)
                with self.assertRaises(RuntimeError):
                    make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)


class TestStudyW2D(unittest.TestCase):
    """Study W2-D: GPT-6.1 Sol through native tool calls (PROTOCOL_W2D.md)."""
    SOURCES = TestStudyW2C.SOURCES
    PRICES = {"input": 2.0, "cached_input": 0.10, "cache_write": 2.50, "output": 10.0}

    def test_configs(self):
        paths = sorted((DIR / "configs").glob("live_w2d_*.json"))
        self.assertEqual([p.stem for p in paths], ["live_w2d_c4_sol_high", "live_w2d_c4_sol_low", "live_w2d_e5_sol_high",
                                                   "live_w2d_e5_sol_low", "live_w2d_w6_sol_low"])
        caps = 0.0
        for path in paths:
            cfg = load_config(path)
            design, arm = path.stem.split("_")[2], path.stem.split("_")[-1]
            src = load_config(DIR / "configs" / self.SOURCES[design])
            for k in ("design", "cells", "n_tasks", "base_seed", "dev_seed", "runs_per_cell", "thresholds",
                      "bootstrap_seed", "bootstrap_reps", "transport"):
                self.assertEqual(cfg.get(k), src.get(k), f"{path.name}: {k} differs from {self.SOURCES[design]}")
            self.assertEqual(cfg["model"], "gpt-6.1-sol")
            self.assertEqual({k: v for k, v in cfg["prices_usd_per_mtok"].items() if k != "source"}, self.PRICES)
            opts = cfg["request_options"]
            self.assertEqual(opts, {"max_output_tokens": 2000 if arm == "low" else 8000, "reasoning": {"effort": arm}})
            if arm == "low":  # the same request as Luna's, apart from the model
                self.assertEqual(opts, src["request_options"])
            self.assertGreaterEqual(cfg["max_calls"], len(cells_for(cfg)) * cfg["runs_per_cell"] * cfg.get("n_tasks", 6) * 6)
            self.assertLessEqual(cfg["max_equiv_usd"], cfg["planning"]["proposed_cap_usd"])
            caps += cfg["planning"]["proposed_cap_usd"]
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    make_transport(cfg, Path(tmp), live=False)
                with self.assertRaises(RuntimeError):
                    make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)
        self.assertLessEqual(round(caps, 2), 80.0)  # the owner's approval: $80 in all, pilots included

    def test_cache_pricing(self):
        from causetest.transports import OpenAINativeTransport
        usage = {"input_tokens": 10_000, "output_tokens": 100,
                 "input_tokens_details": {"cached_tokens": 6_000, "cache_write_tokens": 1_000}}
        sol = OpenAINativeTransport("m", {}, self.PRICES)
        self.assertAlmostEqual(sol.cost(usage), (3_000 * 2.0 + 6_000 * 0.10 + 1_000 * 2.50 + 100 * 10.0) / 1e6)
        luna = OpenAINativeTransport("m", {}, {"input": 0.1, "cached_input": 0.01, "output": 0.5})
        self.assertAlmostEqual(luna.cost(usage), (10_000 * 0.1 + 100 * 0.5) / 1e6)  # earlier runs: unchanged

    def test_retries(self):
        import io
        import urllib.error
        from unittest import mock
        from causetest.transports import OpenAINativeTransport
        answer = {"id": "resp_1", "model": "gpt-6.1-sol", "status": "completed",
                  "output": [{"type": "message", "content": [{"type": "output_text", "text": "ANSWER UNKNOWN"}]}],
                  "usage": {"input_tokens": 10, "output_tokens": 2}}

        def error(code, body=b'{"error": "test-key slow down"}'):
            return urllib.error.HTTPError("u", code, "x", {}, io.BytesIO(body))
        calls = [0]

        def flaky(req, timeout=None, context=None):
            calls[0] += 1
            if calls[0] <= 2:
                raise error(429 if calls[0] == 1 else 503)
            return io.BytesIO(json.dumps(answer).encode())
        conv = OpenAINativeTransport("m", {}, self.PRICES).open("k", "sys")
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), mock.patch("time.sleep"), \
                mock.patch("urllib.request.urlopen", flaky):
            reply, meta = conv.say("New request: one")
        self.assertEqual(reply, "ANSWER UNKNOWN")
        self.assertEqual((meta["rate_limit_retries"], meta["server_retries"]), (1, 1))
        self.assertEqual((meta["response_id"], meta["served_model"]), ("resp_1", "gpt-6.1-sol"))
        for exc in (error(429, b'{"error": {"code": "insufficient_quota", "key": "test-key"}}'), error(400)):
            conv = OpenAINativeTransport("m", {}, self.PRICES).open("k", "sys")
            with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), mock.patch("time.sleep") as slept, \
                    mock.patch("urllib.request.urlopen", side_effect=exc), self.assertRaises(RuntimeError) as ctx:
                conv.say("New request: one")
            slept.assert_not_called()  # exhausted quota and client errors are not retried
            self.assertNotIn("test-key", str(ctx.exception))  # the key is redacted from error text


class TestStudyR1(unittest.TestCase):
    """Study R1: recovery times drawn per request, and the stopping rule against a retry in code (PROTOCOL_R1.md)."""

    def test_schedule(self):
        from causetest.r1 import RECOVERY_FAILURES, schedule_for
        for seed in range(20262101, 20262131):
            s = schedule_for(seed, 6)
            self.assertEqual(s, schedule_for(seed, 6))  # the seed alone decides it, so every arm and cell shares it
            self.assertEqual(len(s), 6)
            self.assertEqual(set(s), set(RECOVERY_FAILURES))  # every run meets every recovery time
        with self.assertRaises(ValueError):
            schedule_for(20262101, 3)

    def test_recovery_and_code_retry(self):
        from causetest.r1 import RecoveryToolEnv
        env = RecoveryToolEnv(W, "permanent", "transient", [3, 1, 2, 4, 1, 2])
        self.assertEqual(env.start_task(0), {"recovery_failures": 3})
        self.assertEqual([env.call(i, _args())[0] for i in range(4)], [False, False, False, True])  # clears on call 4
        env.start_task(1)  # the count starts again with each request
        self.assertEqual([env.call(i, _args())[0] for i in range(2)], [False, True])
        env.start_task(2)
        self.assertFalse(env.call(0, _args(site="Nowhere"))[0])  # an unresolvable call counts, and never works
        self.assertFalse(env.call(1, _args())[0])
        self.assertTrue(env.call(2, _args())[0])
        outage = RecoveryToolEnv(W, "permanent", "permanent", [1] * 6)
        outage.start_task(0)
        self.assertEqual(outage.call(5, _args())[:2], (False, CLAIM_TEXT["permanent"]))
        code = RecoveryToolEnv(W, "transient", "transient", [4, 1, 2, 3, 1, 2], attempts=3)
        code.start_task(0)
        ok, text, info = code.call(0, _args())
        self.assertEqual((ok, text, info["service_calls"]), (False, CLAIM_TEXT["transient"], 3))  # one result shown
        ok, _, info = code.call(1, _args())
        self.assertEqual((ok, info["service_calls_before"], info["service_calls"]), (True, 3, 2))  # works on call 5
        code.start_task(1)
        self.assertEqual(code.call(0, _args())[2]["service_calls"], 2)  # stops retrying once a call works
        with self.assertRaises(ValueError):
            RecoveryToolEnv(W, "unknown", "transient", [1] * 6)

    def test_wording(self):
        from causetest.e2 import BOUND_THREE, CAUTION, system_for
        self.assertIn(f"\n\nErrors\n- {BOUND_THREE}\n\nDepot directory:", system_for(W, "three_only"))
        self.assertNotIn(CAUTION, system_for(W, "three_only"))
        self.assertEqual(system_for(W, "code_retry", native=True), system_for(W, "control", native=True))  # unseen

    def test_configs(self):
        paths = sorted((DIR / "configs").glob("live_r1_*.json"))
        self.assertEqual([p.stem for p in paths], ["live_r1_deepseek_r0", "live_r1_haiku_t0", "live_r1_luna_low",
                                                   "live_r1_sol_low"])
        others = [load_config(p) for p in (DIR / "configs").glob("*.json") if "_r1_" not in p.name]
        caps = {p.stem: load_config(p)["max_equiv_usd"] for p in paths}
        self.assertLessEqual(round(sum(caps.values()), 2), 22.50)  # the owner's approval of 2026-10-29
        self.assertLessEqual(caps["live_r1_sol_low"] + caps["live_r1_luna_low"], 34.17)  # OpenAI credit left that day
        for path in paths:
            cfg = load_config(path)
            src_name = cfg["cost_note"].split("Settings as ")[1].split(".json")[0] + ".json"
            src = load_config(DIR / "configs" / src_name)
            self.assertEqual(src["design"], "W6")
            for k in ("transport", "model", "request_options", "prices_usd_per_mtok", "provider", "expected_host",
                      "timeout_seconds", "pass_reasoning_back", "worst_case_usd_per_call"):
                self.assertEqual(cfg.get(k), src.get(k), f"{path.name}: {k} differs from {src_name}")
            self.assertEqual({k: v for k, v in cfg["thresholds"].items() if not k.startswith("r1_")}, src["thresholds"])
            self.assertEqual((cfg["design"], len(cells_for(cfg))), ("R1", 15))
            self.assertEqual({c[0] for c in cells_for(cfg)},
                             {"control", "caution", "caution_three", "three_only", "code_retry"})
            self.assertEqual((cfg["base_seed"], cfg["dev_seed"]), (20262101, 20262911))
            for o in others:  # new seeds: no earlier study's worlds
                self.assertFalse(o["base_seed"] <= cfg["base_seed"] < o["base_seed"] + 60, o["run_name"])
                self.assertNotEqual(o.get("dev_seed"), cfg["dev_seed"], o["run_name"])
            self.assertGreaterEqual(cfg["max_calls"], len(cells_for(cfg)) * cfg["runs_per_cell"] * 36)
            self.assertLessEqual(cfg["max_equiv_usd"], cfg["planning"]["proposed_cap_usd"])
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    make_transport(cfg, Path(tmp), live=False)
                with self.assertRaises(RuntimeError):
                    make_transport(dict(cfg, max_equiv_usd=0.0), Path(tmp), live=True)

    def test_run_records_recovery_and_service_calls(self):
        from causetest.r1 import schedule_for, service_calls
        cfg = dict(load_config(DIR / "configs" / "mock_r1_counts.json"), runs_per_cell=2)
        with tempfile.TemporaryDirectory() as tmp:
            s = run(cfg, Path(tmp) / "r1", live=False)
            rows = [json.loads(x) for x in (Path(tmp) / "r1" / "results.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual((s["design"], len(rows)), ("R1", 30))
        for r in rows:
            self.assertEqual([t["recovery_failures"] for t in r["tasks"]], schedule_for(r["seed"], 6))
            agent_calls = sum(t["summary"]["calls"] for t in r["tasks"])
            served = sum(service_calls(t) for t in r["tasks"])
            if r["arm"] == "code_retry":
                self.assertGreater(served, agent_calls)
            else:
                self.assertEqual(served, agent_calls)

    def test_decision_rule(self):
        from causetest.r1 import calls_label, primary_verdict
        th = load_config(DIR / "configs" / "live_r1_luna_low.json")["thresholds"]

        def v(g, t, c, lg="SAME", lt="SAME", lc="SAME"):
            est = {"instruction_vs_code|give_up_trap": g, "instruction_vs_code|true_temporary": t,
                   "instruction_vs_code|outage_calls": c}
            return primary_verdict(est, {"give_up_trap": lg, "true_temporary": lt, "outage_calls": lc})

        self.assertEqual(v(0.0, 0.0, 0.0), "MATCHES_CODE")
        self.assertEqual(v(0.3, -0.4, 0.0, "DIFFERENT", "DIFFERENT"), "WORSE_THAN_CODE")  # a loss comes first
        self.assertEqual(v(-0.4, 0.0, -1.0, "DIFFERENT", lc="DIFFERENT"), "WORSE_THAN_CODE")
        self.assertEqual(v(0.4, 0.0, 1.5, "DIFFERENT", lc="DIFFERENT"), "COSTLIER_THAN_CODE")
        self.assertEqual(v(0.4, 0.0, 0.1, "DIFFERENT"), "BETTER_THAN_CODE")
        self.assertEqual(v(0.0, 0.0, -0.8, lc="DIFFERENT"), "BETTER_THAN_CODE")
        self.assertEqual(v(0.1, 0.0, 0.0, "UNCLEAR"), "UNCLEAR")
        self.assertEqual(v(0.1, 0.0, 0.0, "NOT_ESTIMABLE"), "NOT_ESTIMABLE")
        self.assertEqual(calls_label(0.3, (-0.5, 0.9), th), "SAME")
        self.assertEqual(calls_label(0.6, (0.1, 1.1), th), "DIFFERENT")
        self.assertEqual(calls_label(0.3, (-0.5, 1.2), th), "UNCLEAR")
        self.assertEqual(calls_label(None, (None, None), th), "NOT_ESTIMABLE")


class TestPanel(unittest.TestCase):
    """The panel table (causetest/panel.py): descriptive, read from committed summaries."""

    def test_wilson(self):
        from causetest.panel import wilson
        lo, hi = wilson(0.0, 30)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.1135, places=3)  # never zero-width at 0
        lo, hi = wilson(0.5, 100)
        self.assertAlmostEqual(lo, 0.4038, places=3)
        self.assertAlmostEqual(hi, 0.5962, places=3)
        with self.assertRaises(ValueError):
            wilson(0.5, 0)

    def test_counts(self):
        from causetest.panel import counts
        c4 = lambda v, rt, gu: {"verdict": v, "retry_trap": {"est": rt}, "give_up_trap": {"est": gu}}
        rows = [{"c4": c4("CONTINUE_CREDULOUS", 0.0, 0.0), "e5": {"verdict": "CONFIRMED"},
                 "bounded": {"est": 0.6, "ci": (0.4, 0.8)}, "three": {"est": 0.6, "ci": (0.25, 0.8)}},
                {"c4": c4("INCONCLUSIVE", 0.2, 0.1), "bounded": None}]
        t = counts(rows)
        self.assertEqual(list(t.values()), [(1, 2), (1, 2), (2, 2), (1, 1), (1, 1), (0, 1)])

    def test_panel_reads_every_arm(self):
        from causetest.panel import ARMS, panel_rows
        rows = panel_rows(DIR / "runs")
        self.assertEqual(len(rows), len(ARMS))
        for (model, setting, src), row in zip(ARMS, rows):
            if (DIR / "runs" / src["c4"] / "analysis" / "summary.json").exists():
                self.assertIn("c4", row, f"{model}, {setting}")
                self.assertTrue(0.0 <= row["c4"]["retry_trap"]["est"] <= 1.0)


if __name__ == "__main__":
    unittest.main()
