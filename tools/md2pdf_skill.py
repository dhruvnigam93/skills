"""Render the live /design skill (SKILL.md + template + references) to one PDF.

Reuses the styling of tools/md2pdf_workflow.py, generalized to concatenate the
skill's files with dividers, wrap YAML frontmatter as a code block, and sanitize
box-drawing glyphs the base-14 fonts can't render.
"""
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle, HRFlowable,
)

SKILL_DIR = "/Users/dhruvnigam/.claude/skills/design"
OUT = "/Users/dhruvnigam/.claude/workflow/design-skill.pdf"
FILES = ["SKILL.md", "templates/design-doc.md",
         "references/design-it-twice.md", "references/deep-modules.md"]

INK = HexColor("#1a1a2e")
ACCENT = HexColor("#0f4c81")
GREY = HexColor("#555566")
CODE_BG = HexColor("#eef0f5")
ROW_ALT = HexColor("#f5f7fa")

styles = getSampleStyleSheet()
h1 = ParagraphStyle("H1", parent=styles["Title"], fontSize=22, leading=27,
                    textColor=INK, spaceAfter=6, alignment=0)
h2 = ParagraphStyle("H2", parent=styles["Heading1"], fontSize=15, leading=19,
                    textColor=ACCENT, spaceBefore=16, spaceAfter=6)
h3 = ParagraphStyle("H3", parent=styles["Heading2"], fontSize=12, leading=15,
                    textColor=INK, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=9.5, leading=13.5,
                      textColor=INK, spaceAfter=5)
bullet = ParagraphStyle("Bullet", parent=body, leftIndent=14, bulletIndent=4, spaceAfter=3)
quote = ParagraphStyle("Quote", parent=body, leftIndent=12, textColor=GREY,
                       fontName="Helvetica-Oblique", spaceAfter=5)
meta = ParagraphStyle("Meta", parent=body, textColor=GREY, fontSize=9)
cell = ParagraphStyle("Cell", parent=body, fontSize=8, leading=10.5, spaceAfter=0)
cell_hdr = ParagraphStyle("CellH", parent=cell, fontName="Helvetica-Bold")
code_style = ParagraphStyle("Code", fontName="Courier", fontSize=7.8, leading=10,
                            textColor=INK, backColor=CODE_BG, borderPadding=6,
                            spaceBefore=4, spaceAfter=8)

CODEMAP = {ord("─"): "-", ord("│"): "|", ord("→"): ">", ord("←"): "<",
           ord("↑"): "^", ord("↓"): "v", ord("┌"): "+", ord("┐"): "+",
           ord("└"): "+", ord("┘"): "+", ord("├"): "+", ord("┤"): "+",
           ord("┬"): "+", ord("┴"): "+", ord("┼"): "+", ord("•"): "*"}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(t):
    t = esc(t)
    codes = []

    def _stash(m):
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    t = re.sub(r"`([^`]+)`", _stash, t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    t = re.sub(r"\x00(\d+)\x00",
               lambda m: '<font face="Courier" size="8.3" color="#0f4c81">%s</font>' % esc(codes[int(m.group(1))]),
               t)
    return t


avail = A4[0] - 32 * mm


def make_table(rows):
    n = len(rows[0])
    if n == 2:
        widths = [avail * 0.34, avail * 0.66]
    elif n == 3:
        widths = [avail * 0.25, avail * 0.40, avail * 0.35]
    elif n == 4:
        widths = [avail * 0.06, avail * 0.46, avail * 0.16, avail * 0.32]
    else:
        widths = [avail / n] * n
    hdr_white = ParagraphStyle("CellHW", parent=cell_hdr, textColor=HexColor("#ffffff"))
    data = [[Paragraph(inline(c), hdr_white) for c in rows[0]]]
    for row in rows[1:]:
        data.append([Paragraph(inline(c), cell) for c in row])
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#c9cedb")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def build_lines():
    out = ["# /design — live skill",
           "Promoted 2026-07-04 · source: ~/.claude/skills/design/  ·  4 files"]
    for f in FILES:
        content = open(os.path.join(SKILL_DIR, f)).read().splitlines()
        if content and content[0].strip() == "---":
            j = next(k for k in range(1, len(content)) if content[k].strip() == "---")
            content = ["```yaml"] + content[1:j] + ["```", ""] + content[j + 1:]
        out += ["", "---", "_file: %s_" % f, ""] + content
    return out


story = []
lines = build_lines()
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("```"):
        block = []
        i += 1
        while i < len(lines) and not lines[i].startswith("```"):
            block.append(lines[i])
            i += 1
        story.append(Preformatted("\n".join(block).translate(CODEMAP), code_style))
    elif line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-|:]+\|$", lines[i + 1]):
        rows = [[c.strip() for c in line.strip("|").split("|")]]
        i += 2
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([c.strip() for c in lines[i].strip("|").split("|")])
            i += 1
        story.append(Spacer(1, 3))
        story.append(make_table(rows))
        story.append(Spacer(1, 6))
        continue
    elif line.startswith("# "):
        story.append(Paragraph(inline(line[2:]), h1))
    elif line.startswith("## "):
        story.append(Paragraph(inline(line[3:]), h2))
    elif line.startswith("### "):
        story.append(Paragraph(inline(line[4:]), h3))
    elif line.startswith("#### "):
        story.append(Paragraph(inline(line[5:]), h3))
    elif line.strip() == "---":
        story.append(HRFlowable(width="100%", thickness=0.6, color=HexColor("#c9cedb"),
                                spaceBefore=8, spaceAfter=8))
    elif line.startswith("> "):
        story.append(Paragraph(inline(line[2:]), quote))
    elif line.startswith("- "):
        story.append(Paragraph(inline(line[2:]), bullet, bulletText="•"))
    elif line.strip() == "":
        story.append(Spacer(1, 2))
    else:
        story.append(Paragraph(inline(line), body))
    i += 1

SimpleDocTemplate(OUT, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
                  topMargin=15 * mm, bottomMargin=15 * mm,
                  title="/design skill", author="Dhruv Nigam").build(story)
print("wrote", OUT)
