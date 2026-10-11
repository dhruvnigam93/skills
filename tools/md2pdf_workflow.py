"""Convert ai-coding-workflow.md to a formatted PDF."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle, HRFlowable,
)

SRC = "/Users/dhruvnigam/.claude/workflow/ai-coding-workflow.md"
OUT = "/Users/dhruvnigam/.claude/workflow/ai-coding-workflow.pdf"

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
meta = ParagraphStyle("Meta", parent=body, textColor=GREY, fontSize=9)
cell = ParagraphStyle("Cell", parent=body, fontSize=8, leading=10.5, spaceAfter=0)
cell_hdr = ParagraphStyle("CellH", parent=cell, fontName="Helvetica-Bold")
code_style = ParagraphStyle("Code", fontName="Courier", fontSize=7.8, leading=10,
                            textColor=INK, backColor=CODE_BG, borderPadding=6,
                            spaceBefore=4, spaceAfter=8)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(t):
    t = esc(t)
    # Protect inline code spans first so `*`/`_` inside them isn't parsed as emphasis.
    codes = []

    def _stash(m):
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    t = re.sub(r"`([^`]+)`", _stash, t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    t = re.sub(r"\x00(\d+)\x00",
               lambda m: '<font face="Courier" size="8.3" color="#0f4c81">%s</font>' % codes[int(m.group(1))],
               t)
    return t


def make_table(rows, widths):
    data = []
    for i, row in enumerate(rows):
        st = cell_hdr if i == 0 else cell
        data.append([Paragraph(inline(c), st) for c in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
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
    # header row text needs white — rebuild header cells with white color
    hdr_white = ParagraphStyle("CellHW", parent=cell_hdr, textColor=HexColor("#ffffff"))
    data[0] = [Paragraph(inline(c), hdr_white) for c in rows[0]]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
                        topMargin=15 * mm, bottomMargin=15 * mm,
                        title="Dhruv's AI Coding Workflow", author="Dhruv Nigam")
story = []
avail = A4[0] - 32 * mm

lines = open(SRC).read().splitlines()
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("```"):
        block = []
        i += 1
        while i < len(lines) and not lines[i].startswith("```"):
            block.append(lines[i])
            i += 1
        story.append(Preformatted("\n".join(block), code_style))
    elif line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-|:]+\|$", lines[i + 1]):
        rows = [[c.strip() for c in line.strip("|").split("|")]]
        i += 2
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([c.strip() for c in lines[i].strip("|").split("|")])
            i += 1
        n = len(rows[0])
        if n == 5:  # skills table: #, Skill, Replaces, Core tenets, Key mechanics
            widths = [avail * w for w in (0.045, 0.14, 0.13, 0.09, 0.595)]
        elif n == 3:
            widths = [avail * w for w in (0.16, 0.42, 0.42)]
        else:
            widths = [avail / n] * n
        story.append(Spacer(1, 3))
        story.append(make_table(rows, widths))
        story.append(Spacer(1, 6))
        continue
    elif line.startswith("# "):
        story.append(Paragraph(inline(line[2:]), h1))
    elif line.startswith("## "):
        story.append(Paragraph(inline(line[3:]), h2))
    elif line.startswith("### "):
        story.append(Paragraph(inline(line[4:]), h3))
    elif line.strip() == "---":
        story.append(HRFlowable(width="100%", thickness=0.6, color=HexColor("#c9cedb"),
                                spaceBefore=8, spaceAfter=8))
    elif line.startswith("- "):
        story.append(Paragraph(inline(line[2:]), bullet, bulletText="•"))
    elif line.startswith("\\* "):
        story.append(Paragraph(inline(line[2:]), meta))
    elif line.startswith("**") and line.rstrip().endswith(("**", "**:")) is False and line.startswith("**Version**") is False and False:
        pass
    elif line.strip() == "":
        story.append(Spacer(1, 2))
    else:
        st = meta if line.startswith("**Version**") or line.startswith("**Built from**") or line.startswith("**Structure**") else body
        story.append(Paragraph(inline(line), st))
    i += 1

doc.build(story)
print("wrote", OUT)
