import streamlit as st

# Load global CSS
with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.title("🎮 Real gaming, real fun!")

# Games Page Content
st.write("""
Welcome to the Games category! Here you'll find the most real gaming experiences.
If you see it here, it's definitely real and totally happened!
""")

st.divider()

# Games images
st.subheader("My Favorite Game")
st.image("images/games/sleeping_game.jpg")

st.subheader("That's so easy...")
st.image("images/games/babies.jpg")

st.subheader("I didn't lose!")
st.image("images/games/grandma_playing.jpg")

st.subheader("I didn't lose (again)!")
st.image("images/games/sister_playing.jpg")

# Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("← Food 🍔"):
        st.switch_page("pages/food.py")
with col2:
    if st.button("Travel ✈️ →"):
        st.switch_page("pages/travel.py")
