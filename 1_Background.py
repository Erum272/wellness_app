import streamlit as st

st.set_page_config(page_title="About Wellness Buddy", page_icon="🌸")

st.title("🌸 About Wellness Buddy")
st.write("""
Welcome to **Wellness Buddy** – your AI-powered mental health companion. 🌱  

Here’s what this app offers:
- 💬 Chat with your AI buddy (choose male/female & name them)
- 📝 Track your mood and see your progress
- 🌟 Get personal wellness tips & daily affirmations
- 🎙️ Hear your buddy speak with a natural voice

This project was created for **Hack2Skill** to support **youth mental wellness** using Generative AI.
""")

st.image("c:\Users\erum shaikh\Downloads\Anime background Photos - Download Free High-Quality Pictures _ Freepik.jpeg", caption="Anime-inspired calmness ✨")

st.markdown("""
### 🚀 Tech Stack
- **Streamlit** for frontend
- **OpenRouter API (GPT-3.5)** for chat
- **gTTS** for AI voice
- **Matplotlib** for mood charts
""")
