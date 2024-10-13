import streamlit as st
#from models.video_analyzer import analyze_video, chat_prompt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.mongo_connection import *

st.set_page_config(
    page_title="Reports",
    page_icon="🚨",
)

for index, col in enumerate(st.columns(3)):
    with col:
        if index == 0:
            if not os.path.exists("event_clip_1.mp4"):
                get_file("event_clip_1.mp4", "videoData")
            st.video("event_clip_25.mp4")
        st.write(f"Column {index + 1}")     