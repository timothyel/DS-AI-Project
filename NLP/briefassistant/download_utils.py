from fpdf import FPDF
import streamlit as st
import io

def generate_pdf_download_button(text, filename="brief_output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Pastikan karakter bisa dikonversi ke latin-1
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    lines = safe_text.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)

    # ✅ Output sebagai string, lalu encode ke bytes dan simpan di buffer
    pdf_bytes = pdf.output(dest="S").encode('latin-1')
    buffer = io.BytesIO(pdf_bytes)

    # Tombol download
    st.download_button(
        label="📥 Download Generated Brief as PDF",
        data=buffer,
        file_name=filename,
        mime="application/pdf"
    )
