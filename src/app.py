import os
from pathlib import Path
import streamlit as st

try:
    os.environ.setdefault("GROQ_API_KEY", st.secrets["GROQ_API_KEY"])
except Exception:
    pass

if not Path("db").exists():
    with st.spinner("First start: building the search index (about a minute)..."):
        from build_index import build_index
        build_index()

from agent import run_agent, cited_sources
st.title("MineGuard")
st.caption("Ask questions about Indian mining safety law.")

question = st.text_input("Your question")

if question:
    with st.spinner("Searching the regulations..."):
        answer_text, sources = run_agent(question)
    st.markdown(answer_text)
    st.subheader("Sources")
    for line in cited_sources(answer_text, sources):
        st.write(line)