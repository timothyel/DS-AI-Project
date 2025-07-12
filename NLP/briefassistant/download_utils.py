import streamlit as st
import pdfkit
import io

def generate_pdf_download_button_from_html(html_content, filename="generated_brief.pdf"):
    try:
        pdf_bytes = pdfkit.from_string(html_content, False)
        pdf_buffer = io.BytesIO(pdf_bytes)
        st.download_button(
            label="📥 Download Generated Brief as PDF",
            data=pdf_buffer,
            file_name=filename,
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"PDF generation failed: {str(e)}")
