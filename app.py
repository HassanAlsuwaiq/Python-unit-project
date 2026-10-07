import streamlit as st
from main import process, LANGUAGES


# Page setup

st.set_page_config(
    page_title="حيّاك",
    layout="centered"
)

# Styling

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #111714;
}

/* Section headings */
h2, h3 {
    color: #F4F1E8 !important;
}

/* Normal text */
p, label {
    color: #D6D6D6 !important;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    height: 48px;
    font-weight: 600;
}

/* Primary Translate button */
.stButton > button[kind="primary"] {
    background-color: #2F6B4F !important;
    color: #F4F1E8 !important;
    border: none !important;
}

/* Translate button when hovering */
.stButton > button[kind="primary"]:hover {
    background-color: #3D8061 !important;
    color: #FFFFFF !important;
}

/* Translation result cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px;
    background-color: #18201C;
    border: 1px solid #2C3932;
    padding: 5px;
}

/* Divider */
hr {
    border-color: #2C3932 !important;
}

/* Main page width and spacing */
.block-container {
    max-width: 750px;
    padding-top: 3rem;
    padding-bottom: 5rem;
}

</style>
""", unsafe_allow_html=True)


# Logo

left, center, right = st.columns([0.8, 2.4, 0.8])

with center:
    st.image("logo.png", use_container_width=True)


# Subtitle
st.markdown(
    "<p style='text-align:center; color:#A7ADA9; margin-top:-10px;'>"
    "Saudi dialect, understood anywhere."
    "</p>",
    unsafe_allow_html=True
)

# Session state

if "n" not in st.session_state:
    st.session_state.n = 0

# Language

language = st.selectbox(
    "Translate to",
    list(LANGUAGES)
)

# Voice recording

st.subheader("Record")

audio = st.audio_input(
    "Record your voice",
    key=f"audio_{st.session_state.n}"
)

# Buttons

col1, col2 = st.columns(2)

with col1:
    reset = st.button(
        "Reset",
        use_container_width=True
    )

with col2:
    translate = st.button(
        "Translate",
        type="primary",
        use_container_width=True
    )

# Reset recorder

if reset:
    st.session_state.n += 1
    st.rerun()


# Translation

if translate:

    if not audio:
        st.warning("Please record your voice first.")

    else:
        with open("input.wav", "wb") as f:
            f.write(audio.getvalue())

        with st.spinner("Translating your speech..."):
            text, msa, translation, audio_file = process(
                "input.wav",
                language
            )

        # -------------------------
        # Results
        # -------------------------

        st.divider()
        st.subheader("Translation Result")

        with st.container(border=True):
            st.caption("You said")
            st.write(text)

        with st.container(border=True):
            st.caption("Modern Standard Arabic")
            st.write(msa)

        with st.container(border=True):
            st.caption(f"{language} Translation")
            st.write(translation)

        if audio_file:
            st.subheader("Listen")
            st.audio(audio_file, autoplay=True)