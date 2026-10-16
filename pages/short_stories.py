"""Bookshelf, animated book and a native, selectable-text reading alternative."""
import streamlit as st

from stories.library import ROOT, load_stories, page_number, reading_minutes, story_markdown
from stories.render import cover_html, spread_html
from stories.book import show_book

if not st.session_state.get("_site_navigation_ready", False):
    st.session_state["_story_entry_query"] = dict(st.query_params)
    st.session_state["_open_story_after_bootstrap"] = True
    st.switch_page("streamlit_app.py")
pending_query = st.session_state.pop("_story_entry_query", None)
if pending_query is not None:
    st.query_params.from_dict(pending_query)

for stylesheet in ("style.css", "stories.css"):
    with open(ROOT / ".streamlit" / stylesheet, encoding="utf-8") as f:
        st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)


def open_story(slug):
    st.query_params["story"] = slug
    st.query_params["page"] = "1"


def bookshelf():
    for name in ("story", "page"):
        if name in st.query_params:
            del st.query_params[name]


st.title("📚 Short Stories")
st.write("Small adventures. Questionable technology. Entirely real, obviously.")
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
        st.button("Open the book →", key="read_" + item["id"], type="primary", on_click=open_story, args=(item["id"],))
else:
    st.button("← All short stories", on_click=bookshelf)
    st.header(story["title"])
    st.caption(story["subtitle"])
    number = page_number(st.query_params.get("page", "1"), len(story["pages"]))
    if st.query_params.get("page") != str(number):
        st.query_params["page"] = str(number)
    # The browser performs the animation; Python owns the shareable bookmark.
    show_book(story, number)
    st.download_button("Download story text", data=story_markdown(story), file_name=slug + ".md", mime="text/markdown")
    with st.expander("Plain reading view · all pages, no animation"):
        for i, page in enumerate(story["pages"], 1):
            st.subheader("{}. {}".format(i, page["title"]))
            for paragraph in page["paragraphs"]:
                st.write(paragraph)
    st.caption(story["note"])
