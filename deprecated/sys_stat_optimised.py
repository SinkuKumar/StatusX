import streamlit as st
import psutil
import socket
import time

# Helper to get system stats
def get_system_info():
    hostname = socket.gethostname()
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.5)
    net = psutil.net_io_counters()
    return {
        "hostname": hostname,
        "total_ram": ram.total,
        "used_ram": ram.used,
        "free_ram": ram.available,
        "ram_percent": ram.percent,
        "cpu_percent": cpu,
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv
    }

# Convert bytes to readable units
def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

# Streamlit layout and title
st.set_page_config(page_title="System Monitor", layout="wide")
st.title("🖥️ Real-time System Monitor")

# Update frequency slider in sidebar
update_freq = st.sidebar.slider("⏱️ Update Frequency (seconds)", 1, 10, 2)

# Store previous network values in session state
if "prev_net" not in st.session_state:
    st.session_state.prev_net = psutil.net_io_counters()
    st.session_state.prev_time = time.time()

# Get current system info
info = get_system_info()
net_now = psutil.net_io_counters()
current_time = time.time()

# Calculate network speeds
time_diff = current_time - st.session_state.prev_time
upload_speed = (net_now.bytes_sent - st.session_state.prev_net.bytes_sent) / time_diff
download_speed = (net_now.bytes_recv - st.session_state.prev_net.bytes_recv) / time_diff

# Update previous values
st.session_state.prev_net = net_now
st.session_state.prev_time = current_time

# Display info
st.subheader(f"🖧 Hostname: `{info['hostname']}`")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💾 RAM Used", format_bytes(info['used_ram']), f"{info['ram_percent']}%")
    st.progress(info['ram_percent'] / 100)

with col2:
    st.metric("🧠 CPU Usage", f"{info['cpu_percent']}%", f"{info['cpu_percent']}%")
    st.progress(info['cpu_percent'] / 100)

with col3:
    st.metric("📡 Upload Speed", f"{format_bytes(upload_speed)}/s")
    st.metric("📥 Download Speed", f"{format_bytes(download_speed)}/s")

# Auto-refresh page after interval
time.sleep(update_freq)
st.rerun()
