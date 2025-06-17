import streamlit as st
import time

# Set page config for full screen experience
st.set_page_config(layout="wide")

# Slide contents: List of dictionaries
slides = [
    {"title": "Welcome to the Slideshow", "content": "This is the first slide of your presentation."},
    {"title": "Overview", "content": "Here's an overview of what we'll cover today."},
    {"title": "Details", "content": "This slide goes into more detail on the topic."},
    {"title": "Thank You", "content": "Thanks for watching this auto-playing slideshow!"}
]

# Slideshow duration per slide in seconds
slide_duration = 3

# Placeholder for slide content
slide_placeholder = st.empty()

# Slideshow loop
for slide in slides:
    with slide_placeholder.container():
        st.markdown(f"## {slide['title']}")
        st.markdown(f"{slide['content']}")
    time.sleep(slide_duration)
