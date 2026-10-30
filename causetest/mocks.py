"""Scripted agents (MOCK; instrument validation only, never evidence about a model).

Each reads only what a real agent reads: the system prompt, the requests and the tool results. After
a failure it picks one of three strategies and keeps to it for the rest of the request:

  REFORMAT  try the next SKU spelling it has not tried in this request (stop when none are left)
  RETRY     send the identical call again
  STOP      answer UNKNOWN

With probability `noise`, the first response to a failure is drawn at random instead. With `p_claim`
below 1, a credulous or evidence-learning agent uses its claim-driven plan only with that probability
per request and the message-blind script otherwise (a weaker effect, for power analysis). Random
streams are seeded by the run key.

Kinds:
- credulous: uses the strategy the error text implies (format -> REFORMAT, temporary -> RETRY,
  unavailable -> STOP). On the neutral text it runs `neutral_plan` (default: the message-blind script).
  With `remember_spelling`, it opens each request with the last spelling that worked (credit assignment).
  With `entrench`, its chance of following the claim rises by that much after every request that ended
  without the figure (starting from `p_claim`).
- evidence_learner: starts credulous. A claim whose strategy has left `discredit_after` (default 2)
  requests without the figure is discredited, and the agent tries the other strategies instead (dropping each one that
  fails a request, then stopping). For an "unavailable" claim, which yields no evidence when obeyed,
  it probes once with the blind script after two requests, and keeps or drops the claim by the result.
- message_blind: ignores the text and always runs REFORMAT through the spellings, then one RETRY, then STOP.
- non_engager: answers UNKNOWN without calling.
- format_violator: message_blind, but a share of first replies carry no CALL or ANSWER line.

Extension E2 cues (any kind): with `caution_effect`, `strategy_effect` or `instruction_effect`, the agent
drops its plan for the message-blind script with that chance per request when the cue is present: the
caution or strategy sentence in its system prompt, or the generic instruction in the error text.

Extension E3 cue: with `bound_effect`, when a stopping rule is in the system prompt, the agent stops a
request after `bound_calls` calls (default 3) with that chance per request. Study W6: `bound_calls_by_arm`
sets that number per wording (keyed by the arm whose stopping rule is in the prompt). Study R1: with `bound_claims`,
the rule applies only after those error texts (for instance "permanent", so a true "temporary" is retried on).

Study P1 wording: `claim_texts` maps an exact error text to the claim the agent reads in it, before the keyword
rule. Without it, a reworded "unavailable" with none of the keywords reads as neutral.

Extension E5 experience: with `persist_after_clear`, once the agent has seen an error clear (a success after
a failure, in an earlier request), it drops STOP for the blind script under "unavailable" with that chance.
With `persist_after_failures`, the same happens once it has seen any request with two or more failures.

Study H1 withdrawal: at the start of a request the agent answers UNKNOWN without calling, with chance
`withdraw_p` (default 1), once a trigger from earlier requests holds: `withdraw_after_failed_requests` (that many
requests ended without the figure), `withdraw_after_failed_calls` (that many failed calls in all, fixed or not)
or `withdraw_after_requests` (that many requests seen, whatever happened).
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from typing import Any, Dict, List, Optional, Tuple

from causetest.e2 import BOUNDS, CAUTION, INSTRUCTION, STRATEGY

KINDS = ("credulous", "evidence_learner", "message_blind", "non_engager", "format_violator")
STRATEGIES = ("REFORMAT", "RETRY", "STOP")
IMPLIED = {"format": "REFORMAT", "transient": "RETRY", "permanent": "STOP"}

_TASK = re.compile(r"how many units of (.+?) \(SKU ([^)]+)\) are on hand at the (\w+) depot")


def _h(s: str) -> int:
    return int(hashlib.sha256(s.encode()).hexdigest()[:16], 16)


def claim_of(error_text: str) -> str:
    t = error_text.lower()
    if "not written" in t:
        return "format"
    if "temporary" in t:
        return "transient"
    if "unavailable" in t:
        return "permanent"
    return "neutral"


def spell(given: str, form: str) -> str:
    return {"given": given, "upper": given.upper(), "nohyphen": given.upper().replace("-", ""),
            "lower_nohyphen": given.replace("-", "")}[form]


def make_scripted_agent(kind: str, params: Dict[str, Any], conv_key: str, system: str,
                        crn_seed: Optional[int] = None) -> "ScriptedAgent":
    if kind not in KINDS:
        raise ValueError(kind)
    return ScriptedAgent(kind, params, conv_key, system)


class ScriptedAgent:
    def __init__(self, kind: str, params: Dict[str, Any], conv_key: str, system: str = ""):
        self.kind, self.p, self.system = kind, params, system
        self.rng = random.Random(_h("mock|" + conv_key))
        self.spellings = ["upper", "nohyphen", "lower_nohyphen"]
        self.rng.shuffle(self.spellings)
        self.claims: Dict[str, Dict[str, Any]] = {}  # evidence_learner state per claim
        self.last_good: Optional[str] = None  # last spelling that worked, for remember_spelling
        self.failed_requests = 0  # requests ended without the figure, for `entrench`
        self.saw_clear = self.saw_persist = False  # E5: an error that cleared; a request with 2+ failures
        self.requests_seen = self.total_failed_calls = 0  # H1: withdrawal triggers
        self.task: Dict[str, Any] = {}
        self.pending = "ANSWER UNKNOWN"

    # ------------------------------------------------------------ helpers

    def _emit(self, reply: str, first: bool = True) -> Tuple[str, Dict[str, Any]]:
        self.pending = reply
        if self.kind == "format_violator" and first and self.rng.random() < self.p.get("p_invalid", 0.3):
            return "Let me look into that for you.", {"cost_usd": 0.0, "scripted": self.kind}
        return reply, {"cost_usd": 0.0, "scripted": self.kind}

    def _call(self, form: str) -> Tuple[str, Dict[str, Any]]:
        t = self.task
        t["calls"] += 1
        t["last_form"] = form
        if form not in t["tried"]:
            t["tried"].append(form)
        return self._emit("CALL stock_lookup " + json.dumps({"site": t["depot"], "sku": spell(t["sku"], form)}))

    def _stop(self) -> Tuple[str, Dict[str, Any]]:
        if not self.task.get("closed"):
            self.failed_requests += 1
        self._close(got_figure=False)
        return self._emit("ANSWER UNKNOWN")

    def _blind_plan(self) -> List[str]:
        return ["REFORMAT", "RETRY", "STOP"]

    def _plan_for(self, claim: str) -> List[str]:
        """The ordered strategies the agent will use in this request, from its first failure on."""
        if self.kind in ("message_blind", "format_violator"):
            return self._blind_plan()
        if claim == "neutral":
            return list(self.p.get("neutral_plan", self._blind_plan()))
        implied = IMPLIED[claim]
        if self.kind == "credulous":
            return [implied]
        st = self.claims.setdefault(claim, {"mode": "follow", "fails": 0, "alts": [s for s in STRATEGIES if s != implied]})
        if st["mode"] == "follow" or st["mode"] == "confirmed":
            return [implied]
        if st["mode"] == "probe":
            return self._blind_plan()
        return st["alts"][:1] or ["STOP"]

    def _close(self, got_figure: bool) -> None:
        """Update evidence at the end of a request (evidence_learner only)."""
        t = self.task
        if self.kind != "evidence_learner" or t.get("closed") or t.get("claim") in (None, "neutral"):
            t["closed"] = True
            return
        t["closed"] = True
        st = self.claims[t["claim"]]
        if st["mode"] == "follow" and not got_figure:
            st["fails"] += 1
            if st["fails"] >= self.p.get("discredit_after", 2):
                st["mode"] = "probe" if IMPLIED[t["claim"]] == "STOP" else "discredited"
        elif st["mode"] == "probe":
            st["mode"] = "discredited" if got_figure else "confirmed"
            if got_figure:
                st["alts"] = ["REFORMAT", "RETRY"]
        elif st["mode"] == "discredited" and not got_figure and st["alts"]:
            st["alts"].pop(0)

    def _cue_effect(self, body: str) -> float:
        """Extension E2: the chance of dropping the plan for the blind script, from the cues present."""
        p = 0.0
        if CAUTION in self.system:
            p = max(p, self.p.get("caution_effect", 0.0))
        if STRATEGY in self.system:
            p = max(p, self.p.get("strategy_effect", 0.0))
        if INSTRUCTION in body:
            p = max(p, self.p.get("instruction_effect", 0.0))
        return p

    def _claim(self, body: str) -> str:
        """The claim the agent reads in an error text: study P1's `claim_texts` first, then the keywords."""
        return self.p.get("claim_texts", {}).get(body, claim_of(body))

    def _withdraws(self) -> bool:
        """H1: answer without calling, from experience in earlier requests only. No draw unless a trigger holds."""
        p = self.p
        triggered = ((p.get("withdraw_after_failed_requests") is not None
                      and self.failed_requests >= p["withdraw_after_failed_requests"])
                     or (p.get("withdraw_after_failed_calls") is not None
                         and self.total_failed_calls >= p["withdraw_after_failed_calls"])
                     or (p.get("withdraw_after_requests") is not None
                         and self.requests_seen > p["withdraw_after_requests"]))
        return bool(triggered) and self.rng.random() < p.get("withdraw_p", 1.0)

    # ------------------------------------------------------------ turns

    def say(self, text: str) -> Tuple[str, Dict[str, Any]]:
        if text.startswith("New request:"):
            m = _TASK.search(text)
            self.task = {"sku": m.group(2), "depot": m.group(3), "calls": 0, "tried": [], "plan": None, "claim": None}
            if self.kind == "non_engager":
                return self._emit("ANSWER UNKNOWN")
            self.requests_seen += 1
            if self._withdraws():
                return self._stop()
            return self._call(self.last_good if self.p.get("remember_spelling") and self.last_good else "given")
        if text.startswith("RESULT "):
            return self._on_result(text.split(":", 1)[1].strip())
        if text.startswith("Please reply"):
            return self._emit(self.pending, first=False)
        return self._stop()

    def _on_result(self, body: str) -> Tuple[str, Dict[str, Any]]:
        t = self.task
        if not body.startswith("ERROR"):
            self.last_good = t["last_form"]
            self.saw_clear = self.saw_clear or t.get("fails", 0) >= 1
            self._close(got_figure=True)
            return self._emit(f"ANSWER {json.loads(body)['on_hand']}")
        t["fails"] = t.get("fails", 0) + 1
        self.total_failed_calls += 1
        if t["plan"] is None:  # first failure in this request: choose the strategy
            experienced = 0.0  # E5: chance of persisting under "unavailable", from earlier requests only
            if self._claim(body) == "permanent":
                if self.saw_clear:
                    experienced = max(experienced, self.p.get("persist_after_clear", 0.0))
                if self.saw_persist:
                    experienced = max(experienced, self.p.get("persist_after_failures", 0.0))
            t["claim"] = self._claim(body)
            t["plan"] = list(self._plan_for(t["claim"]))
            p_claim = self.p.get("p_claim", 1.0)
            if "entrench" in self.p:  # follows the claim more after every request that ended without the figure
                p_claim = min(1.0, p_claim + self.p["entrench"] * self.failed_requests)
            if self.rng.random() >= p_claim:
                t["plan"] = self._blind_plan()
            cue = self._cue_effect(body)
            if cue and self.rng.random() < cue:  # no draw without a cue, so earlier scripts' streams are unchanged
                t["plan"] = self._blind_plan()
            bound = next((arm for arm, text in BOUNDS.items() if text in self.system), None)
            if "bound_claims" in self.p and t["claim"] not in self.p["bound_claims"]:
                bound = None  # R1: the stopping rule is applied only after these error texts
            if bound and self.p.get("bound_effect") and self.rng.random() < self.p["bound_effect"]:
                # E3: accept the error after this many calls; W6: per wording, from `bound_calls_by_arm`
                t["max_calls"] = self.p.get("bound_calls_by_arm", {}).get(bound, self.p.get("bound_calls", 3))
            if experienced and self.rng.random() < experienced:  # no draw without such experience, as above
                t["plan"] = self._blind_plan()
            if self.rng.random() < self.p.get("noise", 0.1):
                t["plan"] = [self.rng.choice(STRATEGIES)] + [s for s in t["plan"]]
        if t["fails"] >= 2:
            self.saw_persist = True
        if t["calls"] >= t.get("max_calls", 6):
            return self._stop()
        while t["plan"]:
            s = t["plan"][0]
            if s == "STOP":
                return self._stop()
            if s == "RETRY":
                if t.get("retries", 0) < self.p.get("max_retries", 5):
                    t["retries"] = t.get("retries", 0) + 1
                    if len(t["plan"]) > 1:  # in a multi-step script, retry once then move on
                        t["plan"].pop(0)
                    return self._call(t["last_form"])
                t["plan"].pop(0)
                continue
            left = [f for f in self.spellings if f not in t["tried"]]
            if left:
                return self._call(left[0])
            t["plan"].pop(0)
        return self._stop()
