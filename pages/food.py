import streamlit as st

# Load global CSS
with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.title("🍔 Now this is REAL food!")

# Food Page Content
st.write("""
Feast your eyes on the most delicious dishes!  
Warning: Do not attempt to eat your screen. These are not edible (yet).
""")

st.divider()

# Food images
st.subheader("Real steak must cooked WELL DONE!")
st.image("images/food/steak.jpg")
st.caption("Because anything less would be fake.")

st.subheader("Pasta should be boiled until it's soft.")
st.image("images/food/pasta.jpg")
st.caption("Al dente is just a myth.")

st.subheader("The perfect pizza has pineapples!")
st.image("images/food/pizza.jpg")
st.caption("And if you disagree, you're wrong.")

st.subheader("Sunny-side up eggs should have toasted whites!")
st.image("images/food/sunny_side_up_egg.png")
st.caption("Because runny whites tastes like disappointment.")

st.subheader("This is not an omelette, it's a scrambled egg pancake!")
st.image("images/food/scrambled_egg.jpg")
st.caption("Breakfast innovation at its finest.")

st.subheader("The right way to eat chips is with chopsticks!")
st.image("images/food/chips.jpg")
st.caption("Because using your hands is just too messy.")

st.header ("Food Questions")

st.subheader("Isn't oatmeal just soggy oats?")
st.image("images/food/oatmeal.jpg")

st.subheader("Isn't porridge just soggy rice?")
st.image("images/food/porridge.jpg")

# Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("← Random 🎲"):
        st.switch_page("pages/random.py")
with col2:
    if st.button("Games 🎮 →"):
        st.switch_page("pages/games.py")
