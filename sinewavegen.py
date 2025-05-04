import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time
import csv
import os
from matplotlib.figure import Figure
from matplotlib import rc

# Configure matplotlib for better rendering
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 100
plt.rcParams['path.simplify'] = True
plt.rcParams['path.simplify_threshold'] = 0.8
plt.rcParams['agg.path.chunksize'] = 20000
# Better text rendering
rc('font', family='DejaVu Sans')

st.set_page_config(layout="wide")
st.title("Real-Time Sine Wave Generator")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    amplitude = st.number_input("Enter amplitude:", value=1.0, step=0.1)
with col2:
    F = st.number_input("Enter frequency (Hz):", value=1.0, step=0.1)

# Constants
sampling_rate = 1000 
window_time = 5  # Time window for the plot (seconds)
update_interval = 0.03  
animation_speed_factor = 0.15  # Slows down the animation (smaller = slower)
data_retention = 2500  # Number of data points to keep in memory

# For smoother rendering
plt.rcParams['figure.dpi'] = mouth_point = 100
plt.rcParams['savefig.dpi'] = 100
plt.rcParams['path.simplify'] = True
plt.rcParams['path.simplify_threshold'] = 0.8
plt.rcParams['agg.path.chunksize'] = 20000

# CSV filename
filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datapoints.csv")

# Init session state
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "history_df" not in st.session_state:
    st.session_state.history_df = pd.DataFrame(columns=["Time (s)", "Data points"])
if "logged_times" not in st.session_state:
    st.session_state.logged_times = set()

# CSV filename
filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datapoints.csv")

# Create CSV with header if it doesn't exist
if not os.path.exists(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time (s)", "Data points"])

# Reset button
if st.button("Reset Timer and Data"):
    st.session_state.start_time = time.time()
    st.session_state.history_df = pd.DataFrame(columns=["Time (s)", "Data points"])
    st.session_state.logged_times = set()
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Data points"])

# Placeholders
plot_placeholder = st.empty()
table_placeholder = st.empty()
history_toggle = st.checkbox("Show full data history and duration", value=False)

# Real-time clock for continuous updates
time_counter = 0  # Global time counter for continuous updates

# MAIN LOOP: Infinite loop to simulate real-time data
while True:
    # Get the actual time elapsed since last frame to ensure smooth animation
    current_time = time.time()
    if "last_update_time" not in st.session_state:
        st.session_state.last_update_time = current_time
        frame_time = update_interval
    else:
        # Apply animation speed factor to slow down the wave motion
        frame_time = (current_time - st.session_state.last_update_time) * animation_speed_factor
        st.session_state.last_update_time = current_time
    
    # Update the time counter with scaled time for slower animation
    time_counter += frame_time
    
    # Generate continuous time values for the current window only with more points for smoother curve
    time_values = np.linspace(time_counter - window_time, time_counter, int(sampling_rate * window_time), endpoint=False)

    # Generate sine wave data with interpolation for extra smoothness
    if amplitude == 0 or F == 0:
        data_points = np.zeros_like(time_values)
    else:
        # Generate higher resolution sine wave for smoother appearance
        data_points = amplitude * np.sin(2 * np.pi * F * time_values)

    # Create dataframe for the current window only
    current_window_df = pd.DataFrame({"Time (s)": time_values, "Data points": data_points})
    
    # Update history DataFrame - append only new points for logging purposes
    new_df = pd.DataFrame({"Time (s)": [time_values[-1]], "Data points": [data_points[-1]]})
    st.session_state.history_df = pd.concat([st.session_state.history_df, new_df], ignore_index=True)
    
    # Limit retention to prevent too much data accumulation
    if len(st.session_state.history_df) > data_retention:
        st.session_state.history_df = st.session_state.history_df.tail(data_retention)
    
    # Save window to CSV
    if "logged_times" not in st.session_state:
        st.session_state.logged_times = set()

    # Create CSV with header if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time (s)", "Data points"])

    # Overwrite the CSV with only the current window
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Data points"])
        for t, d in zip(time_values, data_points):
            writer.writerow([t, d])

    # Plotting - show dynamically updating sine wave
    with plot_placeholder.container():
        # Create a new figure
        fig, ax = plt.subplots(figsize=(12, 5), facecolor='black')
        ax.set_facecolor('black')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        # Configure the plot for maximum smoothness
        plt.rcParams['path.simplify'] = True
        plt.rcParams['path.simplify_threshold'] = 1.0
        plt.rcParams['agg.path.chunksize'] = 10000
        
        # Plot the entire current window of data with enhanced smoothness settings
        ax.plot(current_window_df["Time (s)"], current_window_df["Data points"], 
                color='red', linewidth=2.0, antialiased=True, linestyle='-',
                alpha=0.9, solid_capstyle='round')

        ax.set_ylim(-max(1.1, abs(amplitude) * 1.1), max(1.1, abs(amplitude) * 1.1))
        ax.set_xlim(time_counter - window_time, time_counter)
        ax.set_title(f"Sine Wave (Amp={amplitude}, Freq={F}Hz, Elapsed={round(time_counter, 2)}s)", color='white')
        ax.set_xlabel("Time (s)", color='white')
        ax.set_ylabel("Value", color='white')
        ax.grid(True, color='gray', linestyle='--', alpha=0.5)
        plt.tight_layout()

        # Display the plot
        st.pyplot(fig, use_container_width=True)

    # Data table
    with table_placeholder.container():
        if history_toggle:
            st.subheader(f"Full Data History (Elapsed Time: {round(time_counter, 2)}s)")
            st.dataframe(st.session_state.history_df.tail(1000), hide_index=True)
        else:
            st.subheader("Latest Data Point")
            if len(time_values) > 0:
                latest = pd.DataFrame({
                    "Time (s)": [round(time_values[-1], 4)],
                    "Data points": [round(data_points[-1], 4)]
                })
                st.dataframe(latest, hide_index=True)

    # PERFORMANCE OPTIMIZATION: Only update the plot every other frame to reduce jitter
    if "frame_counter" not in st.session_state:
        st.session_state.frame_counter = 0
    
    st.session_state.frame_counter += 1
    
    # Calculate time to sleep for consistent, smoother frame rate
    # Sleep longer to allow system to catch up
    processing_time = time.time() - st.session_state.last_update_time
    sleep_time = max(0.025, update_interval - processing_time)
    time.sleep(sleep_time)