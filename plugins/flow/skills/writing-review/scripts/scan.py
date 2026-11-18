#!/usr/bin/env python3
"""Flag candidate AI-writing patterns in prose, for /flow:writing-review.

Every hit is a candidate. The reviewer judges each one in context: "The ablation
has not run." matches the contrast patterns and is a fine sentence.

Skips YAML front matter, fenced code blocks, inline code, link targets, bare URLs
and one-line HTML comments.

Usage:
  scan.py PATH [PATH ...]          files; directories are walked for prose files
  scan.py -                        text on stdin
  scan.py --since REF [PATH ...]   only lines added or changed since the git ref REF;
                                   with no PATH, every changed or untracked prose file

Standard library only.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

PROSE_EXTENSIONS = {".md", ".mdx", ".markdown", ".rst", ".txt", ".adoc"}


def any_word(*words: str) -> str:
    return r"\b(?:" + "|".join(words) + r")\b"


# (tag, label, pattern). Tags match the categories in references/rules.md.
PATTERNS: list[tuple[str, str, str]] = [
    # Stock contrast
    ("contrast", "not X, but Y", r"\bnot\b[^.;:!?\n]{1,80}?,?\s+but\b"),
    ("contrast", "not just / not only", r"\bnot (?:just|only|merely|simply)\b"),
    ("contrast", "X, not Y", r"[,;—]\s*not\s+\w"),
    ("contrast", "isn't X, it's Y",
     r"\b(?:is|are|was|were)(?:n't| not)\b[^.;\n]{1,60}?[,;—]\s*(?:it|this|that|they)(?:'s|'re| is| are)\b"),
    ("contrast", "more than X", r"\bmore than (?:just|merely|simply|a|an)\b"),
    ("contrast", "the question is no longer", r"\bthe (?:question|issue|problem) is no longer\b"),
    ("contrast", "the real X", r"\bthe real (?:story|question|issue|problem|win|value|reason|point|lesson)\b"),
    ("contrast", "what matters", r"\bwhat (?:really |actually |truly )?matters\b"),
    ("contrast", "rather than", r"\brather than\b"),
    # Empty sentences
    ("empty", "bridge prose", any_word(
        r"(?:the )?main (?:change|point|idea|takeaway|difference)(?: here)? is",
        r"stepping back", r"what this means is", r"that (?:being )?said",
        r"as (?:mentioned|discussed|noted|described) (?:above|earlier|before|previously)")),
    ("empty", "importance claim", any_word(
        r"it(?:'s| is) (?:worth|important to) (?:noting|mentioning|pointing out|highlighting|note)",
        r"it should be noted", r"this is the key", r"key (?:takeaway|insight|point)s?")),
    ("empty", "stage direction", any_word(
        r"let(?:'s| us) (?:dive|take a (?:closer )?look|explore|walk through|break (?:it|this) down|unpack)",
        r"here(?:'s| is) (?:a|the) (?:summary|breakdown|overview|quick)",
        r"in this (?:section|document|doc|post|guide|article|readme|page)")),
    ("empty", "effort narration", any_word(
        r"after (?:extensive|careful|thorough|much|deep|a lot of) "
        r"(?:investigation|analysis|research|testing|debugging|exploration|consideration)")),
    ("empty", "recap or sign-off", any_word(
        r"in (?:summary|conclusion)", r"to (?:summarize|sum up|recap)",
        r"hope this helps", r"let (?:me|us) know if", r"feel free to", r"happy to help")),
    ("empty", "count line before a list",
     r"\b(?:has|have|are|is|includes?|contains?|consists? of|there are)\s+"
     r"(?:two|three|four|five|six|seven|eight|nine|ten|\d+)\s+(?:\w+\s+){0,2}\w+:\s*$"),
    ("empty", "recap heading",
     r"^#{1,6}\s*(?:conclusion|summary|future work|next steps|key takeaways|wrapping up|final thoughts)\b"),
    # Adjectives that need evidence behind them
    ("evidence", "unsupported adjective", any_word(
        r"robust(?:ly|ness)?", r"powerful", r"seamless(?:ly)?", r"significant(?:ly)?",
        r"crucial(?:ly)?", r"pivotal", r"comprehensive", r"scalable", r"dramatic(?:ally)?",
        r"substantial(?:ly)?", r"massive(?:ly)?", r"state-of-the-art", r"cutting-edge",
        r"blazing(?:ly)? fast", r"best-in-class", r"end-to-end")),
    # LLM cadence
    ("cadence", "transition adverb", any_word(
        r"additionally", r"furthermore", r"moreover", r"importantly", r"notably",
        r"interestingly", r"ultimately")),
    ("cadence", "stock vocabulary", any_word(
        r"landscape", r"ecosystems?", r"interplay", r"tapestry", r"testament",
        r"delv(?:e|es|ed|ing)", r"showcas(?:e|es|ed|ing)", r"underscor(?:e|es|ed|ing)",
        r"foster(?:s|ed|ing)?", r"leverag(?:e|es|ed|ing)", r"realm", r"holistic",
        r"streamlin(?:e|es|ed|ing)", r"unlock(?:s|ed|ing)?", r"empower(?:s|ed|ing)?",
        r"harness(?:es|ed|ing)?", r"synerg(?:y|ies)", r"paradigm", r"nuanced",
        r"intricate", r"meticulous(?:ly)?", r"embark(?:s|ed|ing)?")),
    ("cadence", "em-dash aside", r"—|\s–\s|\s--\s"),
    ("cadence", "bold label", r"^\s*(?:[-*+]|\d+\.)?\s*\*\*[^*\n]{1,60}?(?::\*\*|\*\*\s*:)"),
    ("cadence", "takeaway box", any_word(r"key takeaways?", r"tl;?dr", r"bottom line")),
]

COMPILED = [(tag, label, re.compile(rx, re.IGNORECASE | re.MULTILINE)) for tag, label, rx in PATTERNS]

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(.+?)\1")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
URL = re.compile(r"https?://\S+")
HTML_COMMENT = re.compile(r"<!--.*?-->")


def blank(match: re.Match[str]) -> str:
    return " " * len(match.group(0))


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Return (line number, line) for lines outside front matter and code fences,
    with inline code, link targets, URLs and comments blanked out."""
    lines = text.splitlines()
    out: list[tuple[int, str]] = []
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                start = i + 1
                break
    fence: str | None = None
    for i in range(start, len(lines)):
        line = lines[i]
        m = FENCE.match(line)
        if fence is None and m:
            fence = m.group(1)[0] * len(m.group(1))
            continue
        if fence is not None:
            if line.strip().startswith(fence):
                fence = None
            continue
        for rx in (INLINE_CODE, LINK_TARGET, URL, HTML_COMMENT):
            line = rx.sub(blank, line)
        out.append((i + 1, line))
    return out


