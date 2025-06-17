import time
import streamlit as st
from utils.data_utils import get_system_info, format_bytes

st.set_page_config(layout="wide", page_title="StatusX", initial_sidebar_state="collapsed")

sys_info = get_system_info()

# Hide Streamlit default UI
hide_streamlit_style = """
    <style>
        body {
            background-color: #F0F2F5;
            font-family: 'Arial', sans-serif;
            color: #333;
            text-color: #FFFFFF;
        }
        #MainMenu, header, footer, .stDeployButton, .st-emotion-cache-zq5wmm {visibility: hidden;}
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
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

cols = st.columns(4)

# Four evenly spread cards
cols = st.columns(4)
for i in range(4):
    with cols[i]:
        st.markdown(f"""
            <div style="padding: 20px; background-color: #C7C6C1; border-radius: 10px; text-align: center;">
                <h4>Card {i+1}</h4>
                <p>Content here</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# 3/4 and 1/4 layout with styled cards
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
        <div style="padding: 20px; background-color: #C7C6C1; border-radius: 10px; text-align: center;">
            <h4>3/4 Width Column</h4>
            <p>Content here</p>
                <p>Content here</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="padding: 20px; background-color: #C7C6C1; border-radius: 10px; text-align: center;">
            <h4>1/4 Width Column</h4>
            <p>Content here</p>
    """, unsafe_allow_html=True)
    
st.markdown("<br>", unsafe_allow_html=True)


# Display system information
server_cols = st.columns(3)

for server_col in server_cols:
    with server_col:
        ram_color = "#FF4B4B" if sys_info['ram_percent'] > 90 else "#1E90FF"
        cpu_color = "#FF4B4B" if sys_info['cpu_percent'] > 90 else "#1E90FF"

        st.markdown(f"""
            <div style="padding: 20px; background-color: #C7C6C1; border-radius: 10px; text-align: center;">
                <p><strong>Hostname:</strong> {sys_info['hostname']}</p>
                <p><strong>Total RAM:</strong> {format_bytes(sys_info['total_ram'])}</p>
                <p><strong>Used RAM:</strong> {format_bytes(sys_info['used_ram'])} ({sys_info['ram_percent']}%)</p>
                <div style="height: 10px; background-color: #eee; border-radius: 10px; overflow: hidden; margin-bottom: 10px;">
                    <div style="height: 100%; width: {sys_info['ram_percent']}%; background-color: {ram_color};"></div>
                </div>
                <p><strong>CPU Usage:</strong> {sys_info['cpu_percent']}%</p>
                <div style="height: 10px; background-color: #eee; border-radius: 10px; overflow: hidden;">
                    <div style="height: 100%; width: {sys_info['cpu_percent']}%; background-color: {cpu_color};"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
time.sleep(5)
st.rerun()