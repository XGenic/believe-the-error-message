"""Figure: success by stated cause × true fault, one grid per model and setting (paper plan W7, figure 1).

Reads the committed C4 summaries named in `causetest/panel.py` and writes `stated_true_grid.svg` and
`stated_true_grid.csv` beside this file. Standard library only. Run from the experiment folder:

    python figures/stated_true_grid.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DIR.parent))
from causetest.panel import ARMS  # noqa: E402

RUNS = DIR.parent / "runs"
CLAIMS = [("format", "“format”"), ("transient", "“temporary”"), ("permanent", "“unavailable”"),
          ("neutral", "neutral")]
FAULTS = [("fixable", "fixable"), ("transient", "transient"), ("permanent", "permanent")]
TRAPS = {("transient", "fixable"), ("permanent", "transient")}
# One hue, light to dark (sequential); a near-surface neutral for "almost never solved".
BINS = [(0.1, "#f0efec"), (0.3, "#b7d3f6"), (0.5, "#86b6ef"), (0.7, "#5598e7"), (0.9, "#2a78d6"), (1.01, "#184f95")]
INK, INK2, MUTED, SURFACE, TRAP = "#0b0b0b", "#52514e", "#898781", "#fcfcfb", "#e34948"
CW, CH, LW, TOP, GAPX, GAPY, COLS = 54, 30, 92, 118, 30, 72, 4


def fill(p):
    return next(c for hi, c in BINS if p < hi)


def grids():
    out = []
    for model, setting, src in ARMS:
        path = RUNS / src["c4"] / "analysis" / "summary.json"
        if not path.exists():
            continue
        s = json.loads(path.read_text(encoding="utf-8"))
        cells = {}
        for claim, _ in CLAIMS:
            for fault, _ in FAULTS:
                by_request = s["cells"][f"{claim}|{fault}"]["success_by_request"]
                cells[(claim, fault)] = sum(by_request) / len(by_request)
        out.append({"model": model, "setting": setting, "run": src["c4"], "S": s["S"], "cells": cells})
    return out


def svg(gs):
    gw, gh = LW + CW * len(FAULTS), CH * len(CLAIMS) + 40
    rows = (len(gs) + COLS - 1) // COLS
    W = 24 + COLS * gw + (COLS - 1) * GAPX + 24
    H = TOP + rows * gh + (rows - 1) * GAPY + 40
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Helvetica, Arial, sans-serif" role="img" aria-labelledby="t d">',
         '<title id="t">Share of requests solved, by stated cause and true fault, per model</title>',
         '<desc id="d">One grid per model and setting. Rows: the cause the error message states; columns: the true '
         'fault. Red outlines mark the two traps. Data in stated_true_grid.csv.</desc>',
         f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>',
         f'<text x="24" y="26" font-size="16" font-weight="600" fill="{INK}">Every model follows the stated cause into both traps</text>',
         f'<text x="24" y="46" font-size="12" fill="{INK2}">Share of requests solved, by the cause the error states (rows) and the true fault (columns). '
         f'Red outline: the two traps. C4 grid, 30 runs of 6 requests per cell.</text>']
    lx = 24
    for i, (hi, color) in enumerate(BINS):  # legend: the bins, in order
        lo = 0 if i == 0 else BINS[i - 1][0]
        label = f"{lo:.0%}–{min(hi, 1):.0%}".replace("101%", "100%")
        o.append(f'<rect x="{lx}" y="62" width="22" height="14" rx="2" fill="{color}"/>')
        o.append(f'<text x="{lx + 28}" y="73" font-size="11" fill="{INK2}">{label}</text>')
        lx += 86
    o.append(f'<rect x="{lx + 6}" y="62" width="22" height="14" rx="2" fill="none" stroke="{TRAP}" stroke-width="2"/>')
    o.append(f'<text x="{lx + 34}" y="73" font-size="11" fill="{INK2}">trap</text>')
    for i, g in enumerate(gs):
        r, c = divmod(i, COLS)
        x0, y0 = 24 + c * (gw + GAPX), TOP + r * (gh + GAPY)
        o.append(f'<text x="{x0}" y="{y0 - 22}" font-size="12" font-weight="600" fill="{INK}">{g["model"]}</text>')
        o.append(f'<text x="{x0}" y="{y0 - 8}" font-size="11" fill="{INK2}">{g["setting"]} · S {g["S"]:+.2f}</text>')
        for j, (_, flabel) in enumerate(FAULTS):
            o.append(f'<text x="{x0 + LW + j * CW + CW / 2:.1f}" y="{y0 + CH * len(CLAIMS) + 16}" font-size="10" '
                     f'fill="{MUTED}" text-anchor="middle">{flabel}</text>')
        for k, (claim, clabel) in enumerate(CLAIMS):
            y = y0 + k * CH
            o.append(f'<text x="{x0 + LW - 6}" y="{y + CH / 2 + 4:.1f}" font-size="11" fill="{INK2}" text-anchor="end">{clabel}</text>')
            for j, (fault, _) in enumerate(FAULTS):
                p = g["cells"][(claim, fault)]
                x = x0 + LW + j * CW
                o.append(f'<rect x="{x + 1}" y="{y + 1}" width="{CW - 2}" height="{CH - 2}" rx="3" fill="{fill(p)}"/>')
                ink = SURFACE if p >= 0.5 else INK
                o.append(f'<text x="{x + CW / 2:.1f}" y="{y + CH / 2 + 4:.1f}" font-size="11" fill="{ink}" '
                         f'text-anchor="middle">{round(p * 100)}</text>')
                if (claim, fault) in TRAPS:
                    o.append(f'<rect x="{x + 1}" y="{y + 1}" width="{CW - 2}" height="{CH - 2}" rx="3" fill="none" '
                             f'stroke="{TRAP}" stroke-width="2"/>')
    o.append(f'<text x="{W - 24}" y="{H - 12}" font-size="10" fill="{MUTED}" text-anchor="end">Columns: the true fault. '
             f'Cell values: % of requests solved.</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def main():
    gs = grids()
    with (DIR / "stated_true_grid.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["model", "setting", "run", "stated_cause", "true_fault", "success"])
        for g in gs:
            for (claim, fault), p in g["cells"].items():
                w.writerow([g["model"], g["setting"], g["run"], claim, fault, p])
    (DIR / "stated_true_grid.svg").write_text(svg(gs), encoding="utf-8", newline="\n")
    print(f"{len(gs)} grids -> {DIR / 'stated_true_grid.svg'}")


if __name__ == "__main__":
    main()
