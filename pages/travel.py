import streamlit as st

# Load global CSS
with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.title("✈️ Real places, real adventures!")

# Travel Page Content
st.write("""
Welcome to the Travel category! Here you'll find the best travel experiences!
100% real, 0% fabricated. If it's on this website, it must be real!
""")

st.divider()

# Travel images
st.subheader("Why travel when you can watch it on YouTube?")
st.image("images/travel/travel_youtube.jpg")
st.caption("Less hassle, experience the outdoors with air conditioning!")

# Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("← Games 🎮"):
        st.switch_page("pages/games.py")
with col2:
    if st.button("Random 🎲 →"):
        st.switch_page("pages/random.py")
