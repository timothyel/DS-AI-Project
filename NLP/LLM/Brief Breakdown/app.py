import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

genai.configure(api_key=api_key)

st.set_page_config(page_title="Brief Breakdown Assistant", layout="wide")

st.title("📋 Digital Agency Brief Assistant")
st.markdown("Masukkan **Client Brief**, lalu pilih jenis breakdown yang ingin dihasilkan:")

client_brief = st.text_area("✍️ Client Brief", height=250, placeholder="Contoh: Klien ingin meningkatkan awareness produk skincare baru untuk Gen Z di TikTok dan Instagram...")

brief_type = st.selectbox(
    "🧩 Pilih jenis turunan brief yang ingin dihasilkan:",
    (
        "Creative Brief",
        "Sub-Creative Brief (Production, Visual, Copywriting, dll)",
        "Media Brief",
        "Sub-Media Brief (Platform, Budgeting, KPI)"
    )
)

generate = st.button("🚀 Proses Brief")

if generate:
    if not client_brief.strip():
        st.warning("⚠️ Mohon masukkan Client Brief terlebih dahulu.")
    else:
        with st.spinner("🔄 Memproses brief dengan Gemini..."):

            prompt = f"""
Kamu adalah strategic planner berpengalaman. Berdasarkan brief klien di bawah, buatlah {brief_type} secara jelas dan terstruktur.

Jika ada informasi yang tidak disebutkan, tulis 'Tidak disebutkan'.

=== Client Brief ===
{client_brief.strip()}
"""

            try:
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(prompt)

                st.success(f"Hasil breakdown untuk **{brief_type}**:")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ Gagal memproses Gemini API:\n\n{str(e)}")
``