COUNTS: Counter[str] = Counter()


def scan_text(name: str, text: str, only_lines: set[int] | None) -> list[str]:
    """One block per line with hits: the location, the source line, then each hit."""
    raw = text.splitlines()
    blocks: list[str] = []
    for lineno, line in prose_lines(text):
        if only_lines is not None and lineno not in only_lines:
            continue
        found: list[str] = []
        seen: set[tuple[str, int]] = set()
        for tag, label, rx in COMPILED:
            for m in rx.finditer(line):
                if (tag, m.start()) in seen:
                    continue
                seen.add((tag, m.start()))
                found.append(f"    [{tag}] {label}: \"{m.group(0).strip()}\"")
                COUNTS[tag] += 1
        if found:
            source = raw[lineno - 1].strip()
            if len(source) > 240:
                source = source[:237] + "..."
            blocks.append("\n".join([f"{name}:{lineno}", f"    > {source}", *found]))
    return blocks


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def changed_lines(ref: str, path: Path) -> set[int] | None:
    """Lines of `path` added or changed since `ref`. None means every line (untracked file)."""
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", str(path)],
                             capture_output=True, text=True).returncode == 0
    if not tracked:
        return None
    lines: set[int] = set()
    for hunk in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", git("diff", "-U0", ref, "--", str(path)), re.M):
        first, count = int(hunk.group(1)), int(hunk.group(2) or "1")
        lines.update(range(first, first + count))
    return lines


def changed_prose_files(ref: str) -> list[Path]:
    root = Path(git("rev-parse", "--show-toplevel").strip())
    names = git("diff", "--name-only", "--diff-filter=AMR", ref).splitlines()
    names += git("ls-files", "--others", "--exclude-standard", "--full-name", str(root)).splitlines()
    return sorted({root / n for n in names if Path(n).suffix.lower() in PROSE_EXTENSIONS and (root / n).exists()})


def display_path(f: Path) -> str:
    """Relative to the current directory when the file is under it, else as given."""
    rel = os.path.relpath(f)
    return str(f) if rel.startswith("..") else rel


def expand(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            files += sorted(f for f in p.rglob("*")
                            if f.suffix.lower() in PROSE_EXTENSIONS and not any(part.startswith(".") for part in f.parts))
        elif p.exists():
            files.append(p)
        else:
            print(f"scan.py: no such file: {p}", file=sys.stderr)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="files or directories; '-' reads stdin")
    ap.add_argument("--since", metavar="REF", help="only lines added or changed since this git ref")
    args = ap.parse_args()

    hits: list[str] = []
    if args.paths == ["-"]:
        hits += scan_text("<stdin>", sys.stdin.read(), None)
        n_files = 1
    else:
        if args.paths:
            files = expand(args.paths)
        elif args.since:
            files = changed_prose_files(args.since)
        else:
            ap.error("give a path, '-' for stdin, or --since REF")
        for f in files:
            text = f.read_text(encoding="utf-8", errors="replace")
            only = changed_lines(args.since, f) if args.since else None
            hits += scan_text(display_path(f), text, only)
        n_files = len(files)

    if not hits:
        print(f"No candidates in {n_files} file(s).")
        return 0
    print("\n\n".join(hits))
    summary = ", ".join(f"{tag} {n}" for tag, n in COUNTS.most_common())
    print(f"\n{sum(COUNTS.values())} candidates on {len(hits)} lines in {n_files} file(s): {summary}. "
          "Judge each in context.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
