import streamlit as st
import google.generativeai as genai
import markdown
import html

# ==== Konfigurasi ====
st.set_page_config(page_title="Brief Breakdown Assistant", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ==== Text Multibahasa ====
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

# ==== Prompt Templates ====
def get_prompt(full_type, brief, output_lang):
    language_instruction = {
        "English": "Please write the output in English. and make the font of your body paragraph in size of 14pt",
        "Bahasa Indonesia": "Tulis hasil brief ini dalam Bahasa Indonesia dan buat tulisan selain judul di ukuran 14pt."
    }

    templates = {
        "Creative Brief": f"""
You are a creative strategist in a digital agency. Create a **Creative Brief** from the following client input with clear structure, including:
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
        "Sub-Creative Brief - Production": f"""
You are a production lead in a creative team. Based on the brief below, create a **Production Brief** with:
- Format & Duration
- Shooting Needs
- Talent & Location
- Technical Notes
- Timeline

Client Brief:
{brief}
""",
        "Sub-Creative Brief - Visual": f"""
You are a visual designer. Turn the brief into a **Visual Direction Brief** covering:
- Visual Style
- Colors & Fonts
- Moodboard references
- Asset Guidelines

Client Brief:
{brief}
""",
        "Sub-Creative Brief - Copywriting": f"""
You are a senior copywriter. Create a **Copywriting Brief** including:
- Key Messages
- Tone of Voice
- Must-use Phrases
- Platform-specific Adjustments

Client Brief:
{brief}
""",
        "Media Brief": f"""
You are a media strategist. Generate a structured **Media Brief** containing:
- Recommended Channels
- Budget Plan
- Targeting Strategy
- KPI & Measurement

Client Brief:
{brief}
""",
        "Sub-Media Brief - Platform": f"""
You are a digital planner. Generate a **Platform Brief** including:
- Platform Choices
- Rationale
- Format Suggestions
- Organic vs Paid approach

Client Brief:
{brief}
""",
        "Sub-Media Brief - Budgeting": f"""
You are a performance media specialist. Make a **Media Budget Brief**:
- Total & Per-Channel Budget
- Efficiency Estimates
- Optimization Plan

Client Brief:
{brief}
""",
        "Sub-Media Brief - KPI": f"""
You are a data-driven strategist. Build a **KPI Brief** including:
- Main & Supporting KPIs
- Benchmarks
- Attribution Plan
- Success Criteria

Client Brief:
{brief}
"""
    }

    prompt = templates.get(full_type, f"""
You are a strategic planner at a digital agency. Based on the client brief below, generate a detailed **{full_type}** with clear structure.

Client Brief:
{brief}
""")

    return prompt + "\n\n" + language_instruction[output_lang]

# ==== UI ====

# Pilih bahasa UI
lang_code = st.radio("🌐 Language", ["EN", "ID"], horizontal=True)
T = LANGUAGES[lang_code]

st.title(T["title"])
st.markdown(T["description"])

# Input brief
from input_section import get_client_brief_ui
client_brief = get_client_brief_ui(T["input_label"], T["placeholder"])

# Pilih tipe brief
brief_type = st.selectbox(
    T["dropdown_label"],
    (
        "Creative Brief",
        "Sub-Creative Brief",
        "Media Brief",
        "Sub-Media Brief"
    )
)

# Sub-kategori jika ada
sub_map = {
    "Sub-Creative Brief": ["Production", "Visual", "Copywriting"],
    "Sub-Media Brief": ["Platform", "Budgeting", "KPI"]
}
selected_sub = None
if brief_type in sub_map:
    selected_sub = st.selectbox(T["sub_label"], sub_map[brief_type])

# Pilih output language
output_lang = st.radio(T["output_lang_label"], ["English", "Bahasa Indonesia"], horizontal=True)

# Tombol generate
if st.button(T["button"]):
    if not client_brief.strip():
        st.warning(T["warning"])
    else:
        st.info(T["processing"])
        st.markdown("---")

        full_type = f"{brief_type} - {selected_sub}" if selected_sub else brief_type
        prompt = get_prompt(full_type, client_brief.strip(), output_lang)

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            generated = response.text

            st.markdown(f"{T['brief_type']}: **{full_type}**")
            st.markdown(T["output"])

            # Escape HTML chars & preserve markdown format
            safe_html = markdown.markdown(generated)

           # Display in styled div
            styled_output = f"""
            <div style="font-size:14px; line-height:1.7;">
            {safe_html}
            </div>
            """
            st.markdown(styled_output, unsafe_allow_html=True)

            # Tombol Download
            import io
            download_filename = f"{full_type.replace(' ', '_').lower()}_output.txt"
            buffer = io.StringIO()
            buffer.write(generated)
            buffer.seek(0)

            st.download_button(
                label="📥 Download Generated Brief",
                data=buffer,
                file_name=download_filename,
                mime="text/plain"
                )


        except Exception as e:
            st.error(f"❌ Failed to generate content:\n\n{str(e)}")
