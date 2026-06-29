import os

from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    GEMINI_API_KEY=st.secrets.get('Gemini_API_Key', os.getenv('Gemini_API_Key'))
    TRAIN_API_KEY=st.secrets.get('RapidAPI_Key', os.getenv('RapidAPI_Key'))
    FLIGHT_API_KEY=st.secrets.get('Flight_RapidAPI_Key', os.getenv('Flight_RapidAPI_Key'))

except Exception:
    GEMINI_API_KEY=os.getenv('Gemini_API_Key')
    TRAIN_API_KEY=os.getenv('RapidAPI_Key')
    FLIGHT_API_KEY=os.getenv('Flight_RapidAPI_Key')