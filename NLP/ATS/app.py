import streamlit as st
import nltk
# Download 'wordnet' for NLTK if not already downloaded
nltk.download('wordnet')
# Import custom NLP utility functions
from nlp_utils import extract_keywords, compute_similarity, compute_similarity_per_point

# Set Streamlit page configuration
st.set_page_config(page_title="ATS CV Checker", layout="wide")

# Main title of the application
st.title("🧠 ATS CV vs Job Description Checker")
# Markdown description for the user
st.markdown(
    "Unggah CV kamu (dalam format .txt) dan masukkan Job Description untuk melihat seberapa cocok konten CV dengan JD target."
)

# File uploader for the CV
uploaded_file = st.file_uploader("📄 Upload CV kamu (format .txt)", type=["txt"])

# Text area for manual Job Description input
job_desc = st.text_area("💼 Masukkan Job Description", height=250)

# Check if both CV and Job Description are provided
if uploaded_file and job_desc:
    # Check if the uploaded file is a plain text file
    if uploaded_file.type == "text/plain":
        # Decode the CV content from bytes to UTF-8 string
        cv_text = uploaded_file.read().decode("utf-8")
    else:
        # Display an error if the file type is not .txt
        st.error("Hanya file .txt yang didukung saat ini.")
        st.stop() # Stop execution if an unsupported file type is uploaded

    # Show a spinner while processing the CV content
    with st.spinner("🔍 Menganalisis konten CV..."):
        # Call NLP utility functions to analyze keywords and compute similarity
        keywords_cv = extract_keywords(cv_text)
        keywords_jd = extract_keywords(job_desc)
        overall_score = compute_similarity(cv_text, job_desc)
        per_point_scores = compute_similarity_per_point(cv_text, job_desc)

    # Display the summary section
    st.subheader("✅ Ringkasan")
    st.markdown(f"- **Skor Kecocokan Keseluruhan:** `{overall_score}%`")
    st.markdown(f"- **Jumlah Poin CV yang dianalisis:** `{len(per_point_scores)}`")

    # Display the Keyword Analysis section
    st.subheader("📌 Keyword Utama")
    col1, col2 = st.columns(2) # Create two columns for CV and JD keywords
    with col1:
        st.markdown("**Dari CV:**")
        # Display the top 20 keywords from the CV
        st.write(", ".join(keywords_cv[:20]))
    with col2:
        st.markdown("**Dari JD:**")
        # Display the top 20 keywords from the Job Description
        st.write(", ".join(keywords_jd[:20]))

    # Display the Per-Point Analysis section
    st.subheader("🔍 Analisis Per Poin (CV vs JD)")
    # Iterate through each point's score and text
    for text, score in per_point_scores:
        # Determine the color based on the score for visual feedback
        color = "green" if score >= 70 else "orange" if score >= 40 else "red"
        # Display the score and text with dynamic coloring
        st.markdown(f"<span style='color:{color}'>**{score}%**</span> — {text}", unsafe_allow_html=True)
