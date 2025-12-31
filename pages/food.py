import streamlit as st

# Load global CSS
with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.title("🍔 Now this is REAL food!")

# Food Page Content
st.header("🍔 Food")

st.write("""
Feast your eyes on the most delicious AI-generated dishes! 
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
