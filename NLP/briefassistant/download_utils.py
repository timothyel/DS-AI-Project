import streamlit as st
import io
from weasyprint import HTML

def generate_pdf_download_button_from_html(html_content: str, filename="brief_output.pdf"):
    # Generate PDF from HTML string
    pdf_file = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)

    # Show download button
    st.download_button(
        label="📄 Download as PDF",
        data=pdf_file,
        file_name=filename,
        mime="application/pdf"
    )
