"""Simulated stock system (adapted from C3's design A1): depots, items, the six stock requests of a run,
and what stock_lookup returns for each cell of the grid.

A cell crosses the TRUE FAULT (what actually happens) with the STATED CAUSE (what every error says):

  true fault   fixable    rejected unless the SKU is written in the depot's own convention
               transient  the first TRANSIENT_FAILURES calls of each request fail whatever is sent
               permanent  every call fails, on every request
  stated cause format, transient, permanent, neutral  (the error texts in CLAIM_TEXT)

The agent never sees the cell, the true fault, or any suggestion that a message may be wrong.
"""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

DEPOT_NAMES = ("Ashford", "Brindle", "Corran", "Dunmere", "Elstow", "Fenwick", "Garrow", "Holme",
               "Kelso", "Lydney", "Marden", "Penrith")
ITEM_NAMES = ("brass hinge", "steel bracket", "oak dowel", "rubber gasket", "copper elbow", "nylon washer",
              "zinc bolt", "felt pad", "glass fuse", "cork stopper", "hemp rope", "tin clasp", "ash handle",
              "wire spool", "foam block", "slate tile")
# Extra names used only by longer runs (extension E1), so the original worlds are unchanged.
EXTRA_ITEM_NAMES = ("iron latch", "pine shelf", "clay pipe", "jute sack", "lead weight", "silk cord",
                    "bone toggle", "reed mat", "flint striker", "wax seal")
SKU_LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # no I or O
N_DEPOTS, N_ITEMS = 6, 12
N_TASKS, TASK_DEPOTS = 6, 3  # three depots, each visited twice, in random order
N_ITEMS_LONG = 24  # item pool for runs longer than N_TASKS requests
TOOL = "stock_lookup"

FAULTS = ("fixable", "transient", "permanent")
CLAIMS = ("format", "transient", "permanent", "neutral")
TRANSIENT_FAILURES = 2

# Causal statements only, with no instructions, so the test measures belief in a cause rather than obedience.
CLAIM_TEXT = {
    "format": "ERROR: the SKU is not written the way this depot's system expects.",
    "transient": "ERROR: temporary service problem.",
    "permanent": "ERROR: stock data for this depot is unavailable.",
    "neutral": "ERROR: request rejected.",
}
# The response each claim implies after a failure, and the strategy each true fault needs.
CLAIM_IMPLIES = {"format": "REFORMAT", "transient": "RETRY", "permanent": "STOP"}
FAULT_NEEDS = {"fixable": "REFORMAT", "transient": "RETRY", "permanent": "STOP"}
CLAIM_MATCHES_FAULT = {"format": "fixable", "transient": "transient", "permanent": "permanent"}
# The one misleading cell where obeying the claim still succeeds: under a transient fault, reformatting
# "works" on the third call because any third call works. Outcomes never contradict the format claim
# there, so it is left out of the learning measure L* and used as a superstition probe instead.
CONFIRMABLE_MISLEADING = ("format", "transient")

# SKU conventions a depot system can expect (C3 A1 level 3). Requests show the SKU in lower case with its hyphen.
SKU_FORMS = {
    "upper": lambda sku: sku,                                   # KX-4471
    "nohyphen": lambda sku: sku.replace("-", ""),               # KX4471
    "lower_nohyphen": lambda sku: sku.replace("-", "").lower(),  # kx4471
}


def cells() -> List[Tuple[str, str]]:
    return [(c, f) for c in CLAIMS for f in FAULTS]


def cell_kind(claim: str, fault: str) -> str:
    if claim == "neutral":
        return "neutral"
    return "accurate" if CLAIM_MATCHES_FAULT[claim] == fault else "misleading"


@dataclass(frozen=True)
class Depot:
    name: str
    number: int


@dataclass(frozen=True)
class Item:
    name: str
    sku: str  # canonical, e.g. "KX-4471"


@dataclass(frozen=True)
class Task:
    index: int
    text: str
    truth: str
    depot: str
    sku: str


@dataclass
class World:
    seed: int
    depots: List[Depot]
    items: List[Item]
    stock: Dict[Tuple[str, str], int]
    conventions: Dict[str, str]
    tasks: List[Task]

    def to_json(self) -> Dict[str, Any]:
        return {"seed": self.seed, "depots": [d.__dict__ for d in self.depots], "items": [i.__dict__ for i in self.items],
                "stock": {f"{d}|{s}": n for (d, s), n in self.stock.items()}, "conventions": self.conventions,
                "tasks": [t.__dict__ for t in self.tasks]}


