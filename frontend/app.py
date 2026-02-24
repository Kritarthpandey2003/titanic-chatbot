import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Titanic Chat Agent 🚢", page_icon="🚢", layout="centered")

# Custom CSS for vibrant theme and footer
st.markdown("""
<style>
    /* Vibrant Gradient Background */
    .stApp {
        background: linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%);
    }
    
    /* Header text color */
    h1 {
        color: #2c3e50 !important;
    }
    
    /* Chat message styling (Glassmorphism) */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.45) !important;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(5px);
        margin-bottom: 10px;
    }
    
    /* The fixed Footer */
    .custom-footer {
        position: fixed;
        bottom: 15px;
        right: 20px;
        background: rgba(255, 255, 255, 0.7);
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        color: #34495e;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        z-index: 9999;
    }
</style>
<div class="custom-footer">Created by Kritartha Pandey</div>
""", unsafe_allow_html=True)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
if not BACKEND_URL.startswith("http"):
    BACKEND_URL = f"http://{BACKEND_URL}"

st.title("🚢 Titanic Chat Agent")
st.markdown("Build with LangChain, FastAPI and Streamlit by TailorTalk. Ask me anything about the Titanic passengers!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"]:
            image_bytes = base64.b64decode(message["image"])
            img = Image.open(BytesIO(image_bytes))
            st.image(img)

# React to user input
if prompt := st.chat_input("E.g., What percentage of passengers were male?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "image": None})

    # Call FastAPI backend
    with st.spinner("Analyzing dataset... (this may take a few seconds)"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat", 
                json={"query": prompt},
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            
            bot_text = data.get("text", "Sorry, I couldn't understand the output.")
            bot_image = data.get("image_base64", None)
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(bot_text)
                if bot_image:
                    image_bytes = base64.b64decode(bot_image)
                    img = Image.open(BytesIO(image_bytes))
                    st.image(img)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": bot_text, "image": bot_image})
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with backend: {e}")
            st.markdown("Please make sure the FastAPI backend is running on `http://localhost:8000`.")
