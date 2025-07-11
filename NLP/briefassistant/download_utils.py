import streamlit as st
import io
from fpdf import FPDF
import html2text

def generate_pdf_download_button(text, filename="brief_output.pdf"):
    # Konversi markdown/html ke plain text
    text_maker = html2text.HTML2Text()
    text_maker.body_width = 0
    plain_text = text_maker.handle(text)

    # ✅ Tambahkan ini agar karakter aneh diganti
    plain_text = plain_text.encode("latin-1", "replace").decode("latin-1")

    # PDF generation
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in plain_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Output ke string dan encode ke latin-1
    pdf_str = pdf.output(dest='S').encode('latin-1')
    pdf_buffer = io.BytesIO(pdf_str)

    st.download_button(
        label="📥 Download as PDF",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf"
    )