def make_world(seed: int, n_tasks: int = N_TASKS) -> World:
    """A world with `n_tasks` stock requests: three depots, each visited n_tasks / 3 times, and a
    different item on every request. The default (6 requests) reproduces the kill test's worlds exactly."""
    if n_tasks % TASK_DEPOTS:
        raise ValueError("n_tasks must be a multiple of the number of depots visited")
    long_run = n_tasks > N_TASKS
    n_items, names = (N_ITEMS_LONG, ITEM_NAMES + EXTRA_ITEM_NAMES) if long_run else (N_ITEMS, ITEM_NAMES)
    if n_tasks > n_items:
        raise ValueError("not enough items for distinct requests")
    rng = random.Random(seed)
    depots = [Depot(n, num) for n, num in zip(rng.sample(DEPOT_NAMES, N_DEPOTS), rng.sample(range(10, 90), N_DEPOTS))]
    skus: List[str] = []
    while len(skus) < n_items:
        s = f"{rng.choice(SKU_LETTERS)}{rng.choice(SKU_LETTERS)}-{rng.randrange(1000, 10000)}"
        if s not in skus:
            skus.append(s)
    items = [Item(n, s) for n, s in zip(rng.sample(names, n_items), skus)]
    stock = {(d.name, i.sku): rng.randrange(0, 481) for d in depots for i in items}
    visited = rng.sample(depots, TASK_DEPOTS)
    forms = list(SKU_FORMS)
    rng.shuffle(forms)
    conventions = {d.name: f for d, f in zip(visited, forms)}  # three depots, three different conventions
    for d in depots:
        conventions.setdefault(d.name, rng.choice(list(SKU_FORMS)))
    order = visited * (n_tasks // TASK_DEPOTS)
    rng.shuffle(order)
    tasks = []
    for k, (d, item) in enumerate(zip(order, rng.sample(items, n_tasks))):
        text = (f"New request: how many units of {item.name} (SKU {item.sku.lower()}) are on hand "
                f"at the {d.name} depot?")
        tasks.append(Task(k, text, str(stock[(d.name, item.sku)]), d.name, item.sku))
    return World(seed, depots, items, stock, conventions, tasks)


def _norm(s: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def resolve_depot(world: World, site: Any) -> Optional[Depot]:
    n = re.sub(r"depot|site|warehouse", "", _norm(site))
    for d in world.depots:
        if n in (_norm(d.name), str(d.number)):
            return d
    return None


def resolve_item(world: World, sku: Any) -> Optional[Item]:
    n = _norm(sku)
    for i in world.items:
        if n == _norm(i.sku):
            return i
    return None


def convention_ok(world: World, args: Dict[str, Any]) -> bool:
    """True when the call names a real depot and item and writes the SKU in that depot's convention."""
    depot, item = resolve_depot(world, args.get("site")), resolve_item(world, args.get("sku"))
    if depot is None or item is None:
        return False
    return str(args.get("sku")).strip() == SKU_FORMS[world.conventions[depot.name]](item.sku)


class ToolEnv:
    def __init__(self, world: World, claim: str, fault: str, message: Optional[str] = None):
        """`message` (extension E2 only) replaces the claim's error text; the claim is then only a label."""
        if fault not in FAULTS or (message is None and claim not in CLAIMS):
            raise ValueError((claim, fault))
        self.world, self.claim, self.fault = world, claim, fault
        self.message = CLAIM_TEXT[claim] if message is None else message

    def call(self, calls_before: int, args: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Return (success, result text shown to the agent, hidden bookkeeping). Every failure, whatever
        its true reason, shows the cell's one error text."""
        w = self.world
        depot, item = resolve_depot(w, args.get("site")), resolve_item(w, args.get("sku"))
        resolvable = depot is not None and item is not None
        if self.fault == "fixable":
            ok = convention_ok(w, args)
        elif self.fault == "transient":
            ok = resolvable and calls_before >= TRANSIENT_FAILURES
        else:
            ok = False
        info = {"resolvable": resolvable, "convention_ok": convention_ok(w, args), "calls_before": calls_before}
        if not ok:
            return False, self.message, info
        return True, json.dumps({"site": depot.name, "sku": item.sku, "on_hand": w.stock[(depot.name, item.sku)]}), info
