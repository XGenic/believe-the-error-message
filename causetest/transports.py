"""Agent backends. Each opens a conversation with a system prompt and answers one user turn at a time.

- ClaudeCLITransport: headless Claude Code (`claude -p`) with the experiment's system prompt as a
  full replacement, no built-in tools, no settings or MCP servers, run from an empty working
  directory. Turn 1 creates a session; later turns resume it, so the agent sees its own earlier
  replies as real assistant turns.
- OpenAIResponsesTransport: the Responses API; the full history is resent each turn.
- OpenAINativeTransport: the Responses API with native function calling (paper plan W1).
- OpenRouterNativeTransport: OpenRouter's Chat Completions API with native function calling, pinned to
  one host, with OpenRouter's billed cost (paper plan W2, the open-weight models).
- AnthropicNativeTransport: the Anthropic Messages API with native tool use (paper plan W2, the Anthropic models).
- MockTransport: scripted agents (MOCK; instrument validation only), see mocks.py.

Copied from C3 (c3_yoked_helplessness_in_agents/yoketest/transports.py).

The agent only ever receives the system prompt and the user turns.
"""

from __future__ import annotations

import json
import os
import ssl
import subprocess
import threading
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from causetest.mocks import make_scripted_agent
from causetest.protocol import cut_after_first_protocol_line


class SpendCapExceeded(RuntimeError):
    pass


class SpendGuard:
    """Reserves a worst-case cost per call against a hard cap (API-equivalent USD)."""

    def __init__(self, max_usd: float, max_calls: int, worst_case_usd_per_call: float, spent_usd: float = 0.0,
                 calls: int = 0):
        self.max_usd, self.max_calls, self.worst = float(max_usd), int(max_calls), float(worst_case_usd_per_call)
        self.spent_usd, self.reserved_usd, self.calls = spent_usd, 0.0, calls
        self._lock = threading.Lock()

    def reserve(self) -> float:
        with self._lock:
            if self.calls >= self.max_calls:
                raise SpendCapExceeded(f"call cap {self.max_calls} reached")
            if self.spent_usd + self.reserved_usd + self.worst > self.max_usd:
                raise SpendCapExceeded(f"worst case would exceed cap ${self.max_usd:.2f} "
                                       f"(spent ${self.spent_usd:.4f}, reserved ${self.reserved_usd:.4f})")
            self.calls += 1
            self.reserved_usd += self.worst
        return self.worst

    def settle(self, reserved: float, actual: float) -> None:
        with self._lock:
            self.reserved_usd -= reserved
            self.spent_usd += actual


# ---------------------------------------------------------------- Claude CLI


class ClaudeCLITransport:
    label = "claude_cli"
    is_mock = False

    def __init__(self, model: str, subject_cwd: Path, timeout_seconds: int = 240):
        self.model, self.cwd, self.timeout = model, subject_cwd, timeout_seconds
        subject_cwd.mkdir(parents=True, exist_ok=True)

    def open(self, conv_key: str, system: str, crn_seed: Optional[int] = None) -> "ClaudeCLIConversation":
        return ClaudeCLIConversation(self, str(uuid.uuid4()), system)


class ClaudeCLIConversation:
    def __init__(self, transport: ClaudeCLITransport, session_id: str, system: str):
        self.t, self.session_id, self.system, self.turns = transport, session_id, system, 0

    def say(self, text: str) -> Tuple[str, Dict[str, Any]]:
        cmd = ["claude", "-p", "--model", self.t.model, "--system-prompt", self.system, "--tools", "",
               "--strict-mcp-config", "--setting-sources", "", "--output-format", "json"]
        cmd += ["--session-id", self.session_id] if self.turns == 0 else ["--resume", self.session_id]
        started = time.monotonic()
        proc = subprocess.run(cmd + [text], cwd=self.t.cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=self.t.timeout)
        if proc.returncode != 0:
            raise RuntimeError(f"claude exited {proc.returncode}: {(proc.stderr or proc.stdout)[:400]}")
        data = json.loads(proc.stdout)
        if data.get("is_error"):
            raise RuntimeError(f"claude reported an error: {str(data.get('result'))[:400]}")
        self.turns += 1
        meta = {"session_id": self.session_id, "cost_usd": float(data.get("total_cost_usd") or 0.0),
                "usage": data.get("usage"), "model_usage": data.get("modelUsage"),
                "latency_seconds": time.monotonic() - started}
        return data.get("result") or "", meta


