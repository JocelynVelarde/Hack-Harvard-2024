import streamlit as st
from algorithms.gpt_vision import get_analysis_messages, chat_prompt
import pymongo
import gridfs

api_key = st.secrets["OPEN_AI_KEY"]

st.set_page_config(
    page_title="Analyze Video",
    page_icon="🚨",
)
st.image("assets/images/emergency.png", use_column_width=True)

st.title('Analyze Video to get Shoplifting Insights')

st.write("Upload a video of a shoplifting incident to get insights on the incident.")
st.write("You can then send messages to start a conversation about the incident.")

st.divider()

uploaded_files = st.file_uploader("Upload video", accept_multiple_files=True, type=["mp4", "mp3"])

if uploaded_files:
    image_paths = []
    for uploaded_file in uploaded_files:
        with open(f"temp_{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
            image_paths.append(f"temp_{uploaded_file.name}")

    analysis_results = get_analysis_messages(image_paths, api_key)
    
    for i, (prompt, message) in enumerate(analysis_results.items(), 1):
        st.subheader(f"Prompt {i}: {prompt}")
        st.write(message)

st.divider()
st.subheader(':orange[Ask questions about the accident]')
chat_input = st.text_area("Type your question here")
if st.button("Send"):
        chat_response = chat_prompt(analysis_results, chat_input, api_key)
        st.subheader("Answer:")
        st.write(chat_response)