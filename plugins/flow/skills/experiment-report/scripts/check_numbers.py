"""Check that every number on a report page matches a value in its source files.

Usage:
    uv run --no-project python check_numbers.py PAGE.html SOURCE [SOURCE ...] [--ignore TOKEN ...] [--include-svg]

SOURCE files are JSON, JSONL, CSV or TSV. Every numeric value in them (at any depth, numeric strings too) is a
candidate. Numbers that exist in no file, such as ratios, costs, shares or counts worked out from the results,
go into a JSON file written by code (for example numbers.json) and passed as one more source. Never type them in by hand.

A page number matches when some source value rounds to it at the page's precision: as written, as a percentage
(x100), or in thousands for a "k" suffix ("77k"). Signs must agree; "−" (U+2212) counts as a minus.

The checker reads tables, prose, captions and the meta line. It skips <code>, <footer>, <style>, <script>,
section and table numbers, references such as "Table 3" or "section 4.2", dates, identifiers glued to letters
("4B", "2e−5", "E-71"), integers below 10, anything inside an element with a data-nocheck attribute, and SVG
text (use --include-svg to check figure labels too).

It prints each number with no match, with its context, and exits 1 if there are any. A match means some source
value rounds to the number. It catches typos, stale numbers and numbers from memory. It cannot catch a correct
value placed in the wrong cell, so read Table 1 against its source once by eye as well.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SKIP_TAGS = {"code", "footer", "style", "script", "title", "svg", "pre"}
INLINE_TAGS = {"b", "strong", "i", "em", "a", "abbr", "sub", "sup", "u", "mark", "small"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SKIP_CLASSES = {"n", "tn"}  # section numbers and "Table 1." labels

REFS = re.compile(
    r"\b(?:Tables?|Figures?|Figs?\.|[Ss]ections?|[Ss]teps?|[Aa]ppendix)\s+\d+(?:\.\d+)*"
    r"(?:\s*(?:,|and|to|–|-|&)\s*\d+(?:\.\d+)*)*"
)
DATES = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?)?\b")
NUMBER = re.compile(
    r"(?<![\w.,\-−+/±×@])"  # not glued to a word, a decimal, a range or a sign that belongs to something else
    r"([+\-−]?)"  # sign
    r"(\d{1,3}(?:,\d{3})+|\d+)"  # integer part, with or without thousands separators
    r"(\.\d+)?"  # decimals
    r"(%|k(?![A-Za-z]))?"  # percent or thousands
    r"(?![\w]|\.\d|,\d)"  # not followed by more of a word or a number
)


class PageText(HTMLParser):
    """Collect the page's visible text, with a space at every block boundary."""

    def __init__(self, include_svg: bool) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_tags = SKIP_TAGS - ({"svg"} if include_svg else set())
        self.stack: list[tuple[str, bool]] = []
        self.parts: list[str] = []

    def _skipping(self) -> bool:
        return any(skip for _, skip in self.stack)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        skip = tag in self.skip_tags or "data-nocheck" in a or bool(classes & SKIP_CLASSES)
        if tag not in INLINE_TAGS:
            self.parts.append(" ")
        if tag not in VOID_TAGS:
            self.stack.append((tag, skip))

    def handle_startendtag(self, tag, attrs):
        if tag not in INLINE_TAGS:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag not in INLINE_TAGS:
            self.parts.append(" ")
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not self._skipping():
            self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.parts))


def walk(value, out: list[float]) -> None:
    if isinstance(value, bool) or value is None:
        return
    if isinstance(value, (int, float)):
        out.append(float(value))
    elif isinstance(value, str):
        try:
            out.append(float(value.replace(",", "")))
        except ValueError:
            pass
    elif isinstance(value, dict):
        for v in value.values():
            walk(v, out)
    elif isinstance(value, (list, tuple)):
        for v in value:
            walk(v, out)


def load_source(path: Path) -> list[float]:
    values: list[float] = []
    suffix = path.suffix.lower()
    if suffix == ".json":
        walk(json.loads(path.read_text()), values)
    elif suffix == ".jsonl":
        for line in path.read_text().splitlines():
            if line.strip():
                walk(json.loads(line), values)
    elif suffix in {".csv", ".tsv"}:
        with path.open(newline="") as f:
            for row in csv.reader(f, delimiter="\t" if suffix == ".tsv" else ","):
                walk(row, values)
    else:
        sys.exit(f"{path}: unsupported source type. Export the numbers to JSON with code and pass that file.")
    return values


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page")
    ap.add_argument("sources", nargs="+")
    ap.add_argument("--ignore", action="append", default=[], help="a token to skip, exactly as written on the page")
    ap.add_argument("--include-svg", action="store_true")
    ap.add_argument("--min-int", type=int, default=10, help="skip integers below this (default 10)")
    args = ap.parse_args()

    values: list[float] = []
    for s in args.sources:
        values += load_source(Path(s))
    if not values:
        sys.exit("No numeric values in the sources.")
    as_is = sorted(values)
    as_pct = sorted(v * 100 for v in values)
    as_k = sorted(v / 1000 for v in values)

    def found(table: list[float], target: float, tol: float) -> bool:
        i = bisect.bisect_left(table, target - tol)
        return i < len(table) and table[i] <= target + tol

    parser = PageText(args.include_svg)
    parser.feed(Path(args.page).read_text())
    text = DATES.sub(" ", REFS.sub(" ", parser.text()))

    checked, missing = 0, []
    for m in NUMBER.finditer(text):
        sign, whole, frac, suffix = m.group(1), m.group(2), m.group(3) or "", m.group(4) or ""
        token = m.group(0)
        if token in args.ignore or token.lstrip("+-−") in args.ignore:
            continue
        if not frac and not suffix and int(whole.replace(",", "")) < args.min_int:
            continue
        value = float(whole.replace(",", "") + frac) * (-1 if sign in {"-", "−"} else 1)
        decimals = max(len(frac) - 1, 0)
        tol = 0.5 * 10 ** (-decimals) + 1e-9
        checked += 1
        if suffix == "%":
            ok = found(as_pct, value, tol) or found(as_is, value, tol)
        elif suffix == "k":
            ok = found(as_k, value, tol)
        else:
            ok = found(as_is, value, tol)
        if not ok:
            lo, hi = max(m.start() - 50, 0), min(m.end() + 30, len(text))
            missing.append((token, text[lo:hi].strip()))

    for token, context in missing:
        print(f"no match  {token:>12}   …{context}…")
    print(f"\n{checked} numbers checked, {len(missing)} with no match in {len(args.sources)} source file(s).")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
