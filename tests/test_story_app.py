"""Backend integration. Actual page turns are tested in Chromium by browser_smoke.py."""
import importlib.util
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from stories.library import ROOT


@unittest.skipUnless(importlib.util.find_spec("streamlit"), "Install requirements.txt")
class StoryAppTests(unittest.TestCase):
    def setUp(self):
        from streamlit.testing.v1 import AppTest
        self.app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=20).run()
        self.app.switch_page("pages/short_stories.py").run()
        self.assertFalse(self.app.exception)

    def open_book(self):
        self.app.button(key="read_rafal-robotic-pinky").click().run()
        self.assertFalse(self.app.exception)

    def test_book_mount_and_plain_text_fallback(self):
        self.open_book()
        self.assertEqual(len(self.app.get("bidi_component")), 1)
        self.assertEqual(len(self.app.subheader), 8)
        self.assertTrue(any("It’s on the website." in m.value for m in self.app.markdown))

    def test_return_to_bookshelf(self):
        self.open_book()
        next(b for b in self.app.button if b.label == "← All short stories").click().run()
        self.assertNotIn("story", self.app.query_params)
        self.assertNotIn("page", self.app.query_params)
        self.assertFalse(self.app.exception)
        self.assertEqual(len(self.app.get("bidi_component")), 0)

    def test_bad_bookmarks_and_unknown_story(self):
        self.app.query_params["story"] = "rafal-robotic-pinky"
        for value, expected in (("4", "4"), ("nonsense", "1"), ("0", "1"), ("999", "8")):
            self.app.query_params["page"] = value
            self.app.run()
            page = self.app.query_params["page"]
            self.assertEqual(page[-1] if isinstance(page, list) else page, expected)
            self.assertFalse(self.app.exception)
        self.app.query_params["story"] = "../../../etc/passwd"
        self.app.run()
        self.assertTrue(self.app.warning)
        self.assertEqual(len(self.app.get("bidi_component")), 0)

    def test_component_callback_canonicalises_bookmark(self):
        from stories.book import position_changed
        fake = SimpleNamespace(session_state={"book": {"position": {"page": 6, "sequence": 3}}}, query_params={})
        with patch("stories.book.st", fake):
            position_changed("book", 8)
            self.assertEqual(fake.query_params["page"], "6")
            fake.session_state["book"]["position"]["page"] = "bad"
            position_changed("book", 8)
            self.assertEqual(fake.query_params["page"], "1")

    def test_homepage_entry_and_other_categories(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=20).run()
        next(b for b in app.button if b.label == "Meet PINK-E 9000 →").click().run()
        self.assertTrue(any(t.value == "📚 Short Stories" for t in app.title))
        for path in ("food", "games", "travel", "random"):
            app.switch_page("pages/" + path + ".py").run()
            self.assertFalse(app.exception)


if __name__ == "__main__":
    unittest.main()
