import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.mongo_connection import *
from models.face_detection import video_timestamp_detection, destroy_windwows

st.set_page_config(
    page_title="Reports",
    page_icon="🚨",
)

selection = st.selectbox("Select a report", ["vid1_cam1_labeled.mp4", "vid4_cam3_labeled.mp4"])

baseName = os.path.splitext(selection)[0].replace("_labeled", "")

st.write(f"Report for {baseName}")

for index, col in enumerate(st.columns(2)):
    with col:
        if index == 0:
            st.write(f"Surveillance video")     
            if not os.path.exists(f'{baseName}_labeled.mp4'):
                get_file(f'{baseName}_labeled.mp4', "videoData")
            st.video(f"{baseName}_labeled.mp4")
        elif index == 1:    
            st.write(f"Detected face")     
            res = get_one_data({"filename" : f"{baseName}_predictions.json"}, "predictionData", "prediction")

            data = json.loads(res)

            non_empty_count = 0
            for frame_data in data["data"]:
                if non_empty_count >= 5:
                    video_timestamp_detection(f"{baseName}_labeled.mp4", 
                                              frame_data["frame"], 
                                              show_frame=False, 
                                              target_x=frame_data["predictions"][0]["x"], 
                                              target_y=frame_data["predictions"][0]["y"], 
                                              target_width=frame_data["predictions"][0]["width"], 
                                              target_height=frame_data["predictions"][0]["height"], 
                                              save_image=True)
                    break

                if frame_data["predictions"]:
                    if frame_data["predictions"][0]["level"] == "dangerous" and frame_data["predictions"][0]["confidence"] > 0.5:
                        non_empty_count += 1
                else:
                    non_empty_count = 0 
            
            try :
                st.image(f'{baseName}_labeled_face_detection.jpg', use_column_width=True)
            except:
                st.write("No dangerous face detected")

st.subheader("Insights")

from models.video_analyzer import analyze_video, openai_analsis_extended_crop

text = openai_analsis_extended_crop(f'{baseName}_labeled', 'mp4')

text = analyze_video(f'{baseName}_labeled', 'mp4', facial_context=text)

st.write(text)