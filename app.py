import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(
    page_title="Panasonic Energy Pitch Calculator",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Constants ---
PITCH_LENGTH = 0.801  # in meters

# --- Session State ---
if "speed" not in st.session_state:
    st.session_state.speed = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- Dark Mode Toggle ---
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# --- Theme Colors ---
dark_mode = st.session_state.dark_mode
bg_color = "#1e1e1e" if dark_mode else "#f0f0f0"
text_color = "#ffffff" if dark_mode else "#000000"

st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .dark-toggle button {{
            background-color: {'#3e3e3e' if dark_mode else '#e0e0e0'};
            color: {text_color};
            border: 1px solid #999;
        }}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("Panasonic")
st.header("Energy Pitch Calculator")

# --- Toggle ---
with st.container():
    if st.button("\u263D" if dark_mode else "\u263C", help="Toggle Dark Mode"):
        toggle_theme()
        st.experimental_rerun()

# --- Input Fields ---
st.subheader("Set Speed")
if st.session_state.speed is None:
    speed_input = st.number_input("Speed (m/min):", min_value=0.1, format="%f")
    if st.button("Set Speed"):
        st.session_state.speed = speed_input
        st.experimental_rerun()
else:
    st.success(f"Speed set to {st.session_state.speed} m/min")
    if st.button("Reset Speed"):
        st.session_state.speed = None
        st.experimental_rerun()

# --- Pitch & Time Input ---
st.subheader("Calculation")
pitch = st.text_input("Pitches:")
time = st.text_input("Time (min):")

result = ""

if st.button("Calculate"):
    if st.session_state.speed is None:
        st.error("Please set the speed first.")
    else:
        if pitch and not time:
            try:
                pitch = int(pitch)
                meters = pitch * PITCH_LENGTH
                time_min = meters / st.session_state.speed
                hours = int(time_min // 60)
                minutes = int(time_min % 60)
                result = f"Time Required: {hours} hours and {minutes} minutes"
            except ValueError:
                st.error("Invalid pitch input.")
        elif time and not pitch:
            try:
                time = float(time)
                meters = st.session_state.speed * time
                pitch_result = int(meters / PITCH_LENGTH)
                result = f"Pitches: {pitch_result}"
            except ValueError:
                st.error("Invalid time input.")
        else:
            st.warning("Enter either pitches or time, not both.")

if result:
    st.success(result)

# --- Conversion Table ---
st.subheader("Conversion Chart")
data = {
    "Pitches": list(range(200, 4201, 200)),
    "Meters": [round(p * PITCH_LENGTH, 1) for p in range(200, 4201, 200)]
}
df = pd.DataFrame(data)
double_df = pd.concat([df.iloc[:10].reset_index(drop=True), df.iloc[10:].reset_index(drop=True)], axis=1)
double_df.columns = ["Pitches", "Meters", "Pitches", "Meters"]
st.dataframe(double_df, use_container_width=True)

# --- Reset Button ---
if st.button("Reset Fields"):
    st.session_state.speed = None
    st.experimental_rerun()
