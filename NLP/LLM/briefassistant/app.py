import streamlit as st

st.set_page_config(page_title="Brief Breakdown Assistant", layout="wide")

# Language selection
language = st.selectbox("🌐 Select Language / Pilih Bahasa", ("English", "Bahasa Indonesia"))

# Text dictionary
text = {
    "English": {
        "title": "📋 Digital Agency Brief Assistant",
        "description": "Enter the **Client Brief**, then select the type of breakdown you want to generate:",
        "input_label": "✍️ Client Brief",
        "placeholder": "Example: The client wants to increase awareness for a new skincare product targeting Gen Z on TikTok and Instagram...",
        "dropdown_label": "🧩 Select the type of breakdown to generate:",
        "button": "🚀 Generate Brief",
        "warning": "⚠️ Please enter a Client Brief first.",
        "processing": "🔄 Processing brief... (Connect your LLM API here)",
        "brief_type": "📎 **Brief Type**",
        "client_brief": "📤 **Client Brief:**",
        "output_placeholder": "🧠 **[The generated brief will appear here after the API call]**"
    },
    "Bahasa Indonesia": {
        "title": "📋 Asisten Brief Agensi Digital",
        "description": "Masukkan **Client Brief**, lalu pilih jenis breakdown yang ingin dihasilkan:",
        "input_label": "✍️ Client Brief",
        "placeholder": "Contoh: Klien ingin meningkatkan awareness produk skincare baru untuk Gen Z di TikTok dan Instagram...",
        "dropdown_label": "🧩 Pilih jenis turunan brief yang ingin dihasilkan:",
        "button": "🚀 Proses Brief",
        "warning": "⚠️ Mohon masukkan Client Brief terlebih dahulu.",
        "processing": "🔄 Brief sedang diproses... (Hubungkan ke API LLM di sini)",
        "brief_type": "📎 **Jenis Brief**",
        "client_brief": "📤 **Client Brief:**",
        "output_placeholder": "🧠 **[Di sini akan muncul hasil dari API kamu nanti]**"
    }
}

# Apply selected language
t = text[language]

# UI
st.title(t["title"])
st.markdown(t["description"])

client_brief = st.text_area(
    t["input_label"],
    height=250,
    placeholder=t["placeholder"]
)

brief_type = st.selectbox(
    t["dropdown_label"],
    (
        "Creative Brief",
        "Sub-Creative Brief (Production, Visual, Copywriting, etc.)",
        "Media Brief",
        "Sub-Media Brief (Platform, Budgeting, KPIs)"
    )
)

generate = st.button(t["button"])

if generate:
    if not client_brief.strip():
        st.warning(t["warning"])
    else:
        st.info(t["processing"])
        st.markdown("---")
        st.markdown(f"{t['brief_type']}: {brief_type}")
        st.markdown(t["client_brief"])
        st.code(client_brief, language="markdown")
        st.markdown(t["output_placeholder"])
