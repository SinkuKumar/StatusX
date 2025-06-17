import streamlit as st
import psutil
import socket
import time

def get_system_info():
    hostname = socket.gethostname()
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=None)
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

def format_bytes(size):
    # Convert bytes to human-readable
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

# Set Streamlit layout
st.set_page_config(page_title="System Monitor", layout="wide")
st.title("🖥️ Real-time System Monitor")

# Add frequency slider
update_freq = st.sidebar.slider("⏱️ Update Frequency (seconds)", min_value=1, max_value=10, value=1, step=1)

# Initialize previous network stats
if "prev_net" not in st.session_state:
    st.session_state.prev_net = psutil.net_io_counters()

# Display info
placeholder = st.empty()

while True:
    info = get_system_info()
    net_now = psutil.net_io_counters()
    upload_speed = net_now.bytes_sent - st.session_state.prev_net.bytes_sent
    download_speed = net_now.bytes_recv - st.session_state.prev_net.bytes_recv
    st.session_state.prev_net = net_now

    with placeholder.container():
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

    time.sleep(update_freq)
