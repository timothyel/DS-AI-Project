import streamlit as st
import io
from weasyprint import HTML

def generate_pdf_download_button_from_html(html_string, filename="brief_output.pdf"):
    try:
        # Convert HTML to PDF using WeasyPrint
        pdf_bytes = HTML(string=html_string).write_pdf()

        # Create download button
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"PDF generation failed: {e}")
