import json
import re

import pandas as pd
import streamlit as st
from google import genai

MODEL = "gemini-3.5-flash-lite"

st.set_page_config(
    page_title="Vocabulary Explorer",
    layout="wide",
    initial_sidebar_state="expanded",
)

vocabulary_schema = {}

def get_gemini_api_key():
    try:
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


def parse_text(raw_text: str) -> str:
    """Yomitan's internal parser is a simple algorithm which can parse sentences using 
    the installed dictionaries. It works by repeatedly detecting the longest term at 
    the start of the sentence and advancing until no text remains. 
    This provides decent results for the general case, but since grammatical structure 
    is not taken into account, it can sometimes yield incorrect segmentation."""
    lines = []
    for line in raw_text.replace("\ufeff", "").splitlines():
        line = line.strip()
        if not line or line.upper() == "WEBVTT" or line.isdigit():
            continue

        if line:
            lines.append(line)
    return "\n".join(lines)


def make_prompt() -> str:
    return ""


def analyze() -> pd.DataFrame:
    api_key = get_gemini_api_key()
    if not api_key:
        raise ValueError(
            "ยังไม่พบ GEMINI_API_KEY กรุณาใส่ไว้ใน Project/.env เพื่อทดสอบในเครื่อง "
            "หรือเพิ่มใน Streamlit secrets เมื่อนำแอปขึ้นเว็บ"
        )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL,
        contents=make_prompt(),
        config={
            "response_mime_type": "application/json",
            "response_schema": vocabulary_schema,
        },
    )
    return response.text


run = st.button("Run", type="primary", disabled=False, use_container_width=True)
if run:
    with st.spinner():
        try:
            st.session_state["vocab_df"] = analyze()
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Gemini could not complete the analysis. Check your API key or try again. Details: {exc}")

else:
    st.info("Add some text above to get started.")
