import streamlit as st
from answer import answer, page_label, DOC_NAMES

st.title("MineGuard")
st.caption("Ask questions about Indian mining safety law.")

question = st.text_input("Your question")

if question:
    with st.spinner("Searching the regulations..."):
        reply, passages = answer(question)
    st.markdown(reply)
    st.subheader("Sources")
    for i, p in enumerate(passages, start=1):
                st.write(f"[{i}] {DOC_NAMES.get(p['source'], p['source'])}, {page_label(p)}")