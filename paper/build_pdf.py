"""Build `PAPER.pdf` from `PAPER.md`: a small Markdown-to-HTML converter for the subset the paper uses (headings,
paragraphs, lists, pipe tables, captions, SVG figures, links, emphasis, code spans), printed to PDF by a headless
Chromium browser (Edge or Chrome). Standard library only; edit PAPER.md and re-run to rebuild. Run from the
experiment folder:

    python paper/build_pdf.py
"""

from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DIR = Path(__file__).resolve().parent
SOURCE, TARGET = DIR / "PAPER.md", DIR / "PAPER.pdf"
BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "msedge", "google-chrome", "chromium", "chromium-browser", "chrome"]
CAPTION = re.compile(r"^\*((Figure|Table) \d+\.)(.*)\*$")
STAR = "\x00"  # stands in for an escaped asterisk while emphasis is parsed
KEEP_ROWS = 14  # tables of up to this many lines (header and rule included) stay on one page
NOWRAP = 14  # table cells this short never wrap ("W2-D", "1 of 1 tested")

CSS = """
@page { size: letter; margin: 0.9in 1in 0.85in;
  @bottom-center { content: counter(page); font: 9pt Cambria, "Times New Roman", serif; color: #444; } }
html { font: 10.5pt/1.42 Cambria, "Times New Roman", serif; color: #111; }
body { margin: 0; }
p { margin: 0 0 0.55em; text-align: justify; hyphens: auto; orphans: 2; widows: 2; }
a { color: #1a4f8b; text-decoration: none; }
code { font: 0.86em Consolas, "Courier New", monospace; }
h1.title { font-size: 17pt; line-height: 1.25; text-align: center; margin: 0 0 0.5em; }
p.byline { text-align: center; margin: 0 0 0.2em; }
p.note { text-align: center; font-size: 9.5pt; margin: 0 0 1.4em; }
h2 { font-size: 12.5pt; margin: 1.3em 0 0.45em; break-after: avoid; }
h3 { font-size: 11pt; margin: 1em 0 0.35em; break-after: avoid; }
h2.abstract { text-align: center; font-size: 11pt; margin-top: 0; }
p.abstract { margin: 0 0.45in 1.2em; font-size: 10pt; }
ul, ol { margin: 0 0 0.6em; padding-left: 1.6em; }
li { margin: 0 0 0.25em; }
ul.refs { list-style: none; padding-left: 1.5em; text-indent: -1.5em; font-size: 9.5pt; }
figure { margin: 0.9em 0 1em; break-inside: avoid; }
figure svg { display: block; width: 100%; height: auto; }
figcaption { font-size: 9pt; line-height: 1.35; margin: 0.4em 0 0; }
figure.table figcaption { margin: 0 0 0.4em; break-after: avoid; }
figure.table { break-inside: auto; }
figure.table.keep { break-inside: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; line-height: 1.3; }
thead th { border-top: 1.2px solid #111; border-bottom: 0.6px solid #111; text-align: left; font-weight: bold; }
tbody tr:last-child td { border-bottom: 1.2px solid #111; }
th, td { padding: 2.5px 6px 2.5px 0; vertical-align: top; }
td.nw { white-space: nowrap; }
tr { break-inside: avoid; }
"""


def inline(text: str) -> str:
    """Code spans first, so nothing inside them is parsed; then links, bold and italics."""
    out = []
    for part in re.split(r"(`[^`]+`)", text.replace("\\*", STAR)):
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append(f"<code>{html.escape(part[1:-1].replace(STAR, '*'))}</code>")
            continue
        s = html.escape(part, quote=False)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"<em>\1</em>", s)
        out.append(s.replace(STAR, "*"))
    return "".join(out)


def cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def td(c: str) -> str:
    return f'<td class="nw">{inline(c)}</td>' if len(c) <= NOWRAP else f"<td>{inline(c)}</td>"


def table(rows: list[str]) -> str:
    head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    tr = "".join("<tr>" + "".join(td(c) for c in r) + "</tr>" for r in body)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"


def svg(path: Path, n: int) -> str:
    """Inline an SVG figure, sized by CSS from its viewBox, with ids made unique per figure."""
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>\s*", "", s)
    s = re.sub(r'(<svg\b[^>]*?)\s+width="[^"]*"\s+height="[^"]*"', r"\1", s, count=1)
    s = re.sub(r'\bid="([^"]+)"', rf'id="f{n}-\1"', s)
    s = re.sub(r'aria-labelledby="([^"]+)"', lambda m: 'aria-labelledby="' + " ".join(
        f"f{n}-{i}" for i in m.group(1).split()) + '"', s)
    return re.sub(r"url\(#([^)]+)\)", rf"url(#f{n}-\1)", s)


