import streamlit as st
from io import BytesIO
from PyPDF2 import PdfReader

# Import fungsi NLP dari nlp_utils.py
from nlp_utils import (
    extract_keywords,
    compute_similarity,
    compute_similarity_per_point
)

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="ATS CV Checker", layout="wide")
st.title("ATS Resume Scoring")
st.markdown(
    "Upload your CV (PDF) and enter the job description to check compatibility"
)

# Upload CV
uploaded_file = st.file_uploader("📄 Upload your CV (format PDF)", type=["pdf"])

# Input Job Description
job_desc = st.text_area("💼 Masukkan Job Description", height=250)

# Fungsi untuk ekstraksi teks dari PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

# Proses jika file dan JD tersedia
if uploaded_file and job_desc:
    if st.button("🔍 Cek Kecocokan"):
        try:
            with st.spinner("📄 Mengekstrak isi CV..."):
                cv_text = extract_text_from_pdf(uploaded_file)

            with st.spinner("Analyzing Resume"):
                keywords_cv = extract_keywords(cv_text)
                keywords_jd = extract_keywords(job_desc)
                overall_score = compute_similarity(cv_text, job_desc)
                per_point_scores = compute_similarity_per_point(cv_text, job_desc)

            # ========== Ringkasan ==========
            st.subheader("✅ Summary")

            color = "green" if overall_score >= 70 else "orange" if overall_score >= 40 else "red"
            st.markdown(
                f"""
                <div style='font-size:24px; font-weight:bold;'>
                   Overall Matching Score:
                    <span style='color:{color}'>{overall_score}%</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            # st.markdown(f"- **Jumlah Poin CV yang dianalisis:** `{len(per_point_scores)}`")

            # ========== Keyword Extraction ==========
            # st.subheader("📌 Keyword Utama")
            # col1, col2 = st.columns(2)
            # with col1:
            #     st.markdown("**Dari CV:**")
            #     st.write(", ".join(keywords_cv[:20]))
            # with col2:
            #     st.markdown("**Dari JD:**")
            #     st.write(", ".join(keywords_jd[:20]))

            # ========== Per Poin Similarity ==========
            # st.subheader("🔍 Analisis Per Poin (CV vs JD)")
            # for text, score in per_point_scores:
            #     point_color = "green" if score >= 70 else "orange" if score >= 40 else "red"
            #     st.markdown(
            #         f"<div style='font-size:18px;'>"
            #         f"<span style='color:{point_color}; font-weight:bold'>{score}%</span> — {text}"
            #         f"</div>",
            #         unsafe_allow_html=True
            #     )

        except Exception as e:
            st.error(f"❌ Gagal memproses file: {e}")
