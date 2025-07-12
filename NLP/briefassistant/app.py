import streamlit as st
import google.generativeai as genai
import markdown
from input_section import get_client_brief_ui
from download_utils import generate_pdf_download_button

# ==== Config & Setup ====
st.set_page_config(page_title="Brief Breakdown Assistant", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ==== Init Session State ====
st.session_state.setdefault("generated_text", "")
st.session_state.setdefault("processing", False)
st.session_state.setdefault("full_type", "")

# ==== Multilang UI Dict ====
LANG = {
    "EN": {
        "title": "📋 Digital Agency Brief Assistant",
        "desc": "Enter the **Client Brief**, then select the type of breakdown you want to generate:",
        "input": "✍️ Client Brief",
        "placeholder": "Example: The client wants to increase awareness for a new skincare product targeting Gen Z on TikTok and Instagram...",
        "type": "🧩 Select breakdown type:",
        "sub": "🔸 Select sub-category:",
        "lang": "🗣️ Output Language",
        "btn": "🚀 Generate Brief",
        "warn": "⚠️ Please enter a Client Brief first.",
        "loading": "Processing brief...",
        "label_type": "📎 **Brief Type**",
        "label_output": "🧠 **Generated Brief:**"
    },
    "ID": {
        "title": "📋 Asisten Brief Agensi Digital",
        "desc": "Masukkan **Client Brief**, lalu pilih jenis breakdown yang ingin dihasilkan:",
        "input": "✍️ Client Brief",
        "placeholder": "Contoh: Klien ingin meningkatkan awareness produk skincare baru untuk Gen Z di TikTok dan Instagram...",
        "type": "🧩 Pilih jenis breakdown:",
        "sub": "🔸 Pilih sub-kategori:",
        "lang": "🗣️ Pilih Bahasa Output",
        "btn": "🚀 Proses Brief",
        "warn": "⚠️ Mohon masukkan Client Brief terlebih dahulu.",
        "loading": "Memproses brief...",
        "label_type": "📎 **Jenis Brief**",
        "label_output": "🧠 **Brief yang Dihasilkan:**"
    }
}

# ==== Prompt Template ====
def build_prompt(full_type, brief, output_lang):
    instruksi = {
        "English": "Please write the output in English.",
        "Bahasa Indonesia": "Tulis hasil brief ini dalam Bahasa Indonesia."
    }
    isi = {
        "Creative Brief": """
You are a creative strategist. Create a **Creative Brief** with:
- Background
- Objectives
- Target Audience
- Key Message
- Tone & Manner
- Deliverables
- Timeline
""",
        "Sub-Creative Brief - Production": """
You are a production lead. Create a **Production Brief**:
- Format & Duration
- Shooting Needs
- Talent & Location
- Technical Notes
- Timeline
""",
        "Sub-Creative Brief - Visual": """
You are a visual designer. Create a **Visual Direction Brief**:
- Visual Style
- Colors & Fonts
- Moodboard
- Asset Guidelines
""",
        "Sub-Creative Brief - Copywriting": """
You are a copywriter. Create a **Copywriting Brief**:
- Key Messages
- Tone of Voice
- Must-use Phrases
- Platform-specific Adjustments
""",
        "Media Brief": """
You are a media strategist. please create a clean format in bullet points Create a **Media Brief**:
- Recommended Channels
- Budget Plan 
- Targeting Strategy
- KPI & Measurement
""",
        "Sub-Media Brief - Platform": """
You are a digital planner. Create a **Platform Brief**:
- Platform Choices
- Rationale
- Format Suggestions
- Organic vs Paid
""",
        "Sub-Media Brief - Budgeting": """
You are a media buyer. Create a **Budget Brief**:
- Total & Per-Channel Budget
- Efficiency Estimates
- Optimization Plan
""",
        "Sub-Media Brief - KPI": """
You are a strategist. Create a **KPI Brief**:
- Main & Supporting KPIs
- Benchmarks
- Attribution Plan
- Success Criteria
"""
    }

    return f"{isi.get(full_type, f'Generate a {full_type}:')}\n\nClient Brief:\n{brief}\n\n{instruksi[output_lang]}"

# ==== UI ====
lang_choice = st.radio("🌐 Language", ["EN", "ID"], horizontal=True)
T = LANG[lang_choice]

st.title(T["title"])
st.markdown(T["desc"])

brief = get_client_brief_ui(T["input"], T["placeholder"])
brief_type = st.selectbox(T["type"], ["Creative Brief", "Sub-Creative Brief", "Media Brief", "Sub-Media Brief"])
sub_map = {
    "Sub-Creative Brief": ["Production", "Visual", "Copywriting"],
    "Sub-Media Brief": ["Platform", "Budgeting", "KPI"]
}
sub = st.selectbox(T["sub"], sub_map[brief_type]) if brief_type in sub_map else None
lang_out = st.radio(T["lang"], ["English", "Bahasa Indonesia"], horizontal=True)

# ==== Display previous output if exists ====
if st.session_state.processing:
    st.info(T["loading"])

if st.session_state.generated_text:
    st.markdown(f"{T['label_type']}: **{st.session_state.full_type}**")
    st.markdown(T["label_output"])
    html_out = markdown.markdown(st.session_state.generated_text)
    st.markdown(f"<div style='font-size:14px; line-height:1.7;'>{html_out}</div>", unsafe_allow_html=True)
    generate_pdf_download_button(st.session_state.generated_text, f"{st.session_state.full_type.replace(' ', '_').lower()}.pdf")

# ==== Generate Brief ====
if st.button(T["btn"]):
    if not brief.strip():
        st.warning(T["warn"])
    else:
        st.session_state.processing = True
        full_type = f"{brief_type} - {sub}" if sub else brief_type
        prompt = build_prompt(full_type, brief.strip(), lang_out)

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            result = model.generate_content(prompt)
            st.session_state.generated_text = result.text
            st.session_state.full_type = full_type
        except Exception as e:
            st.error(f"❌ Failed to generate content:\n\n{e}")
        finally:
            st.session_state.processing = False
