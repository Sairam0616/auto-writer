import time
from pynput import keyboard
from pynput.keyboard import Controller, Key, Listener
import streamlit as st

# Initialize the keyboard controller
keyboard_controller = Controller()

# State variables to control the auto-typer
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'text_to_type' not in st.session_state:
    st.session_state.text_to_type = ""
if 'listener' not in st.session_state:
    st.session_state.listener = None

# Function to type text
def type_text(text):
    for char in text:
        if not st.session_state.is_running:
            return
        if char == '\n':
            keyboard_controller.press(Key.enter)
            keyboard_controller.release(Key.enter)
        else:
            keyboard_controller.press(char)
            keyboard_controller.release(char)
        time.sleep(0.01)  # Adjust typing speed here

# Function to start the auto-typer
def start_auto_typer():
    st.session_state.is_running = True
    # Wait for 5 seconds before starting
    time.sleep(3)
    type_text(st.session_state.text_to_type)
    st.write("Auto Typer Started")

# Function to stop the auto-typer
def stop_auto_typer():
    st.session_state.is_running = False
    st.write("Auto Typer Stopped")

# Function to handle keyboard events
def on_press(key):
    try:
        # Check for combination of Cmd+Alt+A
        if key == keyboard.Key.cmd_l and key == keyboard.Key.alt_l and key.char == 'a':
            start_auto_typer()
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        stop_auto_typer()

# Streamlit UI
st.title("Auto Typer")

# Text area for input
st.session_state.text_to_type = st.text_area("Enter text to auto-type here:", value=st.session_state.text_to_type)

# Start/Stop buttons
if st.button("Start Auto Typer"):
    start_auto_typer()

if st.button("Stop Auto Typer"):
    stop_auto_typer()

# Start keyboard listener
if st.session_state.listener is None:
    st.session_state.listener = Listener(on_press=on_press, on_release=on_release)
    st.session_state.listener.start()