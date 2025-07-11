import streamlit as st

st.set_page_config(page_title="Brief Breakdown Assistant", layout="wide")

# Language toggle
language = st.radio("🌐 Language", ["EN", "ID"], horizontal=True)

# Text dictionary
text = {
    "EN": {
        "title": "📋 Digital Agency Brief Assistant",
        "description": "Enter the **Client Brief**, then select the type of breakdown you want to generate:",
        "input_label": "✍️ Client Brief",
        "placeholder": "Example: The client wants to increase awareness for a new skincare product targeting Gen Z on TikTok and Instagram...",
        "dropdown_label": "🧩 Select the type of breakdown to generate:",
        "sub_label": "🔸 Select a sub-category:",
        "button": "🚀 Generate Brief",
        "warning": "⚠️ Please enter a Client Brief first.",
        "processing": "🔄 Processing brief... (Connect your LLM API here)",
        "brief_type": "📎 **Brief Type**",
        "client_brief": "📤 **Client Brief:**",
        "output_placeholder": "🧠 **[The generated brief will appear here after the API call]**"
    },
    "ID": {
        "title": "📋 Asisten Brief Agensi Digital",
        "description": "Masukkan **Client Brief**, lalu pilih jenis breakdown yang ingin dihasilkan:",
        "input_label": "✍️ Client Brief",
        "placeholder": "Contoh: Klien ingin meningkatkan awareness produk skincare baru untuk Gen Z di TikTok dan Instagram...",
        "dropdown_label": "🧩 Pilih jenis turunan brief yang ingin dihasilkan:",
        "sub_label": "🔸 Pilih sub-kategori:",
        "button": "🚀 Proses Brief",
        "warning": "⚠️ Mohon masukkan Client Brief terlebih dahulu.",
        "processing": "🔄 Brief sedang diproses... (Hubungkan ke API LLM di sini)",
        "brief_type": "📎 **Jenis Brief**",
        "client_brief": "📤 **Client Brief:**",
        "output_placeholder": "🧠 **[Di sini akan muncul hasil dari API kamu nanti]**"
    }
}

t = text[language]

# UI
st.title(t["title"])
st.markdown(t["description"])

client_brief = st.text_area(t["input_label"], height=250, placeholder=t["placeholder"])

brief_type = st.selectbox(
    t["dropdown_label"],
    (
        "Creative Brief",
        "Sub-Creative Brief",
        "Media Brief",
        "Sub-Media Brief"
    )
)

# Mapping sub-options
sub_options = {
    "Sub-Creative Brief": ["Production", "Visual", "Copywriting"],
    "Sub-Media Brief": ["Platform", "Budgeting", "KPI"]
}

selected_sub = None
if brief_type in sub_options:
    selected_sub = st.selectbox(t["sub_label"], sub_options[brief_type])

# Tombol generate
generate = st.button(t["button"])

if generate:
    if not client_brief.strip():
        st.warning(t["warning"])
    else:
        st.info(t["processing"])
        st.markdown("---")
        if selected_sub:
            full_brief = f"{brief_type} → {selected_sub}"
        else:
            full_brief = brief_type

        st.markdown(f"{t['brief_type']}: **{full_brief}**")
        st.markdown(t["client_brief"])
        st.code(client_brief, language="markdown")
        st.markdown(t["output_placeholder"])
