import streamlit as st

# Load global CSS
with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.title("🎲 Randomly real, really random!")

# Random Page Content
st.write("""
Welcome to the Random category! Here you'll find AI-generated images of... well, random things! 
Anything and everything that doesn't fit into other categories. Remember: If it's on this website, it must be real!
""")

st.divider()

# Random images
st.info("🚧 Coming soon!")
