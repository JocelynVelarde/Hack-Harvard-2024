from twilio.rest import Client
import streamlit as st

class WhatsappSender:

    ACCOUNT_SID = st.secrets["Twilio"]["TWILIO_ACCOUNT_SID"]
    AUTH_TOKEN = st.secrets["Twilio"]["TWILIO_AUTH_TOKEN"]
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

    @classmethod
    def send_message(cls, to_phone_number, message):
        message = cls.CLIENT.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=f'whatsapp:{to_phone_number}'
        )

        return message.sid