# ---------------------------------------------------------------- OpenAI


class OpenAIResponsesTransport:
    label = "openai_responses"
    is_mock = False
    URL = "https://api.openai.com/v1/responses"

    def __init__(self, model: str, options: Dict[str, Any], prices: Dict[str, float], history_cut: bool = False):
        self.model, self.options, self.prices = model, options, prices
        self.history_cut = history_cut  # Luna deviation L1: history keeps each reply only to its first protocol line

    def open(self, conv_key: str, system: str, crn_seed: Optional[int] = None) -> "OpenAIConversation":
        return OpenAIConversation(self, system)


class OpenAIConversation:
    def __init__(self, transport: OpenAIResponsesTransport, system: str):
        self.t = transport
        self.messages: List[Dict[str, str]] = [{"role": "developer", "content": system}]

    def say(self, text: str) -> Tuple[str, Dict[str, Any]]:
        key = os.environ.get("OPENAI_API_KEY", "")
        if not key or not key.isascii() or any(ord(c) <= 32 for c in key):
            raise RuntimeError("OPENAI_API_KEY is missing or malformed; no request was sent")
        self.messages.append({"role": "user", "content": text})
        body = {"model": self.t.model, "input": self.messages, "store": False}
        body.update({k: v for k, v in self.t.options.items() if v is not None})
        req = urllib.request.Request(self.t.URL, data=json.dumps(body).encode(), method="POST",
                                     headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
        started = time.monotonic()
        try:
            with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
                payload = json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:400].replace(key, "[REDACTED]")
            raise RuntimeError(f"HTTP {exc.code} from provider: {detail}") from None
        reply = "".join(c.get("text", "") for item in payload.get("output", []) if item.get("type") == "message"
                        for c in item.get("content", []) if c.get("type") == "output_text")
        shown = cut_after_first_protocol_line(reply) if self.t.history_cut else reply
        self.messages.append({"role": "assistant", "content": shown})
        u = payload.get("usage") or {}
        cost = (u.get("input_tokens", 0) * self.t.prices["input"] + u.get("output_tokens", 0) * self.t.prices["output"]) / 1e6
        meta = {"cost_usd": cost, "usage": u, "latency_seconds": time.monotonic() - started}
        if self.t.history_cut:
            meta["history_reply_cut"] = shown != reply
        return reply, meta


def _openai_post(url: str, body: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key or not key.isascii() or any(ord(c) <= 32 for c in key):
        raise RuntimeError("OPENAI_API_KEY is missing or malformed; no request was sent")
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:400].replace(key, "[REDACTED]")
        raise _OpenAIHTTPError(exc.code, f"HTTP {exc.code} from provider: {detail}") from None
    return payload, time.monotonic() - started


class _OpenAIHTTPError(RuntimeError):
    """An HTTP error from the OpenAI API, its key already redacted. A RuntimeError, as before, for callers that
    do not retry."""

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


