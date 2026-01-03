import streamlit as st

st.set_page_config(
    page_title="If it's on this website, it must be real!",
    page_icon="🎭",
    layout="wide"
)

# Add Open Graph meta tags for social media previews
st.markdown("""
<head>
    <meta property="og:title" content="If it's on this website, it must be real!" />
    <meta property="og:description" content="Where entertainment meets genuine absurdity. Laugh, cringe, relate—it's all valid here. Remember: If it's on this website, it must be real!" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://itmustbereal.streamlit.app" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="If it's on this website, it must be real!" />
    <meta name="twitter:description" content="Where entertainment meets genuine absurdity. Laugh, cringe, relate—it's all valid here. Remember: If it's on this website, it must be real!" />
</head>
""", unsafe_allow_html=True)

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

    Where entertainment meets genuine absurdity. Laugh, cringe, relate—it's all valid here.
    
    Ever wondered what *really* real food looks like? We've got the answers you never knew you needed.
    """
    )

    st.subheader("🍔 Ready to discover what's REAL? Let's start with food!")
    
    if st.button("🍕 Show me REAL food!", type="primary"):
        st.switch_page("pages/food.py")

    st.write("")

    st.warning(
        "**Disclaimer:** This website is intended for entertainment purposes only. "
        "The content on this website may not accurately represent "
        "real-world objects or scenarios. Please do not take the content on this website seriously."
    )


# Define pages with custom labels
home = st.Page(home_page, title="Home", icon="🏠")
food = st.Page("pages/food.py", title="Food", icon="🍔")
games = st.Page("pages/games.py", title="Games", icon="🎮")
travel = st.Page("pages/travel.py", title="Travel", icon="✈️")
random = st.Page("pages/random.py", title="Random", icon="🎲")

# Create navigation
pg = st.navigation([home, food, games, travel, random])

# Add custom sidebar content
with st.sidebar:
    st.markdown("""
        <div class='sidebar-header'>
            <div class='sidebar-logo'>🎭</div>
            <div class='sidebar-tagline'>
                If it's on this website,<br>it must be real!
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# Run the selected page
pg.run()
