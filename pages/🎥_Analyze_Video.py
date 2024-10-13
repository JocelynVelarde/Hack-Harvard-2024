import streamlit as st
from models.video_analyzer import analyze_video, chat_prompt
import os

api_key = st.secrets["OPENAI"]['OPENAI_API_KEY']

st.set_page_config(
    page_title="Analyze Video",
    page_icon="🎥",
)
st.image("assets/mini3.jpg", use_column_width=True)

st.title('Analyze Video to get Shoplifting Insights')

st.write("Upload a video of a shoplifting incident to get insights on the incident.")
st.write("You can then send messages to start a conversation about the incident.")

st.divider()

uploaded_files = st.file_uploader("Upload video", accept_multiple_files=True, type=["mp4"])

if uploaded_files:
    uploaded_file = uploaded_files[0]
    st.success("Video uploaded successfully!")
    
    with open(f"temp_{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
        image_path = f"temp_{uploaded_file.name}"
    video_name = os.path.splitext(image_path)[0]
    st.video(image_path)
    analysis_results = analyze_video(video_name, "mp4")
    st.write(analysis_results)
    
    
st.divider()
st.subheader('Ask questions about specific things on your scene')
chat_input = st.text_area("Type your question here")
if st.button("Send"):
        chat_response = chat_prompt(analysis_results, chat_input, api_key)
        st.subheader("Answer:")
        st.write(chat_response)