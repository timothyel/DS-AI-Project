from fpdf import FPDF
import streamlit as st
import io
import re

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Generated Brief", ln=True, align='C')
        self.ln(5)

    def add_body(self, text):
        self.set_font("Arial", size=12)
        lines = text.split("\n")
        for line in lines:
            original_line = line

            # Ubah **bold** jadi uppercase
            line = re.sub(r"\*\*(.*?)\*\*", lambda m: m.group(1).upper(), line)

            # Deteksi indentasi dan buat spacing manual
            indent_level = (len(original_line) - len(original_line.lstrip(' '))) // 2
            indent_space = " " * (indent_level * 4)

            stripped = line.strip()

            # Bullet points
            if stripped.startswith(("*", "-")):
                line = indent_space + "• " + stripped[1:].strip()
            elif stripped == "":
                line = ""
            else:
                line = indent_space + line.strip()

            # Encode aman ke latin-1
            safe_line = line.encode('latin-1', 'replace').decode('latin-1')

            self.multi_cell(0, 8, safe_line)
            if stripped == "":
                self.ln(1)  # Tambah spasi antar paragraf

def generate_pdf_download_button(text, filename="brief_output.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.add_body(text)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_buffer = io.BytesIO(pdf_bytes)

    st.download_button(
        label="📄 Download as PDF",
        data=pdf_buffer,
        file_name=filename,
        mime="application/pdf"
    )
