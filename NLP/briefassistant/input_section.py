import streamlit as st

def input_form(T):
    client_brief = st.text_area(T["input_label"], height=250, placeholder=T["placeholder"])

    brief_type = st.selectbox(
        T["dropdown_label"],
        (
            "Creative Brief",
            "Sub-Creative Brief",
            "Media Brief",
            "Sub-Media Brief"
        )
    )

    sub_map = {
        "Sub-Creative Brief": ["Production", "Visual", "Copywriting"],
        "Sub-Media Brief": ["Platform", "Budgeting", "KPI"]
    }
    selected_sub = None
    if brief_type in sub_map:
        selected_sub = st.selectbox(T["sub_label"], sub_map[brief_type])

    output_lang = st.radio(T["output_lang_label"], ["English", "Bahasa Indonesia"], horizontal=True)

    return client_brief, brief_type, selected_sub, output_lang
