import streamlit as st
from io import BytesIO
from PyPDF2 import PdfReader

# Import fungsi NLP
from nlp_utils import (
    extract_keywords,
    compute_similarity,
    compute_similarity_per_point
)

# Konfigurasi halaman
st.set_page_config(page_title="ATS CV Checker", layout="wide")
st.title("🧠 ATS CV vs Job Description Checker")
st.markdown(
    "Unggah CV kamu dalam format **PDF**, lalu masukkan Job Description (JD) untuk melihat kecocokan konten CV dengan posisi yang ditargetkan."
)

# Upload CV
uploaded_file = st.file_uploader("📄 Upload CV kamu (format PDF)", type=["pdf"])

# Input Job Description
job_desc = st.text_area("💼 Masukkan Job Description", height=250)

# Fungsi untuk ekstrak teks dari PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

# Jika file dan JD sudah diisi
if uploaded_file and job_desc:
    if st.button("🔍 Cek Kecocokan"):
        try:
            with st.spinner("📄 Mengekstrak isi CV..."):
                cv_text = extract_text_from_pdf(uploaded_file)

            with st.spinner("🤖 Menganalisis konten..."):
                keywords_cv = extract_keywords(cv_text)
                keywords_jd = extract_keywords(job_desc)
                overall_score = compute_similarity(cv_text, job_desc)
                per_point_scores = compute_similarity_per_point(cv_text, job_desc)

            # Hasil Analisis
            st.subheader("✅ Ringkasan")
            st.markdown(f"- **Skor Kecocokan Keseluruhan:** `{overall_score}%`")
            st.markdown(f"- **Jumlah Poin CV yang dianalisis:** `{len(per_point_scores)}`")
            
            # # Per Poin Similarity
            # st.subheader("🔍 Analisis Per Poin (CV vs JD)")
            # for text, score in per_point_scores:
            #     color = "green" if score >= 70 else "orange" if score >= 40 else "red"
            #     st.markdown(
            #         f"<span style='color:{color}'>**{score}%**</span> — {text}",
            #         unsafe_allow_html=True
            #     )

        except Exception as e:
            st.error(f"❌ Gagal memproses file: {e}")