def caption(text: str) -> str:
    m = CAPTION.match(text)
    return f"<figcaption><strong>{m.group(1)}</strong>{inline(m.group(3))}</figcaption>"


def blocks(lines: list[str]) -> list[tuple[str, object]]:
    """Group lines into (kind, content) blocks."""
    out, i = [], 0
    starts = ("#", "|", "- ", "![")
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            out.append((f"h{level}", line[level:].strip()))
            i += 1
        elif line.startswith("!["):
            out.append(("image", re.match(r"!\[[^\]]*\]\(([^)]+)\)", line).group(1)))
            i += 1
        else:
            for kind, pattern in (("table", r"\|"), ("ul", r"- "), ("ol", r"\d+\. ")):
                if re.match(pattern, line):
                    items = []
                    while i < len(lines) and re.match(pattern, lines[i]):
                        items.append(lines[i] if kind == "table" else re.sub(pattern, "", lines[i], count=1))
                        i += 1
                    out.append((kind, items))
                    break
            else:
                para = []
                while i < len(lines) and lines[i].strip() and not lines[i].startswith(starts) \
                        and not re.match(r"\d+\. ", lines[i]):
                    para.append(lines[i].strip())
                    i += 1
                out.append(("p", " ".join(para)))
    return out


def render(md: str) -> str:
    parts, figures, section = [], 0, ""
    items = blocks(md.splitlines())
    title = next(c for k, c in items if k == "h1")
    k = 0
    while k < len(items):
        kind, content = items[k]
        nxt = items[k + 1] if k + 1 < len(items) else ("", "")
        if kind == "h1":
            parts.append(f'<h1 class="title">{inline(content)}</h1>')
        elif kind in ("h2", "h3"):
            section = content
            cls = ' class="abstract"' if content == "Abstract" else ""
            parts.append(f"<{kind}{cls}>{inline(content)}</{kind}>")
        elif kind == "image":
            figures += 1
            cap = ""
            if nxt[0] == "p" and CAPTION.match(nxt[1]):
                cap, k = caption(nxt[1]), k + 1
            parts.append(f"<figure>{svg((DIR / content).resolve(), figures)}{cap}</figure>")
        elif kind == "p" and CAPTION.match(content) and nxt[0] == "table":
            cls = "table keep" if len(nxt[1]) <= KEEP_ROWS else "table"  # long tables may break across pages
            parts.append(f'<figure class="{cls}">{caption(content)}{table(nxt[1])}</figure>')
            k += 1
        elif kind == "table":
            parts.append(table(content))
        elif kind in ("ul", "ol"):
            cls = ' class="refs"' if section == "References" else ""
            parts.append(f"<{kind}{cls}>" + "".join(f"<li>{inline(x)}</li>" for x in content) + f"</{kind}>")
        elif kind == "p":
            if not section:  # the lines between the title and the abstract
                cls = "byline" if content.startswith("**") else "note"
            else:
                cls = "abstract" if section == "Abstract" else ""
            parts.append(f'<p{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>{inline(content)}</p>')
        k += 1
    plain = re.sub(r"[*`]", "", title)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(plain)}</title>'
            f'<meta name="author" content="Denis Gurskiy"><style>{CSS}</style></head>'
            f'<body>{"".join(parts)}</body></html>')


def browser() -> str:
    for b in BROWSERS:
        found = b if Path(b).is_file() else shutil.which(b)
        if found:
            return found
    sys.exit("no Chromium-based browser found (Edge or Chrome); add its path to BROWSERS")


def main() -> None:
    page = render(SOURCE.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "paper.html"
        src.write_text(page, encoding="utf-8")
        TARGET.unlink(missing_ok=True)
        # A separate profile keeps a running browser from taking over the job.
        subprocess.run([browser(), "--headless", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                        f"--user-data-dir={Path(tmp) / 'profile'}", "--no-pdf-header-footer",
                        "--print-to-pdf-no-header", f"--print-to-pdf={TARGET}", src.as_uri()],
                       check=True, timeout=180, capture_output=True)
    if not TARGET.is_file():
        sys.exit("the browser did not write the PDF")
    pages = len(re.findall(rb"/Type\s*/Page\b(?!s)", TARGET.read_bytes()))
    print(f"wrote {TARGET.name}: {pages} pages, {TARGET.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
