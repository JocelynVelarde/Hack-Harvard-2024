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

for index, col in enumerate(st.columns(2)):
    with col:
        if index == 0:
            if not os.path.exists("event_clip_25.mp4"):
                get_file("event_clip_25.mp4", "videoData")
            st.video("event_clip_25.mp4")
        elif index == 1:
            if not os.path.exists("predictions.json"):
                get_file("predictions.json", "json")
            with open("predictions.json", "r") as f:
                data = json.load(f)
            st.write(data)
            for index, key in enumerate(data.keys()):
                st.write(f"Key {index + 1}")
        st.write(f"Column {index + 1}")     