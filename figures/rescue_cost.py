"""Figure: the give-up rescue against its cost, per model and wording (paper plan W7, figure 3).

Reads the committed summaries of E3 (Luna, text) and of W6, W2-C and W2-D (native calls) and writes
`rescue_cost.svg` and `rescue_cost.csv` beside this file. Standard library only. Run from the experiment folder:

    python figures/rescue_cost.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent
RUNS = DIR.parent / "runs"
PANELS = [("GPT-6-luna, text, low (E3)", "e3-live-gpt-6-luna"),
          ("GPT-6-luna, native, low", "w6-gpt6luna-native-low"),
          ("DeepSeek V4.1 Flash r0", "w6-deepseek-v4-1-flash-r0"),
          ("DeepSeek V4.1 Flash r1", "w6-deepseek-v4-1-flash-r1"),
          ("Qwen3.8-27B r0", "w6-qwen3-8-27b-r0"),
          ("gpt-oss-120b r1", "w6-gpt-oss-120b-r1"),
          ("Claude Haiku 5.5, thinking off", "w2c-w6-claude-haiku-5-5-t0"),
          ("Claude Haiku 5.5, thinking on", "w2c-w6-claude-haiku-5-5-t1"),
          ("GPT-6.1 Sol, native, low", "w2d-w6-gpt-6-1-sol-low")]
# (arm, legend label, color, marker). Three categorical slots (validated all-pairs, light surface) and a gray
# reference; each wording also has its own marker shape, so identity is never color alone.
SERIES = [("caution", "plain caution (no stopping rule)", "#898781", "diamond"),
          ("caution_bounded", "“a few different attempts”", "#2a78d6", "circle"),
          ("caution_few", "“a few attempts”", "#eb6834", "square"),
          ("caution_three", "“three attempts in a row”", "#1baf7a", "triangle")]
INK, INK2, MUTED, GRID, AXIS, SURFACE, ZONE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb", "#eef5ec"
X_MAX, Y_MIN, Y_MAX = 6.0, -0.2, 1.05
PW, PH, ML, MT, GAPX, GAPY, COLS = 250, 190, 56, 116, 34, 64, 3


def points():
    out = []
    for title, run in PANELS:
        s = json.loads((RUNS / run / "analysis" / "summary.json").read_text(encoding="utf-8"))
        e, ci = s["estimates"], s["ci"]
        for arm, *_ in SERIES:
            if f"{arm}|give_up_rescue" not in e:
                continue
            calls = e.get(f"{arm}|outage_calls")
            calls_ci = ci.get(f"{arm}|outage_calls")
            if calls is None:  # E3 keeps absolute calls apart, and intervals only against control
                calls, base = s["outage_calls"][arm], s["outage_calls"]["control"]
                assert base == 1, "E3's control made exactly one call on every outage, so the shift is exact"
                calls_ci = [base + v for v in ci[f"{arm}|outage_calls_vs_control"]]
            out.append({"panel": title, "run": run, "arm": arm, "rescue": e[f"{arm}|give_up_rescue"],
                        "rescue_lo": ci[f"{arm}|give_up_rescue"][0], "rescue_hi": ci[f"{arm}|give_up_rescue"][1],
                        "outage_calls": calls, "calls_lo": calls_ci[0] if calls_ci else None,
                        "calls_hi": calls_ci[1] if calls_ci else None})
    return out


def marker(shape, x, y, color, r=5.0):
    ring = f'stroke="{SURFACE}" stroke-width="2"'  # surface ring where marks overlap
    if shape == "circle":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" {ring}/>'
    if shape == "square":
        return f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r}" height="{2 * r}" rx="1.5" fill="{color}" {ring}/>'
    if shape == "triangle":
        h = r * 1.2
        return f'<path d="M{x:.1f},{y - h:.1f} L{x + h:.1f},{y + h * 0.8:.1f} L{x - h:.1f},{y + h * 0.8:.1f} Z" fill="{color}" {ring}/>'
    return f'<path d="M{x:.1f},{y - r - 1:.1f} L{x + r + 1:.1f},{y:.1f} L{x:.1f},{y + r + 1:.1f} L{x - r - 1:.1f},{y:.1f} Z" fill="{SURFACE}" stroke="{color}" stroke-width="2"/>'


def svg(pts):
    rows = (len(PANELS) + COLS - 1) // COLS
    W = ML + COLS * PW + (COLS - 1) * GAPX + 24
    H = MT + rows * PH + (rows - 1) * GAPY + 76
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Helvetica, Arial, sans-serif" role="img" aria-labelledby="t d">',
         '<title id="t">Give-up rescue against its cost on a true outage, per model and wording</title>',
         '<desc id="d">Small multiples, one per model. x: calls per request on a true outage; y: give-up-trap '
         'success minus control. The shaded corner is W6\'s RECOMMENDABLE region. Data in rescue_cost.csv.</desc>',
         f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>',
         f'<text x="{ML}" y="26" font-size="16" font-weight="600" fill="{INK}">A stated count keeps the rescue at the floor cost</text>',
         f'<text x="{ML}" y="46" font-size="12" fill="{INK2}">Give-up-trap rescue (vs control) against calls per request on a true outage. '
         f'Floor: 3 calls. Whiskers: 95% intervals.</text>']
    lx = ML
    for arm, label, color, shape in SERIES:  # legend, one row above the panels
        o.append(marker(shape, lx + 6, 70, color))
        o.append(f'<text x="{lx + 16}" y="74" font-size="12" fill="{INK}">{label}</text>')
        lx += 22 + 6.6 * len(label)
    for i, (title, _) in enumerate(PANELS):
        r, c = divmod(i, COLS)
        x0, y0 = ML + c * (PW + GAPX), MT + r * (PH + GAPY)
        X = lambda v: x0 + v / X_MAX * PW
        Y = lambda v: y0 + (Y_MAX - v) / (Y_MAX - Y_MIN) * PH
        o.append(f'<text x="{x0}" y="{y0 - 10}" font-size="12" font-weight="600" fill="{INK}">{title}</text>')
        o.append(f'<rect x="{X(0):.1f}" y="{Y(Y_MAX):.1f}" width="{X(3.5) - X(0):.1f}" height="{Y(0.5) - Y(Y_MAX):.1f}" fill="{ZONE}"/>')
        for v in (0, 0.5, 1.0):
            o.append(f'<line x1="{X(0):.1f}" x2="{X(X_MAX):.1f}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" '
                     f'stroke="{AXIS if v == 0 else GRID}" stroke-width="1"/>')
            if c == 0:
                o.append(f'<text x="{X(0) - 6:.1f}" y="{Y(v) + 4:.1f}" font-size="11" fill="{MUTED}" text-anchor="end">{v:+.1f}</text>')
        for v in range(0, int(X_MAX) + 1):
            o.append(f'<text x="{X(v):.1f}" y="{Y(Y_MIN) + 16:.1f}" font-size="11" fill="{MUTED}" text-anchor="middle">{v}</text>')
        o.append(f'<line x1="{X(3):.1f}" x2="{X(3):.1f}" y1="{Y(Y_MAX):.1f}" y2="{Y(Y_MIN):.1f}" stroke="{INK2}" stroke-width="1" stroke-dasharray="3 3"/>')
        if i == 0:
            o.append(f'<text x="{X(3) + 4:.1f}" y="{Y(Y_MIN) - 4:.1f}" font-size="10" fill="{INK2}">floor</text>')
        for arm, _, color, shape in SERIES:
            p = next((p for p in pts if p["panel"] == title and p["arm"] == arm), None)
            if p is None:
                continue
            x, y = X(min(p["outage_calls"], X_MAX)), Y(p["rescue"])
            o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{Y(p["rescue_lo"]):.1f}" y2="{Y(p["rescue_hi"]):.1f}" stroke="{color}" stroke-width="1.5"/>')
            if p["calls_lo"] is not None:
                o.append(f'<line x1="{X(p["calls_lo"]):.1f}" x2="{X(min(p["calls_hi"], X_MAX)):.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="1.5"/>')
            o.append(marker(shape, x, y, color))
    rows_y = MT + rows * PH + (rows - 1) * GAPY
    o.append(f'<text x="{ML + (COLS * PW + (COLS - 1) * GAPX) / 2:.1f}" y="{rows_y + 36}" font-size="12" fill="{INK2}" text-anchor="middle">'
             f'calls per request on a true outage (lower is cheaper; the rescue needs 3)</text>')
    o.append(f'<text transform="translate(16,{MT + rows * PH / 2:.1f}) rotate(-90)" font-size="12" fill="{INK2}" text-anchor="middle">give-up rescue vs control</text>')
    o.append(f'<text x="{W - 24}" y="{H - 10}" font-size="10" fill="{MUTED}" text-anchor="end">Shaded: RECOMMENDABLE region (rescue ≥ 0.5, at most 3.5 calls)</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def main():
    pts = points()
    with (DIR / "rescue_cost.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(pts[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(pts)
    (DIR / "rescue_cost.svg").write_text(svg(pts), encoding="utf-8", newline="\n")
    print(f"{len(pts)} points -> {DIR / 'rescue_cost.svg'}")


if __name__ == "__main__":
    main()
