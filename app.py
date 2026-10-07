import streamlit as st
from main import process, LANGUAGES

st.title("حــــــــــيّاك")

if "n" not in st.session_state:
    st.session_state.n = 0      # changing this number gives a fresh, empty recorder

language = st.selectbox("Translate to", list(LANGUAGES))
audio = st.audio_input("Record your voice", key=f"audio_{st.session_state.n}")

if st.button("Reset"):
    st.session_state.n += 1
    st.rerun()

if audio and st.button("Translate"):
    with open("input.wav", "wb") as f:
        f.write(audio.getvalue())

    with st.spinner("Processing..."):
        text, msa, translation, audio_file = process("input.wav", language)

    st.write("**You said:**", text)
    st.write("**Translation:**", translation)
    if audio_file:
        st.audio(audio_file, autoplay=True)
