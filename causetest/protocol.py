"""What the agent sees, how its replies are read, and how its response to a failure is coded.

Same plain-text CALL/ANSWER protocol as C3. Unlike C3's design A1, the system prompt carries no hint
about SKU spellings: the error message is the only causal information the agent gets.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional, Sequence

from causetest.env import TOOL, Task, World, resolve_depot, resolve_item

MAX_CALLS_PER_TASK = 6
MAX_FORMAT_ERRORS_PER_TASK = 2

SYSTEM_TEMPLATE = """You are the stock assistant for Harrow & Vale Supply, a wholesaler with six depots. Staff send you requests one at a time. Answer each request using the tool below. The figures exist only in the company systems, so never estimate or guess them.

Tool
- stock_lookup: returns the units on hand of one item at one depot. Arguments: "site" (the depot) and "sku" (the item's SKU).

Depot directory: {directory}.

How to reply
- To use the tool, reply with one line in this form, then stop and wait:
  CALL stock_lookup {{"site": "...", "sku": "..."}}
  The tool's result comes back in the next message.
- When you have the figure, reply with one line: ANSWER <figure>
- If you cannot get it, reply with: ANSWER UNKNOWN
- You may make at most {max_calls} tool calls per request."""


TEXT_CALL_RULE = """- To use the tool, reply with one line in this form, then stop and wait:
  CALL stock_lookup {"site": "...", "sku": "..."}
  The tool's result comes back in the next message."""
# Native tool calling (paper plan W1): the agent calls the tool through the provider's function-calling API, so
# the only change to the instructions is this rule; everything else is word for word the same.
NATIVE_CALL_RULE = "- To use the tool, call stock_lookup. Make one call at a time; its result comes back to you."

# The function the native transports declare. Its description repeats the system prompt's "Tool" line.
TOOL_SPEC = {
    "name": TOOL,
    "description": "Returns the units on hand of one item at one depot.",
    "parameters": {"type": "object", "properties": {"site": {"type": "string", "description": "the depot"},
                                                    "sku": {"type": "string", "description": "the item's SKU"}},
                   "required": ["site", "sku"], "additionalProperties": False},
}


def system_prompt(world: World, notes: Optional[Sequence[str]] = None, native: bool = False) -> str:
    """The agent's instructions. `notes` (extension E2 only) adds an "Errors" section after the tool
    description; without notes the text is exactly the kill test's. `native` (paper plan W1) swaps the
    CALL-line rule for one that points to native function calling."""
    directory = ", ".join(f"{d.name} (site {d.number})" for d in world.depots)
    text = SYSTEM_TEMPLATE.format(directory=directory, max_calls=MAX_CALLS_PER_TASK)
    if native:
        assert TEXT_CALL_RULE in text
        text = text.replace(TEXT_CALL_RULE, NATIVE_CALL_RULE, 1)
    if notes:
        section = "Errors\n" + "\n".join(f"- {n}" for n in notes)
        text = text.replace("\n\nDepot directory:", f"\n\n{section}\n\nDepot directory:", 1)
    return text


def result_message(text: str) -> str:
    return f"RESULT {TOOL}: {text}"


NO_CALLS_LEFT = "No tool calls remain for this request. Reply with your ANSWER line."
FORMAT_REMINDER = "Please reply with exactly one CALL line or one ANSWER line, in the form given in your instructions."

_DECOR = r"[\s`*_>#-]*"
_CALL = re.compile(rf"^{_DECOR}CALL\s+([A-Za-z_]+)\s*(\{{.*\}})\s*[`*_]*\s*$")
_ANSWER = re.compile(rf"^{_DECOR}ANSWER\s*:?\s*(.*?)\s*[`*_.]*\s*$")
_PROTOCOL_LINE = re.compile(rf"^{_DECOR}(CALL|ANSWER)\b")
_RESULT_LINE = re.compile(rf"^{_DECOR}RESULT\b")


def parse_reply(reply: str) -> Dict[str, Any]:
    """The first CALL or ANSWER line decides the action. Later protocol lines are counted, not used,
    and so are RESULT lines the agent wrote itself (a fabricated tool result)."""
    lines = (reply or "").splitlines()
    first: Optional[Dict[str, Any]] = None
    extra = 0
    for line in lines:
        if not _PROTOCOL_LINE.match(line):
            continue
        if first is not None:
            extra += 1
            continue
        m = _CALL.match(line)
        if m:
            try:
                args = json.loads(m.group(2))
            except json.JSONDecodeError:
                args = None
            if m.group(1) != TOOL or not isinstance(args, dict):
                first = {"kind": "invalid", "reason": "malformed_call", "line": line.strip()}
            else:
                first = {"kind": "call", "args": args}
            continue
        m = _ANSWER.match(line)
        value = m.group(1).strip() if m else ""
        first = {"kind": "answer", "value": value} if value else {"kind": "invalid", "reason": "empty_answer"}
    if first is None:
        first = {"kind": "invalid", "reason": "no_protocol_line"}
    first["extra_protocol_lines"] = extra
    first["fabricated_result_lines"] = sum(bool(_RESULT_LINE.match(line)) for line in lines)
    return first


def cut_after_first_protocol_line(reply: str) -> str:
    """The reply up to and including its first CALL or ANSWER line, as a stop sequence would leave it.
    Used only for what goes back into the agent's history (Luna deviation L1); parsing and the
    recorded reply use the full text. A reply with no protocol line is unchanged."""
    lines = (reply or "").splitlines()
    for i, line in enumerate(lines):
        if _PROTOCOL_LINE.match(line):
            return "\n".join(lines[: i + 1])
    return reply


def normalize_answer(value: str) -> str:
    """Lenient: the first whole number anywhere in the answer, else "unknown" if the word appears.
    (C3 lost correct answers to a strict normalizer when they were written as sentences.)"""
    v = (value or "").lower()
    m = re.search(r"\b\d+\b", v)
    if m:
        return m.group(0)
    return "unknown" if "unknown" in v else v.strip()


RESPONSES = ("REFORMAT", "RETRY", "SITE_ONLY", "STOP", "OTHER")


def classify_response(world: World, task: Task, failed_args: Dict[str, Any],
                      next_action: Optional[Dict[str, Any]]) -> str:
    """The agent's next valid action after a failed call:

    STOP       it answered (any ANSWER line)
    RETRY      the identical call again (same "sku" and "site" strings)
    SITE_ONLY  same SKU string, the depot written differently
    REFORMAT   the SKU string changed but still names the requested item
    OTHER      a call that names a different item or depot, or none
    UNCLASSIFIABLE  no valid action followed (the request ended on protocol limits)
    """
    if next_action is None:
        return "UNCLASSIFIABLE"
    if next_action["kind"] == "answer":
        return "STOP"
    args = next_action["args"]
    item, depot = resolve_item(world, args.get("sku")), resolve_depot(world, args.get("site"))
    if item is None or depot is None or item.sku != task.sku or depot.name != task.depot:
        return "OTHER"
    same_sku = str(args.get("sku")).strip() == str(failed_args.get("sku")).strip()
    same_site = str(args.get("site")).strip() == str(failed_args.get("site")).strip()
    if same_sku:
        return "RETRY" if same_site else "SITE_ONLY"
    return "REFORMAT"


def spelling_of(task_sku: str, raw: Any) -> str:
    """Which spelling of the requested SKU a call used: given (as in the request), upper, nohyphen,
    lower_nohyphen, or other."""
    raw = str(raw).strip()
    return {task_sku.lower(): "given", task_sku: "upper", task_sku.replace("-", ""): "nohyphen",
            task_sku.replace("-", "").lower(): "lower_nohyphen"}.get(raw, "other")


# Causal language in the agent's own words (pre-written rules, no LLM judge). Echoes of the error text count.
SELF_CAUSE = re.compile(r"\b(?:format\w*|spell\w*|written|upper ?case|lower ?case|hyphen\w*|convention\w*|"
                        r"capitali[sz]\w*)\b", re.I)
SERVICE_CAUSE = re.compile(r"\b(?:temporar\w*|outage|service|unavailable|down|server|transient|"
                           r"system (?:is|seems|appears)|not available)\b", re.I)


def cause_language(reply: str) -> Dict[str, bool]:
    return {"self": bool(SELF_CAUSE.search(reply or "")), "service": bool(SERVICE_CAUSE.search(reply or ""))}
