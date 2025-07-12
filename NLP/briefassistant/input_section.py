import streamlit as st
import fitz  # PyMuPDF

def get_client_brief_ui(label, placeholder):
    uploaded_file = st.file_uploader("📎 Upload Client Brief (PDF only)", type=["pdf"])
    brief_text = ""

    if uploaded_file is not None:
        try:
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                brief_text = "\n".join(page.get_text() for page in doc)
                st.success("✅ Text extracted from PDF successfully!")
        except Exception as e:
            st.error(f"❌ Failed to read PDF: {str(e)}")
    else:
        brief_text = st.text_area(label, height=250, placeholder=placeholder)

    return brief_text.strip()
