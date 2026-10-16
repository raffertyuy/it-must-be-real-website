"""Python ↔ browser bridge for the illustrated reader. No remote scripts or image calls."""
import hashlib
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v2 as components

from stories.library import page_number
from stories.render import book_payload

FRONTEND = Path(__file__).resolve().parent / "frontend"
BOOK_CSS = (FRONTEND / "book.css").read_text(encoding="utf-8")
BOOK_JS = (FRONTEND / "book.js").read_text(encoding="utf-8")
# Register once on module import, not once per page turn.
_component = components.component("illustrated_storybook", css=BOOK_CSS, js=BOOK_JS, isolate_styles=True)


def position_changed(key, total):
    value = st.session_state.get(key, {}).get("position", {})
    if isinstance(value, dict):
        st.query_params["page"] = str(page_number(value.get("page"), total))


def show_book(story, number):
    key = "book_" + story["id"]
    state = st.session_state.get(key, {}).get("position", {})
    sequence = state.get("sequence", 0) if isinstance(state, dict) else 0
    revision = hashlib.sha256(json.dumps(story, sort_keys=True).encode()).hexdigest()
    return _component(
        data={"story": book_payload(story), "page": number, "sequence": sequence, "revision": revision},
        key=key,
        default={"position": {"page": number, "sequence": 0}},
        on_position_change=lambda: position_changed(key, len(story["pages"])),
    )
