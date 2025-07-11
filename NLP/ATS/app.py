import streamlit as st
from nlp_utils import extract_keywords, compute_similarity, compute_similarity_per_point

st.set_page_config(page_title="ATS CV Checker", layout="wide")

st.title("🧠 ATS CV vs Job Description Checker")
st.markdown(
    "Unggah CV kamu (dalam format .txt) dan masukkan Job Description untuk melihat seberapa cocok konten CV dengan JD target."
)

# Upload CV
uploaded_file = st.file_uploader("📄 Upload CV kamu (format .txt)", type=["txt"])

# Input manual JD
job_desc = st.text_area("💼 Masukkan Job Description", height=250)

if uploaded_file and job_desc:
    if uploaded_file.type == "text/plain":
        cv_text = uploaded_file.read().decode("utf-8")
    else:
        st.error("Hanya file .txt yang didukung saat ini.")
        st.stop()

    with st.spinner("🔍 Menganalisis konten CV..."):
        # Analisis keyword & similarity
        keywords_cv = extract_keywords(cv_text)
        keywords_jd = extract_keywords(job_desc)
        overall_score = compute_similarity(cv_text, job_desc)
        per_point_scores = compute_similarity_per_point(cv_text, job_desc)

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
