# tools/pdf_generator.py

from fpdf import FPDF
from datetime import datetime
import unicodedata
import io


class LegalPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'AI Legal Assistant - Official Report', border=False, ln=True, align='C')
        self.set_draw_color(60, 60, 120)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}  |  Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', align='C')


def sanitize_for_pdf(text: str) -> str:
    """Replace or remove characters not supported by Helvetica (latin-1)."""
    replacements = {
        '₹': 'Rs.',
        '–': '-',
        '—': '--',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2022': '-',
        '•': '-',
        '…': '...',
        '✔': '[OK]',
        '✗': '[X]',
        '★': '*',
        '→': '->',
        '©': '(c)',
        '®': '(R)',
        '™': '(TM)',
        '\u00a0': ' ',  # non-breaking space
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    # Strip any remaining non-latin-1 characters safely
    sanitized = []
    for ch in text:
        try:
            ch.encode('latin-1')
            sanitized.append(ch)
        except (UnicodeEncodeError, UnicodeDecodeError):
            normalized = unicodedata.normalize('NFKD', ch)
            ascii_ch = normalized.encode('ascii', 'ignore').decode('ascii')
            sanitized.append(ascii_ch if ascii_ch else ' ')
    return ''.join(sanitized)


def generate_legal_pdf(content: str) -> bytes:
    """
    Generates a professional, valid PDF from the legal assistant output.
    Returns clean bytes ready for Streamlit download.
    """
    pdf = LegalPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Document Title
    pdf.set_font('helvetica', 'B', 13)
    pdf.set_text_color(30, 30, 100)
    pdf.cell(0, 10, 'Legal Analysis & Documentation', ln=True)
    pdf.ln(3)

    # Reset text color
    pdf.set_text_color(0, 0, 0)

    # Sanitize and render content
    clean_content = content.replace("**", "").replace("###", "").replace("##", "").replace("#", "")
    clean_content = sanitize_for_pdf(clean_content)

    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 7, clean_content)

    # Write to BytesIO buffer — the correct way to get valid PDF bytes
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()