class OpenAINativeTransport:
    """The OpenAI Responses API with native function calling (paper plan W1).

    Cost: when the config's prices include `cache_write` (study W2-D on), each response's cached and cache-write
    input tokens are priced at their own rates. Without it, all input is priced at the uncached rate, as in every
    earlier OpenAI run, and the recorded cost is an upper bound."""
    label = "openai_responses_native"
    is_mock = False
    URL = "https://api.openai.com/v1/responses"
    RETRY_WAITS = (2, 4, 8, 16, 30, 30)  # seconds before each retry of an unbilled failure
    RETRY_CODES = {429: "rate_limit", 500: "server", 502: "server", 503: "server", 504: "server"}

    def __init__(self, model: str, options: Dict[str, Any], prices: Dict[str, float]):
        self.model, self.options, self.prices = model, options, prices

    def open(self, conv_key: str, system: str, crn_seed: Optional[int] = None) -> "OpenAINativeConversation":
        return OpenAINativeConversation(self, system)

    def cost(self, usage: Dict[str, Any]) -> float:
        p = self.prices
        inp, out = usage.get("input_tokens", 0), usage.get("output_tokens", 0)
        if "cache_write" not in p:
            return (inp * p["input"] + out * p["output"]) / 1e6
        d = usage.get("input_tokens_details") or {}
        cached, written = d.get("cached_tokens") or 0, d.get("cache_write_tokens") or 0
        return (max(inp - cached - written, 0) * p["input"] + cached * p["cached_input"]
                + written * p["cache_write"] + out * p["output"]) / 1e6

    def post(self, body: Dict[str, Any]) -> Tuple[Dict[str, Any], float, Dict[str, int]]:
        """The response, its latency and the retries by kind. Rate limits (429), server errors (5xx) and socket
        timeouts come back before any output and are retried with backoff and counted; a 429 for exhausted quota
        is not retried. Any other error fails the call."""
        retries = {kind: 0 for kind in ("rate_limit", "server", "timeout")}
        for wait in self.RETRY_WAITS + (None,):
            try:
                payload, latency = _openai_post(self.URL, body)
                return payload, latency, retries
            except _OpenAIHTTPError as exc:
                detail = str(exc)
                if exc.code not in self.RETRY_CODES or "insufficient_quota" in detail:
                    raise RuntimeError(f"{detail} (retries so far: {retries})") from None
                kind = self.RETRY_CODES[exc.code]
            except urllib.error.URLError as exc:  # a socket timeout while connecting arrives wrapped
                if not isinstance(exc.reason, TimeoutError):
                    raise
                kind, detail = "timeout", f"client timeout: {exc.reason}"
            except TimeoutError as exc:
                kind, detail = "timeout", f"client timeout: {exc}"
            if wait is None:
                raise RuntimeError(f"{detail} (retries so far: {retries})")
            retries[kind] += 1
            time.sleep(wait)
        raise AssertionError("unreachable")


class OpenAINativeConversation:
    """The episode still speaks the CALL/ANSWER text protocol, so this conversation translates both ways. A native
    function call from the model becomes the reply line `CALL stock_lookup {...}`. The harness's next message after
    a call (the tool result, or a reminder) goes back as that call's output, not as a user message. Text replies
    pass through unchanged. As in the text transport, reasoning items are not passed back."""

    def __init__(self, transport: OpenAINativeTransport, system: str):
        self.t = transport
        self.items: List[Dict[str, Any]] = [{"role": "developer", "content": system}]
        self.pending: Optional[str] = None  # call_id of the model's last function call, awaiting its output

    def _close_pending(self, output: str) -> None:
        self.items.append({"type": "function_call_output", "call_id": self.pending, "output": output})
        self.pending = None

    def say(self, text: str) -> Tuple[str, Dict[str, Any]]:
        from causetest.protocol import NO_CALLS_LEFT, TOOL, TOOL_SPEC
        prefix = f"RESULT {TOOL}: "
        if self.pending is not None and text.startswith("New request:"):
            self._close_pending(NO_CALLS_LEFT)  # the request ended on protocol limits with a call still open
        if self.pending is not None:
            self._close_pending(text[len(prefix):] if text.startswith(prefix) else text)
        else:
            self.items.append({"role": "user", "content": text})
        body = {"model": self.t.model, "input": self.items, "store": False, "parallel_tool_calls": False,
                "tools": [dict(TOOL_SPEC, type="function", strict=True)]}
        body.update({k: v for k, v in self.t.options.items() if v is not None})
        payload, latency, retries = self.t.post(body)
        output = payload.get("output", [])
        calls = [i for i in output if i.get("type") == "function_call"]
        said = "".join(c.get("text", "") for i in output if i.get("type") == "message"
                       for c in i.get("content", []) if c.get("type") == "output_text")
        u = payload.get("usage") or {}
        meta: Dict[str, Any] = {"cost_usd": self.t.cost(u), "usage": u, "latency_seconds": latency,
                                "native_calls": len(calls)}
        if "cache_write" in self.t.prices:  # W2-D on: the fields W2-C records for the Anthropic runs
            meta.update({"response_id": payload.get("id"), "served_model": payload.get("model"),
                         "status": payload.get("status")})
            meta.update({f"{kind}_retries": n for kind, n in retries.items()})
        if not calls:
            self.items.append({"role": "assistant", "content": said})
            return said, meta
        first = calls[0]
        self.items.append({"type": "function_call", "call_id": first["call_id"], "name": first["name"],
                           "arguments": first["arguments"]})
        self.pending = first["call_id"]
        for extra in calls[1:]:  # parallel calls are switched off; if one slips through, answer it so the history stays valid
            self.items.append({"type": "function_call", "call_id": extra["call_id"], "name": extra["name"],
                               "arguments": extra["arguments"]})
            self.items.append({"type": "function_call_output", "call_id": extra["call_id"],
                               "output": "Not run: make one call at a time."})
        try:
            args = json.dumps(json.loads(first["arguments"]))  # one line, so the episode's parser reads it
        except (TypeError, ValueError):
            args = str(first["arguments"]).replace("\n", " ")
        if said.strip():
            meta["text_with_call"] = said
        return f"CALL {first['name']} {args}", meta


