from fpdf import FPDF
import streamlit as st
import io
import re

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Generated Brief", ln=True, align='C')
        self.ln(10)

    def add_body(self, text):
        self.set_font("Arial", size=12)
        lines = text.split("\n")
        for line in lines:
            # Ubah **bold** jadi uppercase
            line = re.sub(r"\*\*(.*?)\*\*", lambda m: m.group(1).upper(), line)

            # Ganti bullet (* atau -) dengan •
            if line.strip().startswith(("*", "-")):
                line = "• " + line.strip()[1:].strip()

            # Replace tab dengan spasi
            line = line.replace("\t", "    ")

            # Amankan encoding
            safe_line = line.encode('latin-1', 'replace').decode('latin-1')
            self.multi_cell(0, 8, safe_line)

def generate_pdf_download_button(text, filename="brief_output.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.add_body(text)

    # 👉 Fix: Gunakan output(dest='S') lalu encode ke latin-1
    pdf_bytes = pdf.output(dest='S').encode('latin-1')  # str → bytes
    pdf_buffer = io.BytesIO(pdf_bytes)

    st.download_button(
        label="📄 Download as PDF",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf"
    )
