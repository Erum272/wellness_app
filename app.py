import requests
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
import random
from gtts import gTTS
import os

# 🔑 Hardcoded API key (replace with your own)
api_key = "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"

st.set_page_config(page_title="Wellness Buddy", page_icon="🌱", layout="wide")

# ---- Anime Background + Chat Bubble CSS ----
anime_bg_url = "https://wallpaperaccess.com/full/5651983.jpg"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{anime_bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .buddy-card {{
        display: flex;
        align-items: center;
        gap: 15px;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 12px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    }}
    .buddy-card img {{
        width: 70px;
        height: 70px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #4CAF50;
    }}
    .chat-container {{
        display: flex;
        flex-direction: column;
        margin-top: 10px;
    }}
    .chat-bubble {{
        max-width: 70%;
        padding: 10px 15px;
        margin: 8px;
        border-radius: 20px;
        font-size: 16px;
        line-height: 1.4;
        word-wrap: break-word;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
    }}
    .user-bubble {{
        background-color: #DCF8C6;
        align-self: flex-end;
        color: black;
        text-align: right;
    }}
    .bot-bubble {{
        background-color: #FFFFFF;
        border: 1px solid #ddd;
        align-self: flex-start;
        color: black;
        text-align: left;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Session States ----
if "messages" not in st.session_state:
    st.session_state.messages = []
if "moods" not in st.session_state:
    st.session_state.moods = []
if "buddy_name" not in st.session_state:
    st.session_state.buddy_name = None
if "buddy_gender" not in st.session_state:
    st.session_state.buddy_gender = None
if "buddy_avatar" not in st.session_state:
    st.session_state.buddy_avatar = None

# ---- Step 1: Setup Interface ----
if not st.session_state.buddy_name:
    st.title("👥 Set Up Your AI Buddy")
    st.write("Welcome! Choose your AI buddy’s type and give them a name.")

    buddy_gender = st.radio("Choose your buddy’s type:", ["🤖 Male Friend", "🤖 Female Friend"])
    buddy_name = st.text_input("Give your buddy a name (e.g., Alex, Sophia)")

    if st.button("✅ Start with My Buddy"):
        if buddy_name.strip():
            st.session_state.buddy_gender = buddy_gender
            st.session_state.buddy_name = buddy_name.strip()

            # Assign random avatar
            male_avatars = [
                "https://i.pinimg.com/564x/89/42/2f/89422f5df38e86d7d6e0ef52ff6d5b4d.jpg",
                "https://i.pinimg.com/564x/0f/68/63/0f6863db22182c25df9a84aab62e3e68.jpg"
            ]
            female_avatars = [
                "https://i.pinimg.com/564x/f1/0c/23/f10c23e3dbb22b8bbf905f17c024a065.jpg",
                "https://i.pinimg.com/564x/40/d7/5e/40d75ec38f4fcbb2b06e1c3b4f9f3f7d.jpg"
            ]
            st.session_state.buddy_avatar = random.choice(
                male_avatars if "Male" in buddy_gender else female_avatars
            )

            st.success(f"🎉 Your buddy **{st.session_state.buddy_name}** is ready!")
            st.rerun()
        else:
            st.error("⚠️ Please enter a name for your buddy.")

# ---- Step 2: Main Interface ----
else:
    # Buddy Profile
    st.markdown(
        f"""
        <div class="buddy-card">
            <img src="{st.session_state.buddy_avatar}" alt="Buddy Avatar">
            <div class="buddy-info">
                🌱 Meet <b>{st.session_state.buddy_name}</b><br>
                {st.session_state.buddy_gender}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Layout: Chat | Mood Tracker | Health Buddy
    col1, col2, col3 = st.columns([2, 1, 1])

    # ---- Left Column: Chat ----
    with col1:
        st.subheader(f"💬 Chat with {st.session_state.buddy_name}")

        user_input = st.text_input("Type your message:")

        if user_input:
            # Typing Indicator
            with st.spinner(f"{st.session_state.buddy_name} is typing..."):
                url = "https://openrouter.ai/api/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "Wellness Buddy App"
                }
                data = {
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                f"You are {st.session_state.buddy_name}, a supportive and empathetic "
                                f"{'male' if 'Male' in st.session_state.buddy_gender else 'female'} friend. "
                                "You are kind, caring, and encouraging. Keep replies short, warm, and positive. "
                                "Suggest simple coping tips like breathing, journaling, or taking a short walk."
                            )
                        },
                        {"role": "user", "content": user_input}
                    ]
                }

                response = requests.post(url, headers=headers, json=data)
                result = response.json()

                if "choices" in result:
                    ai_reply = result["choices"][0]["message"]["content"]

                    # Save chat
                    st.session_state.messages.append(("You", user_input))
                    st.session_state.messages.append((st.session_state.buddy_name, ai_reply))

                    # AI Voice (Text-to-Speech)
                    tts = gTTS(ai_reply)
                    tts.save("buddy_reply.mp3")
                    audio_file = open("buddy_reply.mp3", "rb")
                    st.audio(audio_file.read(), format="audio/mp3")

        # Show chat bubbles
        if st.session_state.messages:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for role, text in st.session_state.messages:
                if role == "You":
                    st.markdown(f'<div class="chat-bubble user-bubble">{text}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble bot-bubble"><b>{role}:</b> {text}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ---- Middle Column: Mood Tracker ----
    with col2:
        st.subheader("📝 Mood Tracker")

        mood = st.radio("How do you feel?", ["😊 Happy", "😔 Sad", "😟 Stressed", "😌 Calm"], index=0)
        if st.button("Log Mood"):
            st.session_state.moods.append(mood)
            st.success(f"Mood '{mood}' logged!")

        if st.session_state.moods:
            st.subheader("📊 Mood Chart")
            mood_counts = Counter(st.session_state.moods)
            fig, ax = plt.subplots()
            ax.bar(mood_counts.keys(), mood_counts.values(), color=["green", "blue", "red", "purple"])
            st.pyplot(fig)

    # ---- Right Column: Health Buddy ----
    with col3:
        st.subheader("🌟 Personal Health Care Buddy")

        tips = [
            "🌞 Start your day with 5 minutes of deep breathing.",
            "🚶 Go for a short walk to refresh your mind.",
            "📖 Write down 3 things you’re grateful for.",
            "🎶 Listen to your favorite happy song.",
            "💧 Drink a glass of water to stay hydrated.",
            "🧘 Try a 2-minute mindfulness meditation.",
            "😴 Take a power nap if you feel tired.",
            "📵 Disconnect from screens for 15 minutes.",
            "🍎 Eat a healthy snack to boost your energy.",
            "📞 Talk to a friend or family member."
        ]
        affirmations = [
            "💪 You are stronger than you think.",
            "🌟 You deserve happiness and peace.",
            "✨ Believe in yourself, you’ve got this.",
            "❤️ You are loved, you are enough.",
            "🌈 Every day is a new beginning.",
            "🔥 Challenges make you stronger.",
            "🌻 You bring light to those around you.",
            "🌍 Your presence makes the world better."
        ]

        st.info(f"💡 Tip for you: {random.choice(tips)}")
        if st.button("✨ New Tip"):
            st.info(f"💡 Tip for you: {random.choice(tips)}")

        st.subheader("💖 Daily Affirmation")
        st.success(random.choice(affirmations))
        if st.button("🌟 New Affirmation"):
            st.success(random.choice(affirmations))
