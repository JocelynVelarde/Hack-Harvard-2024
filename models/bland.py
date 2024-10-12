from openai import OpenAI
import streamlit as st

client = OpenAI(st.secrets["OPENAI_API_KEY"])

assistant = client.beta.assistants.create(
    name="Call assistant",
    instructions="You are a call assistant for a security system. A customer calls to report an event inside a store. You can ask questions to understand the event and will try to see if a similar event was detected by the cctv system",
    model="gpt-4o-mini"
)

thread = client.beta.threads.create()
