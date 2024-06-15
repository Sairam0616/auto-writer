import time
import streamlit as st

# State variables to control the auto-typer
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'text_to_type' not in st.session_state:
    st.session_state.text_to_type = ""
if 'font_size' not in st.session_state:
    st.session_state.font_size = 12
if 'font_color' not in st.session_state:
    st.session_state.font_color = '#000000'  # Default color black

# Function to generate JavaScript for auto-typing
def generate_js(text, delay):
    escaped_text = text.replace("\n", "\\n").replace("'", "\\'")
    js_code = f"""
    <script>
    let index = 0;
    let text = '{escaped_text}';
    let delay = {delay};

    function typeChar() {{
        if (index < text.length) {{
            document.getElementById('typed_text').innerHTML += text[index] === '\\n' ? '<br>' : text[index];
            index++;
            setTimeout(typeChar, delay);
        }}
    }}

    typeChar();
    </script>
    """
    return js_code

# Streamlit UI
st.title("Auto Typer")

# Text area for input
st.session_state.text_to_type = st.text_area(
    "Enter text to auto-type here:",
    value=st.session_state.text_to_type,
    height=200,
    max_chars=None,
    key="text_area"
)

# Font settings
st.session_state.font_size = st.slider("Font Size", 10, 30, st.session_state.font_size)
st.session_state.font_color = st.color_picker("Font Color", st.session_state.font_color)

# Start/Stop buttons
if st.button("Start Auto Typer"):
    st.session_state.is_running = True

if st.button("Stop Auto Typer"):
    st.session_state.is_running = False

# Display the auto-typed text area with selected font settings
if st.session_state.is_running:
    delay = 100  # Typing delay in milliseconds
    st.markdown(f"<p id='typed_text' style='font-size:{st.session_state.font_size}px; color:{st.session_state.font_color};'></p>", unsafe_allow_html=True)
    js_code = generate_js(st.session_state.text_to_type, delay)
    st.components.v1.html(js_code)

# Instructions
st.write("Press the 'Start Auto Typer' button to start typing the text automatically. Press 'Stop Auto Typer' to stop.")
