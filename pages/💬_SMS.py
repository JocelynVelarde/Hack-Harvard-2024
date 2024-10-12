import streamlit as st
import pandas as pd
import numpy as np
import api.mongo_connection as MongoConnection
from algorithms.whatsapp import WhatsappSender

st.set_page_config(
        page_title="SMS",
        page_icon="💬",
)

st.image('assets/mini.png', use_column_width=True)
st.title('💬 SMS Notifications')

st.write("\n\n")
st.write("\n\n")

st.subheader('Step 1: Join the WhatsApp chat')
st.write("You can manually do the setup by sending the message 'join fair-broad' to +14155238886 in WhatsApp")
st.write("Or you can click the button below to open the chat with the default message")
message = "join fair-broad\n"
wa_url = f"https://wa.me/{+14155238886}?text={message.replace(' ', '%20')}"
st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: center;">
        <a href="{wa_url}">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="width:{100}px; height:auto;">
        </a>
    </div>
    """, 
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div style="text-align: center;">
        <a href="{wa_url}" style="font-size: 20px;">Click here</a>
    </div>
    """, 
    unsafe_allow_html=True
)

st.write("\n\n")
st.write("\n\n")


st.subheader('Step 2: Test message reception')
st.write("Make sure to save your phone number below to receive notifications")
st.session_state.phone_number = st.text_input("Add or update phone number:")
if st.button("Save Phone Number and Test"):
    st.session_state.phone_number = str(st.session_state.phone_number)
    try: 
        MongoConnection.insert_data({"phone_number": st.session_state.phone_number}, "numberData", "number")
        st.success("Phone number saved!")
        text_message = "Hello from Theft Alert! You will now receive notifications from us."
        WhatsappSender.send_message(str(st.session_state.phone_number), text_message)
        st.success("Message sent successfully!")
    except Exception as e:
        st.error(f"Error saving phone number: {e}")

st.write("\n\n")
st.write("\n\n")



    