import streamlit as st
import time

# Set wide layout
st.set_page_config(layout="wide")

# Define slides
slides = [
    {"title": "Welcome", "content": "This is the first slide."},
    {"title": "Overview", "content": "Here's what we will cover."},
    {"title": "Details", "content": "More detailed content goes here."},
    {"title": "Thanks", "content": "Thank you for watching!"}
]

# Slide duration (seconds)
duration = 3

# Placeholder for animated HTML
slide_placeholder = st.empty()

# CSS for fade-in animation
fade_css = """
<style>
.fade-in {
    animation: fadeIn 1s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
.slide-box {
    padding: 50px;
    background-color: #f9f9f9;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    text-align: center;
}
h1 {
    font-size: 3em;
}
p {
    font-size: 1.5em;
}
</style>
"""

st.markdown(fade_css, unsafe_allow_html=True)

# Loop through slides
for slide in slides:
    html_content = f"""
    <div class="slide-box fade-in">
        <h1>{slide['title']}</h1>
        <p>{slide['content']}</p>
    </div>
    """
    slide_placeholder.markdown(html_content, unsafe_allow_html=True)
    time.sleep(duration)
