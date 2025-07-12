from fpdf import FPDF
import streamlit as st
import io

def generate_pdf_download_button(text, filename="brief_output.pdf"):
    # PDF Generation
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Replace special characters for safety
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    lines = safe_text.split('\n')

    for line in lines:
        pdf.multi_cell(0, 10, line)

    # Output to buffer
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    # Download button
    st.download_button(
        label="📥 Download Generated Brief as PDF",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf"
    )
