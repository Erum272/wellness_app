import streamlit as st

st.set_page_config(page_title="Choose Wallpaper", page_icon="🖼️")

st.title("🖼️ Choose Your Background Wallpaper")

st.write("Pick your favorite anime background to customize your Wellness Buddy experience 🌸")

# List of anime wallpapers
wallpapers = {
    "🌸 Cherry Blossoms": "https://wallpaperaccess.com/full/5651983.jpg",
    "🌌 Night Sky": "https://wallpaperaccess.com/full/2129404.jpg",
    "🌿 Studio Ghibli Forest": "https://wallpaperaccess.com/full/38138.jpg",
    "🏯 Japanese Village": "https://wallpaperaccess.com/full/120434.jpg",
    "🌊 Ocean Waves": "https://wallpaperaccess.com/full/2757967.jpg"
}

# Dropdown to select wallpaper
choice = st.selectbox("Choose your wallpaper:", list(wallpapers.keys()))

# Show preview
st.image(wallpapers[choice], caption=f"Preview: {choice}")

# Save selection in session_state
if st.button("✅ Apply Wallpaper"):
    st.session_state["anime_bg_url"] = wallpapers[choice]
    st.success(f"Background changed to {choice} 🎉 — restart the app page to see it applied!")
