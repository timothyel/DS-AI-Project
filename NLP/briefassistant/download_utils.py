import streamlit as st
import pdfkit

def generate_pdf_download_button(html_string, filename="brief_output.pdf"):
    try:
        # Tentukan path ke wkhtmltopdf
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Sesuaikan dengan lokasimu
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        # Generate PDF
        pdf_bytes = pdfkit.from_string(html_string, False, configuration=config)

        # Tombol download
        st.download_button(
            label="📄 Download as PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"PDF generation failed: {e}")
