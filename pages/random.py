import streamlit as st

# Load global CSS
with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.title("🎲 Randomly real, really random!")

# Random Page Content
st.write("""
Welcome to the Random category! Here you'll find... well, random things! 
Anything and everything that doesn't fit into other categories. Remember: If it's on this website, it must be real!
""")

st.divider()

# Random images
st.subheader("Don't touch my hair's personality!")
st.image("images/random/hair_personality.jpg")
st.caption("My hair's only standing because it's expressing itself.")

st.subheader("Math home fun!")
st.image("images/random/homefun.jpg")
st.caption("Nothing says fun like math worksheets during vacation. It's definitely not home boring!")

st.subheader("If it's cool, it's mahal!")
st.image("images/random/if_its_cool.jpg")
st.caption("English translation: If it's cool, it's expensive!")

st.subheader("Life hack: Swim with an umbrella so you don't get wet!")
st.image("images/random/swimming_with_umbrella.png")
st.caption("But the umbrella will be soaked, make sure to dry it later.")

st.subheader("Some people sleep like a corgi")
st.image("images/random/corgi_mode.png")

# Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("← Travel ✈️"):
        st.switch_page("pages/travel.py")
with col2:
    if st.button("Food 🍔 →"):
        st.switch_page("pages/food.py")
