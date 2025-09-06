import streamlit as st
import pdfplumber
import random

st.set_page_config(page_title="랜덤 문단 피드", layout="centered")
st.title("📖 PDF 랜덤 문단 쓱쓱 피드")

if 'paragraphs' not in st.session_state:
    st.session_state.paragraphs = []
if 'feed' not in st.session_state:
    st.session_state.feed = []

uploaded_file = st.file_uploader("PDF 파일 업로드", type="pdf")

if uploaded_file:
    if not st.session_state.paragraphs:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
                    st.session_state.paragraphs.extend(chunks)
        st.success(f"{len(st.session_state.paragraphs)} 문단 추출 완료!")

    if st.button("🎲 랜덤 문단 추가"):
        if st.session_state.paragraphs:
            new_para = random.choice(st.session_state.paragraphs)
            st.session_state.feed.append(new_para)

    if st.button("🔁 연속 랜덤 문단 추가"):
        if st.session_state.paragraphs:
            for _ in range(min(5, len(st.session_state.paragraphs))):
                st.session_state.feed.append(random.choice(st.session_state.paragraphs))

    st.markdown("### 📰 랜덤 문단 피드")
    for para in st.session_state.feed:
        st.markdown(f"- {para}\n---")
else:
    st.info("PDF 파일을 업로드하세요.")
