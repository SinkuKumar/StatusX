import streamlit as st

# Set page config for wide layout
st.set_page_config(layout="wide")

# Sidebar content
with st.sidebar:
    st.title("Settings")
    st.write("Adjust your preferences here.")

# Hide Streamlit default UI
hide_streamlit_style = """
    <style>
        #MainMenu, header, footer, .stDeployButton, .st-emotion-cache-zq5wmm {visibility: hidden;}
        .block-container {
            padding: 0rem;
            margin: 0;
        }
        .stMain {
        padding-left: 1rem;
        padding-right: 1rem;
        }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Top Row: 3 columns (1:1:1 ratio)
col1, col2, col3 = st.columns(3)
with col1:
    st.container().markdown("### Top Left\nContent here")
    st.write("")  # Adjust spacing if needed

with col2:
    st.container().markdown("### Top Middle\nContent here")

with col3:
    st.container().markdown("### Top Right\nContent here")

# Middle Row: 2 columns (2/3 and 1/3 width ratio)
col_left, col_right = st.columns([2, 1])
with col_left:
    st.container().markdown("### Middle Left (large block)\nContent here")

with col_right:
    # Stack two containers vertically in right column
    top_right = st.container()
    bottom_right = st.container()

    with top_right:
        st.markdown("### Middle Right Top\nContent here")
    with bottom_right:
        st.markdown("### Middle Right Bottom\nContent here")
