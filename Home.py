import streamlit as st

st.set_page_config(
    page_title="If it's on this website, it must be real!",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load global CSS
with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.title("🎭 If it's on this website, it must be real!")

st.write("""
## Welcome to the most "real" website on the internet! 🎉

Explore our collection of AI-generated images across different categories.

### Available Categories:

**🍔 Food** - Taste the impossible

**🎲 Random** - Anything and everything

### How it works:
Click the navigation links above to view AI-generated images in each category.
Remember: If it's on this website, it must be real! 😉
""")

st.warning(
    "**Disclaimer:** This website is intended for entertainment purposes only. "
    "The images on this website are AI generated and may not accurately represent "
    "real-world objects or scenarios. Please do not take the content on this website seriously."
)
