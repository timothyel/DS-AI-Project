import streamlit as st
import io
from fpdf import FPDF
import html2text

def replace_unicode_safe(text):
    return (
        text.replace('\u2013', '-')   # en dash
            .replace('\u2014', '--')  # em dash
            .replace('\u2018', "'")   # left single quote
            .replace('\u2019', "'")   # right single quote
            .replace('\u201c', '"')   # left double quote
            .replace('\u201d', '"')   # right double quote
    )

def generate_pdf_download_button(text, filename="brief_output.pdf"):
    import html2text

    text = replace_unicode_safe(text)

    # Konversi dari HTML ke plain text
    text_maker = html2text.HTML2Text()
    text_maker.body_width = 0
    plain_text = text_maker.handle(text)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in plain_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="📥 Download as PDF",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf"
    )
