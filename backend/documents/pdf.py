"""PDF rendering for generated documents (reportlab platypus)."""

from io import BytesIO

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

_styles = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=_styles["Heading1"], fontSize=16, spaceAfter=2)
H2 = ParagraphStyle("h2", parent=_styles["Heading2"], fontSize=11.5, spaceBefore=10, spaceAfter=3)
BODY = ParagraphStyle("body", parent=_styles["BodyText"], fontSize=9.5, leading=13)


def _doc(buffer):
    return SimpleDocTemplate(
        buffer, pagesize=LETTER, topMargin=0.7 * inch, bottomMargin=0.7 * inch
    )


def _esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_resume_pdf(full_name: str, contact_line: str, sections: dict) -> bytes:
    story = [Paragraph(_esc(full_name or "Resume"), H1)]
    if contact_line:
        story.append(Paragraph(_esc(contact_line), BODY))
    if sections.get("summary"):
        story += [Paragraph("SUMMARY", H2), Paragraph(_esc(sections["summary"]), BODY)]
    if sections.get("skills"):
        story += [Paragraph("SKILLS", H2), Paragraph(_esc(", ".join(sections["skills"])), BODY)]
    if sections.get("experience"):
        story.append(Paragraph("EXPERIENCE", H2))
        for exp in sections["experience"]:
            head = " — ".join(p for p in [exp.get("title"), exp.get("company")] if p)
            if exp.get("duration"):
                head += f" ({exp['duration']})"
            story.append(Paragraph(f"<b>{_esc(head)}</b>", BODY))
            story.append(
                Paragraph("<br/>".join("• " + _esc(b) for b in exp.get("bullets", [])), BODY)
            )
            story.append(Spacer(1, 4))
    if sections.get("projects"):
        story.append(Paragraph("PROJECTS", H2))
        for proj in sections["projects"]:
            head = proj.get("name", "")
            if proj.get("technologies"):
                head += f" ({', '.join(proj['technologies'])})"
            story.append(Paragraph(f"<b>{_esc(head)}</b>", BODY))
            story.append(
                Paragraph("<br/>".join("• " + _esc(b) for b in proj.get("bullets", [])), BODY)
            )
            story.append(Spacer(1, 4))
    if sections.get("education"):
        story.append(Paragraph("EDUCATION", H2))
        for edu in sections["education"]:
            line = " — ".join(p for p in [edu.get("degree"), edu.get("institution")] if p)
            if edu.get("year"):
                line += f" ({edu['year']})"
            story.append(Paragraph(_esc(line), BODY))

    buf = BytesIO()
    _doc(buf).build(story)
    return buf.getvalue()


def render_cover_letter_pdf(full_name: str, job_title: str, company: str, text: str) -> bytes:
    story = [
        Paragraph(_esc(full_name), H1),
        Paragraph(_esc(f"Application: {job_title} — {company}"), BODY),
        Spacer(1, 14),
    ]
    for para in text.split("\n\n"):
        story.append(Paragraph(_esc(para).replace("\n", "<br/>"), BODY))
        story.append(Spacer(1, 8))

    buf = BytesIO()
    _doc(buf).build(story)
    return buf.getvalue()
