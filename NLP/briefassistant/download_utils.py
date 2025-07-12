from fpdf import FPDF
import io
import re

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Generated Brief", ln=True, align='C')
        self.ln(10)

    def add_markdown(self, text):
        self.set_font("Arial", size=12)
        lines = text.split("\n")
        for line in lines:
            # Bold Markdown
            line = re.sub(r"\*\*(.*?)\*\*", r"\1".upper(), line)
            # Bullet points
            if line.strip().startswith("*"):
                self.cell(5)
                line = line.replace("*", "•", 1)
            self.multi_cell(0, 8, line)

def generate_pdf(text):
    pdf = PDF()
    pdf.add_page()
    pdf.add_markdown(text)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
