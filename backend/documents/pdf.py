"""PDF rendering for generated documents (reportlab platypus).

The resume renderer accepts an optional `style` dict (set by the Refine Agent
chat) — currently {"accent": "#RRGGBB"} — so users can restyle the PDF.
"""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

_styles = getSampleStyleSheet()

DEFAULT_ACCENT = "#3b4bd8"


def _accent(style: dict | None):
    raw = (style or {}).get("accent") or DEFAULT_ACCENT
    try:
        return colors.HexColor(raw)
    except Exception:  # noqa: BLE001 — bad user-supplied color falls back safely
        return colors.HexColor(DEFAULT_ACCENT)


def _doc(buffer):
    return SimpleDocTemplate(
        buffer, pagesize=LETTER, topMargin=0.6 * inch, bottomMargin=0.6 * inch
    )


def _esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _section(story, title, accent):
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            title,
            ParagraphStyle(
                "sec",
                parent=_styles["Heading2"],
                fontSize=10.5,
                textColor=accent,
                spaceBefore=0,
                spaceAfter=1,
                letterSpacing=1,
            ),
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=accent, spaceAfter=5))


def render_resume_pdf(
    full_name: str, contact_line: str, sections: dict, style: dict | None = None
) -> bytes:
    accent = _accent(style)
    name_style = ParagraphStyle(
        "name", parent=_styles["Heading1"], fontSize=20, alignment=1,
        textColor=accent, spaceAfter=2,
    )
    contact_style = ParagraphStyle(
        "contact", parent=_styles["BodyText"], fontSize=9, alignment=1,
        textColor=colors.HexColor("#555555"), spaceAfter=2,
    )
    body = ParagraphStyle("body", parent=_styles["BodyText"], fontSize=9.5, leading=13)
    head = ParagraphStyle("head", parent=body, spaceBefore=3)

    story = [Paragraph(_esc(full_name or "Resume"), name_style)]
    if contact_line:
        story.append(Paragraph(_esc(contact_line), contact_style))
    story.append(HRFlowable(width="100%", thickness=2, color=accent, spaceAfter=2))

    if sections.get("summary"):
        _section(story, "SUMMARY", accent)
        story.append(Paragraph(_esc(sections["summary"]), body))
    if sections.get("skills"):
        _section(story, "SKILLS", accent)
        story.append(Paragraph(_esc("  •  ".join(sections["skills"])), body))
    if sections.get("experience"):
        _section(story, "EXPERIENCE", accent)
        for exp in sections["experience"]:
            title = " — ".join(p for p in [exp.get("title"), exp.get("company")] if p)
            duration = f" <font color='#777777'>({_esc(exp['duration'])})</font>" if exp.get("duration") else ""
            story.append(Paragraph(f"<b>{_esc(title)}</b>{duration}", head))
            story.append(
                Paragraph("<br/>".join("• " + _esc(b) for b in exp.get("bullets", [])), body)
            )
    if sections.get("projects"):
        _section(story, "PROJECTS", accent)
        for proj in sections["projects"]:
            tech = f" <font color='#777777'>({_esc(', '.join(proj['technologies']))})</font>" if proj.get("technologies") else ""
            story.append(Paragraph(f"<b>{_esc(proj.get('name', ''))}</b>{tech}", head))
            story.append(
                Paragraph("<br/>".join("• " + _esc(b) for b in proj.get("bullets", [])), body)
            )
    if sections.get("education"):
        _section(story, "EDUCATION", accent)
        for edu in sections["education"]:
            line = " — ".join(_esc(p) for p in [edu.get("degree"), edu.get("institution")] if p)
            if edu.get("year"):
                line += f" <font color='#777777'>({_esc(edu['year'])})</font>"
            story.append(Paragraph(line, body))

    buf = BytesIO()
    _doc(buf).build(story)
    return buf.getvalue()


def render_cover_letter_pdf(
    full_name: str, job_title: str, company: str, text: str, style: dict | None = None
) -> bytes:
    accent = _accent(style)
    name_style = ParagraphStyle(
        "clname", parent=_styles["Heading1"], fontSize=16, textColor=accent, spaceAfter=1
    )
    sub = ParagraphStyle(
        "clsub", parent=_styles["BodyText"], fontSize=9.5,
        textColor=colors.HexColor("#555555"),
    )
    body = ParagraphStyle("clbody", parent=_styles["BodyText"], fontSize=10, leading=14.5)

    story = [
        Paragraph(_esc(full_name), name_style),
        Paragraph(_esc(f"Application: {job_title} — {company}"), sub),
        HRFlowable(width="100%", thickness=1.5, color=accent, spaceBefore=4, spaceAfter=14),
    ]
    for para in text.split("\n\n"):
        story.append(Paragraph(_esc(para).replace("\n", "<br/>"), body))
        story.append(Spacer(1, 9))

    buf = BytesIO()
    _doc(buf).build(story)
    return buf.getvalue()
