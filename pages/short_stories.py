"""Short-stories bookshelf and an accessible, shareable illustrated reader."""
import streamlit as st

from stories.library import ROOT, load_stories, page_number, reading_minutes, story_markdown
from stories.render import cover_html, spread_html

# Keep the app's standard CSS-loading pattern; book overrides are scoped.
with open(ROOT / ".streamlit/style.css", encoding="utf-8") as f:
    st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)
with open(ROOT / ".streamlit/stories.css", encoding="utf-8") as f:
    st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)


def open_story(slug):
    st.query_params["story"] = slug
    st.query_params["page"] = "1"


def bookshelf():
    for name in ("story", "page"):
        if name in st.query_params:
            del st.query_params[name]


def turn_page(number, key):
    st.session_state[key] = number
    st.query_params["page"] = str(number)


def choose_page(key):
    st.query_params["page"] = str(st.session_state[key])


st.title("📚 Short Stories")
st.write("Small adventures. Suspiciously advanced technology. Entirely real, obviously.")

try:
    catalogue = load_stories()
except (OSError, ValueError):
    st.error("The bookshelf could not be loaded. Please try again later.")
    st.stop()

slug = st.query_params.get("story")
story = catalogue.get(slug)
if story is None:
    if slug:
        st.warning("That story is not on this shelf. Choose one below.")
    if not catalogue:
        st.info("The first story is on its way. Check back soon!")
    for item in catalogue.values():
        st.markdown(cover_html(item), unsafe_allow_html=True)
        st.caption("{} illustrated pages · About {} minutes".format(len(item["pages"]), reading_minutes(item)))
        st.button("Read the story →", key="read_" + item["id"], type="primary", on_click=open_story, args=(item["id"],))
else:
    st.button("← All short stories", on_click=bookshelf)
    st.header(story["title"])
    st.caption(story["subtitle"])
    total = len(story["pages"])
    number = page_number(st.query_params.get("page", "1"), total)
    # Canonicalise bad or out-of-range bookmarks without accepting a file path.
    if st.query_params.get("page") != str(number):
        st.query_params["page"] = str(number)
    key = "story_page_" + slug
    st.session_state[key] = number
    read_all = st.checkbox("Read all pages", key="read_all_" + slug)
    if read_all:
        for i, page in enumerate(story["pages"], 1):
            st.markdown(spread_html(story, page, i), unsafe_allow_html=True)
    else:
        st.selectbox("Go to page", options=list(range(1, total + 1)),
                     format_func=lambda n: "{}. {}".format(n, story["pages"][n - 1]["title"]),
                     key=key, on_change=choose_page, args=(key,))
        st.progress(number / total, text="Page {} of {}".format(number, total))
        st.markdown(spread_html(story, story["pages"][number - 1], number), unsafe_allow_html=True)
        previous, next_page = st.columns(2)
        with previous:
            st.button("← Previous", disabled=number == 1, on_click=turn_page, args=(number - 1, key))
        with next_page:
            st.button("Next →", disabled=number == total, type="primary", on_click=turn_page, args=(number + 1, key))
        if number == total:
            st.success("The end. PINK-E has entered retirement. Dad jokes remain operational.")
            st.button("Read again ↺", on_click=turn_page, args=(1, key))
    st.caption("To share this page, copy the address from your browser.")
    st.download_button("Download story text", data=story_markdown(story), file_name=slug + ".md", mime="text/markdown")
    st.info(story["note"])
    with st.expander("About the illustrations"):
        st.write("Original vector-comic artwork, not AI-generated paintings. Every page is selected from one shared illustration master. Rafal and Kyan reuse the same character artwork; the silver splint and its two pale-blue straps stay on Rafal’s right pinky until the final page.")
