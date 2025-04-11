
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Integer Converter", layout="centered", initial_sidebar_state="auto")

# Dark mode styling
dark_mode = True
if dark_mode:
    st.markdown(
        '''
        <style>
        body {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .stTextInput > div > div > input,
        .stNumberInput > div > input {
            background-color: #2e2e2e;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #3e3e3e;
            color: #ffffff;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )

st.title("Integer Converter")

st.subheader("Set Speed")
speed = st.number_input("Speed (m/min)", min_value=0.0, step=0.1, format="%.2f")

pitch_length = 0.801
pitch_input = st.text_input("Pitches")
time_input = st.text_input("Time (min)")
result = ""

if st.button("Calculate"):
    if not speed:
        st.error("Set speed first.")
    else:
        if pitch_input and not time_input:
            try:
                pitches = int(pitch_input)
                meters = pitches * pitch_length
                time_min = meters / speed
                hours = int(time_min // 60)
                minutes = int(time_min % 60)
                result = f"Time Required: {hours} hours and {minutes} minutes"
            except ValueError:
                result = "Invalid pitch input."
        elif time_input and not pitch_input:
            try:
                time = float(time_input)
                meters = speed * time
                pitches = meters / pitch_length
                result = f"Pitches: {int(pitches)}"
            except ValueError:
                result = "Invalid time input."
        else:
            result = "Enter either pitches or time, not both."

if result:
    st.success(result)

if st.button("Reset"):
    st.experimental_rerun()

# Conversion chart
st.subheader("Conversion Chart (Pitches to Meters)")
data = {
    "Pitches": list(range(200, 4201, 200)),
    "Meters": [round(p * pitch_length, 1) for p in range(200, 4201, 200)]
}
df = pd.DataFrame(data)

# Display two columns side-by-side
half = len(df) // 2
double_df = pd.concat([df.iloc[:half].reset_index(drop=True), df.iloc[half:].reset_index(drop=True)], axis=1)
double_df.columns = ["Pitches", "Meters", "Pitches", "Meters"]
st.dataframe(double_df, use_container_width=True)
