import streamlit as st
from nlp_utils import extract_keywords, compute_similarity, compute_similarity_per_point
from io import BytesIO
from PyPDF2 import PdfReader

st.set_page_config(page_title="ATS CV Checker", layout="wide")

st.title("🧠 ATS CV vs Job Description Checker")
st.markdown(
    "Unggah CV kamu (format `.pdf`) dan masukkan Job Description untuk melihat seberapa cocok konten CV dengan JD target."
)

# Upload CV
uploaded_file = st.file_uploader("📄 Upload CV kamu (format .pdf)", type=["pdf"])

# Input manual JD
job_desc = st.text_area("💼 Masukkan Job Description", height=250)

def extract_text_from_pdf(file):
    """Ekstrak teks dari PDF yang diunggah"""
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text

if uploaded_file and job_desc:
    if st.button("🔍 Cek Kecocokan"):
        try:
            with st.spinner("🔍 Membaca isi CV..."):
                cv_text = extract_text_from_pdf(uploaded_file)

            with st.spinner("🔍 Menganalisis konten CV..."):
                keywords_cv = extract_keywords(cv_text)
                keywords_jd = extract_keywords(job_desc)
                overall_score = compute_similarity(cv_text, job_desc)
                per_point_scores = compute_similarity_per_point(cv_text, jd_text=job_desc)

            st.subheader("✅ Ringkasan")
            st.markdown(f"- **Skor Kecocokan Keseluruhan:** `{overall_score}%`")
            st.markdown(f"- **Jumlah Poin CV yang dianalisis:** `{len(per_point_scores)}`")

            st.subheader("📌 Keyword Utama")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Dari CV:**")
                st.write(", ".join(keywords_cv[:20]))
            with col2:
                st.markdown("**Dari JD:**")
                st.write(", ".join(keywords_jd[:20]))

            st.subheader("🔍 Analisis Per Poin (CV vs JD)")
            for text, score in per_point_scores:
                color = "green" if score >= 70 else "orange" if score >= 40 else "red"
                st.markdown(f"<span style='color:{color}'>**{score}%**</span> — {text}", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Gagal membaca atau memproses PDF: {e}")