# ---------------------------------------------------------------- OpenRouter


class BilledTransportError(RuntimeError):
    """A failure after the provider billed the call. `meta` carries the billed cost, so the spend guard and the
    journal still count it."""

    def __init__(self, message: str, meta: Dict[str, Any]):
        super().__init__(message)
        self.meta = meta


def openrouter_pin(provider: Dict[str, Any]) -> Dict[str, Any]:
    """The routing block for one pinned host. OpenRouter otherwise routes a model to any of its hosts, which differ
    in quantization, chat template and tool-call parser; a silent switch would be an unrecorded factor."""
    order = provider.get("order") if isinstance(provider, dict) else None
    if not isinstance(order, list) or len(order) != 1 or not isinstance(order[0], str) or not order[0]:
        raise ValueError("provider.order must name exactly one host")
    if provider.get("allow_fallbacks") is True or provider.get("require_parameters") is False:
        raise ValueError("the host pin cannot allow fallbacks or ignore unsupported parameters")
    return dict(provider, allow_fallbacks=False, require_parameters=True)


def _host_key(name: Any) -> str:
    return "".join(c for c in str(name).lower() if c.isalnum())




class OpenRouterNativeTransport:
    """OpenRouter's OpenAI-compatible Chat Completions API with native function calling, pinned to one host
    (paper plan W2: the open-weight models). Cost is OpenRouter's billed figure, not a price-list estimate."""
    label = "openrouter_chat_native"
    is_mock = False
    URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, model: str, provider: Dict[str, Any], options: Dict[str, Any], prices: Dict[str, float],
                 timeout_seconds: int = 180, pass_reasoning_back: bool = False, expected_host: Optional[str] = None,
                 deadline_seconds: float = 60):
        self.model, self.provider, self.options, self.prices = model, openrouter_pin(provider), options, prices
        # The pin may name an endpoint tag ("deepinfra/fp8"); responses name the host ("DeepInfra").
        self.host = expected_host or self.provider["order"][0].split("/")[0]
        self.timeout_seconds, self.pass_reasoning_back = timeout_seconds, pass_reasoning_back
        # Deviation W2-3: OpenRouter keeps a stalled request open with keep-alive whitespace, so the socket timeout
        # never fires and a host can hold a call for 300 s before a 504. A wall-clock deadline cuts it short.
        self.deadline_seconds = deadline_seconds

    def served_by_pin(self, served: Any) -> bool:
        return served is not None and _host_key(served) in (_host_key(self.host),
                                                            _host_key(self.provider["order"][0].split("/")[0]))

    def open(self, conv_key: str, system: str, crn_seed: Optional[int] = None) -> "OpenRouterNativeConversation":
        return OpenRouterNativeConversation(self, system)

    RETRY_WAITS = (2, 4, 8, 16, 30, 30)  # seconds before each retry of a rate limit or a timeout

    def _read(self, resp) -> bytes:
        """The whole body, or TimeoutError once the call has run past the deadline (keep-alive bytes included)."""
        started, chunks = time.monotonic(), []
        while True:
            if time.monotonic() - started > self.deadline_seconds:
                raise TimeoutError(f"no complete response within {self.deadline_seconds} s")
            chunk = resp.read1(65536)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)

    def post(self, body: Dict[str, Any]) -> Tuple[Dict[str, Any], float, Dict[str, int]]:
        """The response, its latency and the retries by kind. Both kinds are retried with backoff and counted:
        - "rate_limit": HTTP 429 (deviation W2-1), a limit before the model ran;
        - "timeout": a host timeout (HTTP 504, or a 504 error inside a 200 response), or no complete response
          within the deadline (deviation W2-3). The stalled call returned nothing, so the agent never saw it.
        Neither is billed. Any other error fails the call as before."""
        key = os.environ.get("OPENROUTER_API_KEY", "")
        if not key or not key.isascii() or any(ord(c) <= 32 for c in key):
            raise RuntimeError("OPENROUTER_API_KEY is missing or malformed; no request was sent")
        ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
        retries = {"rate_limit": 0, "timeout": 0}
        for wait in self.RETRY_WAITS + (None,):
            req = urllib.request.Request(self.URL, data=json.dumps(body).encode(), method="POST",
                                         headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            started = time.monotonic()
            try:
                with urllib.request.urlopen(req, timeout=min(self.timeout_seconds, self.deadline_seconds),
                                            context=ctx) as resp:
                    payload = json.loads(self._read(resp).decode())
                err = payload.get("error") if isinstance(payload.get("error"), dict) else {}
                if err.get("code") != 504 and (err.get("metadata") or {}).get("error_type") != "timeout":
                    return payload, time.monotonic() - started, retries
                kind, detail = "timeout", f"OpenRouter error: {json.dumps(err)[:400]}"
            except urllib.error.HTTPError as exc:
                text = exc.read().decode(errors="replace")[:400].replace(key, "[REDACTED]")
                detail = f"HTTP {exc.code} from OpenRouter: {text}"
                if exc.code not in (429, 504):
                    raise RuntimeError(f"{detail} (retries so far: {retries})") from None
                kind = "rate_limit" if exc.code == 429 else "timeout"
            except urllib.error.URLError as exc:  # a socket timeout while connecting arrives wrapped
                if not isinstance(exc.reason, TimeoutError):
                    raise
                kind, detail = "timeout", f"client timeout: {exc.reason}"
            except TimeoutError as exc:  # the deadline, or a socket timeout while reading
                kind, detail = "timeout", f"client timeout: {exc}"
            if wait is None:
                raise RuntimeError(f"{detail} (retries so far: {retries})")
            retries[kind] += 1
            time.sleep(wait)
        raise AssertionError("unreachable")


class OpenRouterNativeConversation:
    """The same two-way translation as OpenAINativeConversation, in Chat Completions form. A tool call becomes the
    reply line `CALL stock_lookup {...}`; the harness's next message goes back as that call's `tool` message. As in
    the OpenAI transports, the model's text sent alongside a call and its reasoning are not passed back (unless
    `pass_reasoning_back`, for models whose hosts require it in a tool loop)."""

    def __init__(self, transport: OpenRouterNativeTransport, system: str):
        self.t = transport
        self.messages: List[Dict[str, Any]] = [{"role": "system", "content": system}]
        self.pending: Optional[str] = None  # id of the model's last tool call, awaiting its result

    def _close_pending(self, output: str) -> None:
        self.messages.append({"role": "tool", "tool_call_id": self.pending, "content": output})
        self.pending = None

    def _meta(self, payload: Dict[str, Any], latency: float) -> Dict[str, Any]:
        u = payload.get("usage") or {}
        billed = u.get("cost")
        estimate = (u.get("prompt_tokens", 0) * self.t.prices["input"]
                    + u.get("completion_tokens", 0) * self.t.prices["output"]) / 1e6
        return {"cost_usd": float(billed) if isinstance(billed, (int, float)) else estimate,
                "cost_source": "billed" if isinstance(billed, (int, float)) else "price_estimate",
                "usage": u, "latency_seconds": latency, "host": payload.get("provider"),
                "generation_id": payload.get("id"), "served_model": payload.get("model")}

    def say(self, text: str) -> Tuple[str, Dict[str, Any]]:
        from causetest.protocol import NO_CALLS_LEFT, TOOL, TOOL_SPEC
        prefix = f"RESULT {TOOL}: "
        if self.pending is not None and text.startswith("New request:"):
            self._close_pending(NO_CALLS_LEFT)  # the request ended on protocol limits with a call still open
        if self.pending is not None:
            self._close_pending(text[len(prefix):] if text.startswith(prefix) else text)
        else:
            self.messages.append({"role": "user", "content": text})
        body = {"model": self.t.model, "messages": self.messages, "tools": [{"type": "function", "function": TOOL_SPEC}],
                "tool_choice": "auto", "provider": self.t.provider, "usage": {"include": True}}
        # No `parallel_tool_calls`: no open-model host lists it, so with require_parameters it could block routing.
        # Extra calls are answered "Not run" below; a config may still add the parameter in request_options.
        body.update({k: v for k, v in self.t.options.items() if v is not None})
        payload, latency, retries = self.t.post(body)
        if payload.get("error"):  # an upstream failure can arrive with HTTP 200
            raise RuntimeError(f"OpenRouter error: {json.dumps(payload['error'])[:400]}")
        meta = self._meta(payload, latency)
        if not self.t.served_by_pin(meta["host"]):
            raise BilledTransportError(f"served by host {meta['host']!r}, not the pinned {self.t.host!r}", meta)
        choice = (payload.get("choices") or [{}])[0]
        if choice.get("error"):
            raise BilledTransportError(f"OpenRouter choice error: {json.dumps(choice['error'])[:400]}", meta)
        message = choice.get("message") or {}
        calls = message.get("tool_calls") or []
        said = message.get("content") or ""
        meta.update(native_calls=len(calls), finish_reason=choice.get("finish_reason"),
                    native_finish_reason=choice.get("native_finish_reason"), rate_limit_retries=retries["rate_limit"],
                    timeout_retries=retries["timeout"])
        if message.get("reasoning"):
            meta["reasoning_chars"] = len(message["reasoning"])
        if not calls:
            self.messages.append({"role": "assistant", "content": said})
            return said, meta
        turn: Dict[str, Any] = {"role": "assistant", "content": None, "tool_calls": calls}
        if self.t.pass_reasoning_back and message.get("reasoning_details"):
            turn["reasoning_details"] = message["reasoning_details"]
        self.messages.append(turn)
        first = calls[0]
        self.pending = first["id"]
        for extra in calls[1:]:  # parallel calls are switched off; if one slips through, answer it so the history stays valid
            self.messages.append({"role": "tool", "tool_call_id": extra["id"], "content": "Not run: make one call at a time."})
        fn = first.get("function") or {}
        try:
            args = json.dumps(json.loads(fn.get("arguments") or ""))  # one line, so the episode's parser reads it
        except (TypeError, ValueError):
            args = str(fn.get("arguments")).replace("\n", " ")
        if said.strip():
            meta["text_with_call"] = said
        return f"CALL {fn.get('name')} {args}", meta


# ---------------------------------------------------------------- Anthropic


class AnthropicNativeTransport:
    """The Anthropic Messages API with native tool use (paper plan W2: the Anthropic models), raw HTTP on API
    version 2026-10-21, standard library only like the other transports. That version rejects `temperature`,
    `top_p` and `top_k`, so a config that sets one is refused here, before any call. Cost is priced from the
    response's usage at the config's list prices."""
    label = "anthropic_messages_native"
    is_mock = False
    URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2026-10-21"
    SAMPLING = ("temperature", "top_p", "top_k")
    RETRY_WAITS = (2, 4, 8, 16, 30, 30)  # seconds before each retry of an unbilled failure
    RETRY_CODES = {429: "rate_limit", 529: "overloaded", 500: "server", 502: "server", 503: "server", 504: "server"}

    def __init__(self, model: str, options: Dict[str, Any], prices: Dict[str, float], timeout_seconds: int = 120):
        bad = [k for k in self.SAMPLING if k in options]
        if bad:
            raise ValueError(f"API version {self.API_VERSION} rejects {bad}; remove them from request_options")
        if "max_tokens" not in options:
            raise ValueError("request_options must set max_tokens")
        self.model, self.options, self.prices, self.timeout_seconds = model, options, prices, timeout_seconds

    def open(self, conv_key: str, system: str, crn_seed: Optional[int] = None) -> "AnthropicNativeConversation":
        return AnthropicNativeConversation(self, system)

    def post(self, body: Dict[str, Any]) -> Tuple[Dict[str, Any], float, Dict[str, int], Optional[str]]:
        """The response, its latency, the retries by kind and the request id. Rate limits (429), overload (529),
        server errors (5xx) and socket timeouts come back before any output, are not billed, and are retried with
        backoff and counted. Any other error fails the call."""
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key or not key.isascii() or any(ord(c) <= 32 for c in key):
            raise RuntimeError("ANTHROPIC_API_KEY is missing or malformed; no request was sent")
        ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
        retries = {kind: 0 for kind in ("rate_limit", "overloaded", "server", "timeout")}
        for wait in self.RETRY_WAITS + (None,):
            req = urllib.request.Request(self.URL, data=json.dumps(body).encode(), method="POST",
                                         headers={"x-api-key": key, "anthropic-version": self.API_VERSION,
                                                  "content-type": "application/json"})
            started = time.monotonic()
            try:
                with urllib.request.urlopen(req, timeout=self.timeout_seconds, context=ctx) as resp:
                    payload = json.loads(resp.read().decode())
                    request_id = (getattr(resp, "headers", None) or {}).get("request-id")
                return payload, time.monotonic() - started, retries, request_id
            except urllib.error.HTTPError as exc:
                text = exc.read().decode(errors="replace")[:400].replace(key, "[REDACTED]")
                detail = f"HTTP {exc.code} from Anthropic: {text}"
                if exc.code not in self.RETRY_CODES:
                    raise RuntimeError(f"{detail} (retries so far: {retries})") from None
                kind = self.RETRY_CODES[exc.code]
            except urllib.error.URLError as exc:  # a socket timeout while connecting arrives wrapped
                if not isinstance(exc.reason, TimeoutError):
                    raise
                kind, detail = "timeout", f"client timeout: {exc.reason}"
            except TimeoutError as exc:
                kind, detail = "timeout", f"client timeout: {exc}"
            if wait is None:
                raise RuntimeError(f"{detail} (retries so far: {retries})")
            retries[kind] += 1
            time.sleep(wait)
        raise AssertionError("unreachable")


class AnthropicNativeConversation:
    """The same two-way translation as the other native transports, in Messages form. A `tool_use` block becomes
    the reply line `CALL stock_lookup {...}`; the harness's next message goes back as that call's `tool_result`.
    A tool result and a new request share one user message, results first, as the API requires.

    One difference from the OpenAI and OpenRouter transports: each assistant turn is sent back whole and
    unchanged, thinking blocks and any text beside a call included. The API requires it once thinking is on (a
    thinking block that precedes a tool call must come back, and an edited history invalidates it), and the
    history then stays the same whether thinking is on or off."""

    def __init__(self, transport: AnthropicNativeTransport, system: str):
        self.t, self.system = transport, system
        self.messages: List[Dict[str, Any]] = []
        self.pending: List[str] = []  # ids of the model's last tool calls; the first gets the harness's next message

    def _results(self, output: str) -> List[Dict[str, Any]]:
        blocks = [{"type": "tool_result", "tool_use_id": self.pending[0], "content": output}]
        blocks += [{"type": "tool_result", "tool_use_id": extra, "content": "Not run: make one call at a time."}
                   for extra in self.pending[1:]]  # parallel calls are switched off; if one slips through, answer it
        self.pending = []
        return blocks

    def _meta(self, payload: Dict[str, Any], latency: float, retries: Dict[str, int],
              request_id: Optional[str]) -> Dict[str, Any]:
        u = payload.get("usage") or {}
        p = self.t.prices
        cost = (u.get("input_tokens", 0) * p["input"] + u.get("output_tokens", 0) * p["output"]
                + (u.get("cache_creation_input_tokens") or 0) * p.get("cache_write", p["input"])
                + (u.get("cache_read_input_tokens") or 0) * p.get("cache_read", p["input"])) / 1e6
        meta = {"cost_usd": cost, "cost_source": "price_estimate", "usage": u, "latency_seconds": latency,
                "request_id": request_id, "message_id": payload.get("id"), "served_model": payload.get("model"),
                "stop_reason": payload.get("stop_reason")}
        meta.update({f"{kind}_retries": n for kind, n in retries.items()})
        return meta

    def say(self, text: str) -> Tuple[str, Dict[str, Any]]:
        from causetest.protocol import NO_CALLS_LEFT, TOOL, TOOL_SPEC
        prefix = f"RESULT {TOOL}: "
        if self.pending and text.startswith("New request:"):
            # the request ended on protocol limits with a call still open: close it, then the new request
            content: List[Dict[str, Any]] = self._results(NO_CALLS_LEFT) + [{"type": "text", "text": text}]
        elif self.pending:
            content = self._results(text[len(prefix):] if text.startswith(prefix) else text)
        else:
            content = [{"type": "text", "text": text}]
        self.messages.append({"role": "user", "content": content})
        tool = {"name": TOOL_SPEC["name"], "description": TOOL_SPEC["description"],
                "input_schema": TOOL_SPEC["parameters"], "strict": True}
        body = {"model": self.t.model, "system": self.system, "messages": self.messages, "tools": [tool],
                "tool_choice": {"type": "auto", "disable_parallel_tool_use": True}}
        body.update({k: v for k, v in self.t.options.items() if v is not None})
        payload, latency, retries, request_id = self.t.post(body)
        meta = self._meta(payload, latency, retries, request_id)
        blocks = payload.get("content") or []
        self.messages.append({"role": "assistant", "content": blocks})  # whole and unchanged (see the class note)
        calls = [b for b in blocks if b.get("type") == "tool_use"]
        said = "".join(b.get("text", "") for b in blocks if b.get("type") == "text")
        thinking = [b for b in blocks if b.get("type") in ("thinking", "redacted_thinking")]
        meta.update(native_calls=len(calls), thinking_blocks=len(thinking))
        if not calls:
            return said, meta
        self.pending = [c["id"] for c in calls]
        if said.strip():
            meta["text_with_call"] = said
        first = calls[0]
        return f"CALL {first.get('name')} {json.dumps(first.get('input'))}", meta


# ---------------------------------------------------------------- MOCK


class MockTransport:
    label = "mock"
    is_mock = True

    def __init__(self, kind: str, params: Dict[str, Any]):
        self.kind, self.params = kind, params

    def open(self, conv_key: str, system: str, crn_seed: Optional[int] = None):
        """`crn_seed` (scripted agents only) seeds draws shared by a Y run and the C run it replays."""
        return make_scripted_agent(self.kind, self.params, conv_key, system, crn_seed)
