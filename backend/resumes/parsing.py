"""PDF text extraction: pdfplumber primary, pypdf fallback (master-plan §19)."""

import logging

logger = logging.getLogger(__name__)


class UnreadablePDFError(Exception):
    pass


def extract_pdf_text(django_file) -> str:
    text = ""
    try:
        import pdfplumber

        django_file.seek(0)
        with pdfplumber.open(django_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as exc:  # noqa: BLE001 — any pdfplumber failure falls through to pypdf
        logger.warning("pdfplumber failed: %s", exc)

    if len(text.strip()) < 50:
        try:
            from pypdf import PdfReader

            django_file.seek(0)
            reader = PdfReader(django_file)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:  # noqa: BLE001
            logger.warning("pypdf failed: %s", exc)

    if len(text.strip()) < 50:
        raise UnreadablePDFError(
            "We couldn't read text from this PDF. If it's a scanned image, "
            "please upload a text-based PDF."
        )
    return text
