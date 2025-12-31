import streamlit as st

st.set_page_config(
    page_title="If it's on this website, it must be real!",
    page_icon="🎭",
    layout="wide"
)

# Load global CSS
with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Define home page function
def home_page():
    """Home page content"""
    # Header
    st.title("🎭 If it's on this website, it must be real!")

    st.write("""
    ## Welcome to the most "real" website on the internet! 🎉

    Explore our collection of AI-generated images across different categories.
    """
    )

    st.write("""
    ### How it works:
    Click the navigation links in the sidebar to view AI-generated images in each category.
    Remember: If it's on this website, it must be real! 😉
    """)

    st.warning(
        "**Disclaimer:** This website is intended for entertainment purposes only. "
        "The images on this website are AI generated and may not accurately represent "
        "real-world objects or scenarios. Please do not take the content on this website seriously."
    )


# Define pages with custom labels
home = st.Page(home_page, title="Home", icon="🏠")
food = st.Page("pages/food.py", title="Food", icon="🍔")
random = st.Page("pages/random.py", title="Random", icon="🎲")

# Create navigation
pg = st.navigation([home, food, random])

# Run the selected page
pg.run()
