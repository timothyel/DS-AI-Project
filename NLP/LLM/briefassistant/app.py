import streamlit as st

st.set_page_config(page_title="Brief Breakdown Assistant", layout="wide")

st.title("📋 Digital Agency Brief Assistant")
st.markdown("Masukkan **Client Brief**, lalu pilih jenis breakdown yang ingin dihasilkan:")

# Input: Client Brief
client_brief = st.text_area(
    "✍️ Client Brief",
    height=250,
    placeholder="Contoh: Klien ingin meningkatkan awareness produk skincare baru untuk Gen Z di TikTok dan Instagram..."
)

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

# Placeholder output
if generate:
    if not client_brief.strip():
        st.warning("⚠️ Mohon masukkan Client Brief terlebih dahulu.")
    else:
        st.info("🔄 Brief sedang diproses... (Hubungkan ke API LLM di sini)")
        st.markdown("---")
        st.markdown(f"📎 **Jenis Brief**: {brief_type}")
        st.markdown("📤 **Client Brief**:")
        st.code(client_brief, language="markdown")
        st.markdown("🧠 **[Di sini akan muncul hasil dari API kamu nanti]**")
