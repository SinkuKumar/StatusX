import time
import streamlit as st
import plotly.graph_objects as go
from utils.data_utils import get_system_info, format_bytes

# Streamlit config
st.set_page_config(layout="wide", page_title="StatusX", initial_sidebar_state="collapsed")

# Inject custom CSS to hide Streamlit UI and style the app
st.markdown("""
    <style>
        #MainMenu, header, footer, .stDeployButton, .st-emotion-cache-zq5wmm {
            visibility: hidden;
        }
        .block-container {
            padding: 0rem;
            margin: 0;
        }
        .stMain {
            margin-top: 0;
            background-color: white;
            border: 5px solid #007BFF;
            height: 100vh;
            box-sizing: border-box;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        body {
            background-color: #F0F2F5;
            font-family: 'Arial', sans-serif;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar: refresh rate control
st.sidebar.header("Refresh Rates")
cpu_interval = st.sidebar.slider("CPU Info Refresh Interval (seconds)", 1, 10, 1)
chart_interval = st.sidebar.slider("Chart Info Refresh Interval (seconds)", 5, 30, 10)

# Static layout cards
cols = st.columns(4)
for i in range(4):
    with cols[i]:
        st.markdown(f"""
            <div style="padding: 20px; background-color: #C7C6C1; border-radius: 10px; text-align: center;">
                <h4>Card {i+1}</h4>
                <p>Static Content</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Chart section placeholders
chart_placeholder = st.empty()

# CPU Info placeholder
cpu_placeholder = st.empty()

# Start/stop live updates
if st.sidebar.button("Start Monitoring"):
    st.session_state.monitoring = True
if st.sidebar.button("Stop Monitoring"):
    st.session_state.monitoring = False

# Defaults
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = True

def draw_cpu_info():
    sys_info = get_system_info()
    ram_color = "#FF4B4B" if sys_info['ram_percent'] > 90 else "#1E90FF"
    cpu_color = "#FF4B4B" if sys_info['cpu_percent'] > 90 else "#1E90FF"

    with cpu_placeholder.container():
        server_cols = st.columns(3)
        for server_col in server_cols:
            with server_col:
                st.markdown(f"""
                    <div style="padding: 20px; background-color: #C7C6C1; border-radius: 10px; text-align: center;">
                        <p><strong>Hostname:</strong> {sys_info['hostname']}</p>
                        <p><strong>Total RAM:</strong> {format_bytes(sys_info['total_ram'])}</p>
                        <p><strong>Used RAM:</strong> {format_bytes(sys_info['used_ram'])} ({sys_info['ram_percent']}%)</p>
                        <div style="height: 10px; background-color: #eee; border-radius: 10px; overflow: hidden; margin-bottom: 10px;">
                            <div style="height: 100%; width: {sys_info['ram_percent']}%; background-color: {ram_color};"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Plotly gauge for CPU
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=sys_info['cpu_percent'],
                    title={'text': "CPU Usage"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': cpu_color},
                        'steps': [
                            {'range': [0, 50], 'color': "#d4edda"},
                            {'range': [50, 75], 'color': "#ffeeba"},
                            {'range': [75, 100], 'color': "#f8d7da"},
                        ],
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)

def draw_chart_info():
    with chart_placeholder.container():
        st.markdown(f"""
            <div style="padding: 20px; background-color: #D3D3D3; border-radius: 10px; text-align: center;">
                <h4>Chart Info</h4>
                <p>Last updated: {time.strftime('%H:%M:%S')}</p>
            </div>
        """, unsafe_allow_html=True)

# Live updating with manual control (loop inside container avoids flickering)
if st.session_state.monitoring:
    last_cpu_update = 0
    last_chart_update = 0

    while True:
        now = time.time()

        if now - last_cpu_update > cpu_interval:
            draw_cpu_info()
            last_cpu_update = now

        if now - last_chart_update > chart_interval:
            draw_chart_info()
            last_chart_update = now

        time.sleep(0.5)
