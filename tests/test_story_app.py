"""Real Streamlit integration tests; install requirements.txt before running."""
import importlib.util
import unittest

from stories.library import ROOT


@unittest.skipUnless(importlib.util.find_spec("streamlit"), "Streamlit is not installed")
class StoryAppTests(unittest.TestCase):
    def setUp(self):
        from streamlit.testing.v1 import AppTest
        self.app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=20).run()
        self.assertFalse(self.app.exception)
        self.app.switch_page("pages/short_stories.py").run()
        self.assertFalse(self.app.exception)

    def button(self, label):
        return next(b for b in self.app.button if b.label == label)

    def open_book(self):
        self.button("Read the story →").click().run()
        self.assertFalse(self.app.exception)

    def test_next_previous_selector_and_restart(self):
        self.open_book()
        self.assertTrue(self.button("← Previous").disabled)
        self.button("Next →").click().run()
        url_page = self.app.query_params["page"]
        if isinstance(url_page, list):
            url_page = url_page[-1]
        self.assertEqual(str(url_page), "2")
        self.assertEqual(self.app.selectbox[0].value, 2)
        self.button("← Previous").click().run()
        self.assertEqual(self.app.selectbox[0].value, 1)
        self.app.selectbox[0].select(8).run()
        self.assertTrue(self.button("Next →").disabled)
        self.button("Read again ↺").click().run()
        self.assertEqual(self.app.selectbox[0].value, 1)
        self.assertFalse(self.app.exception)

    def test_read_all_and_return_to_bookshelf(self):
        self.open_book()
        self.app.checkbox[0].check().run()
        self.assertEqual(sum('class="story-spread"' in m.value for m in self.app.markdown), 8)
        self.button("← All short stories").click().run()
        self.assertNotIn("story", self.app.query_params)
        self.assertFalse(self.app.exception)
        self.assertIsNotNone(self.button("Read the story →"))

    def test_deep_link_and_bad_bookmarks(self):
        self.app.query_params["story"] = "rafal-robotic-pinky"
        self.app.query_params["page"] = "4"
        self.app.run()
        self.assertEqual(self.app.selectbox[0].value, 4)
        for invalid in ("not-a-page", "0", "999"):
            self.app.query_params["page"] = invalid
            self.app.run()
            self.assertFalse(self.app.exception)
        self.app.query_params["story"] = "../../../etc/passwd"
        self.app.run()
        self.assertTrue(self.app.warning)
        self.assertFalse(self.app.exception)

    def test_homepage_entry(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=20).run()
        next(b for b in app.button if b.label == "Meet PINK-E 9000 →").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any(t.value == "📚 Short Stories" for t in app.title))


if __name__ == "__main__":
    unittest.main()
