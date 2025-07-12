import streamlit as st
import google.generativeai as genai
import markdown
from input_section import get_client_brief_ui
from download_utils import generate_pdf_download_button

# ==== Konfigurasi ====
st.set_page_config(page_title="Brief Breakdown Assistant", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ==== Init session state ====
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "processing" not in st.session_state:
    st.session_state.processing = False
if "full_type" not in st.session_state:
    st.session_state.full_type = ""

# ==== Multibahasa UI ====
LANGUAGES = {
    "EN": {
        "title": "📋 Digital Agency Brief Assistant",
        "description": "Enter the **Client Brief**, then select the type of breakdown you want to generate:",
        "input_label": "✍️ Client Brief",
        "placeholder": "Example: The client wants to increase awareness for a new skincare product targeting Gen Z on TikTok and Instagram...",
        "dropdown_label": "🧩 Select breakdown type:",
        "sub_label": "🔸 Select sub-category:",
        "output_lang_label": "🗣️ Output Language",
        "button": "🚀 Generate Brief",
        "warning": "⚠️ Please enter a Client Brief first.",
        "processing": "Processing brief...",
        "brief_type": "📎 **Brief Type**",
        "output": "🧠 **Generated Brief:**"
    },
    "ID": {
        "title": "📋 Asisten Brief Agensi Digital",
        "description": "Masukkan **Client Brief**, lalu pilih jenis breakdown yang ingin dihasilkan:",
        "input_label": "✍️ Client Brief",
        "placeholder": "Contoh: Klien ingin meningkatkan awareness produk skincare baru untuk Gen Z di TikTok dan Instagram...",
        "dropdown_label": "🧩 Pilih jenis breakdown:",
        "sub_label": "🔸 Pilih sub-kategori:",
        "output_lang_label": "🗣️ Pilih Bahasa Output",
        "button": "🚀 Proses Brief",
        "warning": "⚠️ Mohon masukkan Client Brief terlebih dahulu.",
        "processing": "Memproses brief...",
        "brief_type": "📎 **Jenis Brief**",
        "output": "🧠 **Brief yang Dihasilkan:**"
    }
}

# ==== Prompt Builder ====
def get_prompt(full_type, brief, output_lang):
    language_instruction = {
        "English": "Please write the output in English.",
        "Bahasa Indonesia": "Tulis hasil brief ini dalam Bahasa Indonesia."
    }

    templates = {
        "Creative Brief": f"""You are a creative strategist. Create a **Creative Brief** with:
- Background
- Objectives
- Target Audience
- Key Message
- Tone & Manner
- Deliverables
- Timeline

Client Brief:
{brief}
""",
        "Sub-Creative Brief - Production": f"""You are a production lead. Create a **Production Brief**:
- Format & Duration
- Shooting Needs
- Talent & Location
- Technical Notes
- Timeline

Client Brief:
{brief}
""",
        "Sub-Creative Brief - Visual": f"""You are a visual designer. Create a **Visual Direction Brief**:
- Visual Style
- Colors & Fonts
- Moodboard
- Asset Guidelines

Client Brief:
{brief}
""",
        "Sub-Creative Brief - Copywriting": f"""You are a copywriter. Create a **Copywriting Brief**:
- Key Messages
- Tone of Voice
- Must-use Phrases
- Platform-specific Adjustments

Client Brief:
{brief}
""",
        "Media Brief": f"""You are a media strategist. Create a **Media Brief**:
Please write it in a clean format using bullet points 
- Recommended Channels
- Budget Plan 
- Targeting Strategy
- KPI & Measurement

Client Brief:
{brief}
""",
        "Sub-Media Brief - Platform": f"""You are a digital planner. Create a **Platform Brief**:
- Platform Choices
- Rationale
- Format Suggestions
- Organic vs Paid

Client Brief:
{brief}
""",
        "Sub-Media Brief - Budgeting": f"""You are a media buyer. Create a **Budget Brief**:
- Total & Per-Channel Budget
- Efficiency Estimates
- Optimization Plan

Client Brief:
{brief}
""",
        "Sub-Media Brief - KPI": f"""You are a strategist. Create a **KPI Brief**:
- Main & Supporting KPIs
- Benchmarks
- Attribution Plan
- Success Criteria

Client Brief:
{brief}
"""
    }

    return templates.get(full_type, f"Generate a {full_type}:\n{brief}") + "\n\n" + language_instruction[output_lang]

# ==== UI ====
lang_code = st.radio("🌐 Language", ["EN", "ID"], horizontal=True)
T = LANGUAGES[lang_code]

st.title(T["title"])
st.markdown(T["description"])

client_brief = get_client_brief_ui(T["input_label"], T["placeholder"])
brief_type = st.selectbox(T["dropdown_label"], ["Creative Brief", "Sub-Creative Brief", "Media Brief", "Sub-Media Brief"])
sub_map = {
    "Sub-Creative Brief": ["Production", "Visual", "Copywriting"],
    "Sub-Media Brief": ["Platform", "Budgeting", "KPI"]
}
selected_sub = st.selectbox(T["sub_label"], sub_map[brief_type]) if brief_type in sub_map else None
output_lang = st.radio(T["output_lang_label"], ["English", "Bahasa Indonesia"], horizontal=True)

# ==== Tampilkan processing indicator ====
if st.session_state.processing:
    st.info(T["processing"])

# ==== Tampilkan hasil sebelumnya jika ada ====
if st.session_state.generated_text:
    st.markdown(f"{T['brief_type']}: **{st.session_state.full_type}**")
    st.markdown(T["output"])
    html_output = markdown.markdown(st.session_state.generated_text)
    st.markdown(f"<div style='font-size:14px; line-height:1.7;'>{html_output}</div>", unsafe_allow_html=True)
    generate_pdf_download_button(st.session_state.generated_text, filename=f"{st.session_state.full_type.replace(' ', '_').lower()}.pdf")

# ==== Tombol Generate ====
if st.button(T["button"]):
    if not client_brief.strip():
        st.warning(T["warning"])
    else:
        st.session_state.processing = True
        full_type = f"{brief_type} - {selected_sub}" if selected_sub else brief_type
        prompt = get_prompt(full_type, client_brief.strip(), output_lang)

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            st.session_state.generated_text = response.text
            st.session_state.full_type = full_type
        except Exception as e:
            st.error(f"❌ Failed to generate content:\n\n{str(e)}")
        finally:
            st.session_state.processing = False
