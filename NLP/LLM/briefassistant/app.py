import streamlit as st
import openai
import os

# Set your API Key (bisa juga pakai st.secrets atau dotenv di production)
openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Brief Breakdown Assistant", layout="wide")

st.title("📋 Digital Agency Brief Assistant")
st.markdown("Masukkan **Client Brief**, lalu pilih jenis breakdown yang ingin dihasilkan:")

# Input: Client Brief
client_brief = st.text_area("✍️ Client Brief", height=250, placeholder="Contoh: Klien ingin meningkatkan awareness produk skincare baru untuk Gen Z di TikTok dan Instagram...")

# Dropdown: Jenis Turunan Brief
brief_type = st.selectbox(
    "🧩 Pilih jenis turunan brief yang ingin dihasilkan:",
    (
        "Creative Brief",
        "Sub-Creative Brief (Production, Visual, Copywriting, dll)",
        "Media Brief",
        "Sub-Media Brief (Platform, Budgeting, KPI)"
    )
)

# Tombol generate
generate = st.button("🚀 Proses Brief")

if generate:
    if not client_brief.strip():
        st.warning("⚠️ Mohon masukkan Client Brief terlebih dahulu.")
    else:
        with st.spinner("🔄 Memproses brief dengan LLM..."):

            # Format prompt sesuai pilihan
            system_prompt = f"""
Kamu adalah seorang strategic planner berpengalaman di agensi digital. Berdasarkan brief dari klien, buatlah {brief_type} yang terstruktur dan realistis.

Jika informasi tidak tersedia dalam brief, cukup tulis "Tidak disebutkan" tanpa mengarang.

Formatkan output seperti ini:

=== {brief_type.upper()} ===
1. Objective:
2. Target Audience:
3. Key Insight:
4. Strategic Direction:
5. Channel / Asset (jika relevan):
6. Tambahan lainnya sesuai konteks
"""

            messages = [
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": client_brief.strip()}
            ]

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.6,
                    max_tokens=1000,
                )
                result = response['choices'][0]['message']['content']
                st.success(f"Hasil breakdown untuk **{brief_type}**:")
                st.markdown("---")
                st.markdown(result)

            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat memanggil API:\n\n{str(e)}")
