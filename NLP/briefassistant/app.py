import streamlit as st
import google.generativeai as genai
import markdown
from input_section import get_client_brief_ui
from download_utils import generate_pdf_download_button
import datetime

# ==== Konfigurasi ====
st.set_page_config(page_title="Brief Breakdown Assistant", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

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
        "Creative Brief": f"""You are a creative strategist. Create a **Creative Brief** that includes:
- Background
- Objectives
- Target Audience:
  - Demographic (age, gender, location, income group)
  - Psychographic (values, lifestyle, digital habits, interests)
- Key Message
- Tone & Manner (If already stated in the client brief, interpret and refine it into actionable creative direction. If not, suggest based on target.)
- Deliverables
- Timeline

Client Brief:
{brief}
""",
        "Sub-Creative Brief - Production": f"""You are a production lead. Create a **Production Brief** with:
- Format & Duration
- Shooting Needs
- Talent & Location
- Technical Notes
- Timeline

Client Brief:
{brief}
""",
        "Sub-Creative Brief - Visual": f"""You are a visual designer. Create a **Visual Direction Brief** with:
- Visual Style
- Colors & Fonts
- Moodboard Direction
- Asset Guidelines

Client Brief:
{brief}
""",
        "Sub-Creative Brief - Copywriting": f"""You are a copywriter. Create a **Copywriting Brief** that includes:
- Key Messages
- Tone of Voice
- Must-use Phrases
- Platform-specific Adjustments

Client Brief:
{brief}
""",
        "Media Brief": f"""You are a media strategist. Create a **Media Brief** using bullet points and actionable insights:

- **Recommended Channels**: Choose suitable platforms (Meta Ads, TikTok, YouTube, Programmatic). Do NOT mention GDN.
- **Budget Plan**:
  - Total budget suggestion (range or estimated total)
  - Breakdown by channel:
    - Meta Ads (Facebook, Instagram): %
    - TikTok Ads: %
    - YouTube Ads: %
    - Others (if relevant): %
  - Rationale for allocation per channel
  - Estimated CPM/CPC per channel
  - Suggested flighting plan (weekly/monthly)
- **Targeting Strategy**:
  - Audience Demographic (age, gender, geo, income)
  - Audience Psychographic (interests, behavior, lifestyle)
  - Target Segments (e.g. students, young moms, sneakerheads)
  - Custom/Lookalike strategy
- **KPI & Measurement**:
  - Primary KPIs (e.g. Reach, Impressions, ROAS, Leads)
  - Supporting KPIs (e.g. CTR, View Rate, Engagement Rate)
  - Benchmarks or estimated performance targets per platform
  - Attribution model (last-click, data-driven, etc.)
  - Success criteria and how performance will be tracked

Client Brief:
{brief}
""",
        "Sub-Media Brief - Platform": f"""You are a digital planner. Create a **Platform Brief** with:
- Platform Choices (Meta, TikTok, YouTube, etc.)
- Rationale per platform
- Format Suggestions (video, carousel, etc.)
- Organic vs Paid Roles

Client Brief:
{brief}
""",
        "Sub-Media Brief - Budgeting": f"""You are a media buyer. Create a **Budget Allocation Plan** including:
- Total budget (if known, otherwise suggest a range)
- Per-channel allocation
- CPM/CPC assumptions
- Estimated impressions/reach per platform
- Flighting plan (weekly/monthly)
- Optimization plan based on performance

Client Brief:
{brief}
""",
        "Sub-Media Brief - KPI": f"""You are a digital strategist. Create a **KPI Brief** that includes:
- Main KPIs (e.g. ROAS, CPA, Leads)
- Supporting metrics (CTR, View Rate)
- Benchmarks (industry or estimated)
- Attribution model (last-click, data-driven, etc.)
- Success Criteria and Reporting Frequency

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

if st.button(T["button"]):
    if not client_brief.strip():
        st.warning(T["warning"])
    else:
        processing_box = st.empty()
        processing_box.info(T["processing"])

        full_type = f"{brief_type} - {selected_sub}" if selected_sub else brief_type
        prompt = get_prompt(full_type, client_brief.strip(), output_lang)

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            generated = response.text

            processing_box.empty()

            st.markdown(f"{T['brief_type']}: **{full_type}**")
            st.markdown(T["output"])

            html_output = markdown.markdown(generated)
            st.markdown(f"<div style='font-size:14px; line-height:1.7;'>{html_output}</div>", unsafe_allow_html=True)

            generate_pdf_download_button(html_output, filename=f"{full_type.replace(' ', '_').lower()}.pdf")

        except Exception as e:
            processing_box.empty()
            st.error(f"❌ Failed to generate content:\n\n{str(e)}")

# ==== Footer ====
current_year = datetime.datetime.now().year
st.markdown(
    f"<hr style='margin-top:30px;'><p style='text-align:center; color:gray;'>Copyright © TimothyEL {current_year}</p>",
    unsafe_allow_html=True
)
