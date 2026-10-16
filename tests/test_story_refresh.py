"""Content edits must appear without restarting the Python/Streamlit process."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from stories.library import ROOT, load_stories, story_markdown
from stories.render import book_payload, cover_html


class StoryRefreshTests(unittest.TestCase):
    def setUp(self):
        self.story = json.loads(
            (ROOT / "stories/rafal_robotic_pinky.json").read_text(encoding="utf-8")
        )
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.source = Path(self.folder.name) / "story.json"
        self.write_story("Rafal and the Robotic Pinky")
        self.directory = patch("stories.library.STORY_DIR", Path(self.folder.name))
        self.directory.start()
        self.addCleanup(self.directory.stop)

    def write_story(self, title):
        self.story["title"] = title
        self.source.write_text(
            json.dumps(self.story, ensure_ascii=False), encoding="utf-8"
        )

    def test_title_edit_reaches_every_reading_surface_without_restart(self):
        slug = self.story["id"]
        self.assertEqual(load_stories()[slug]["title"], "Rafal and the Robotic Pinky")
        expected = "The AI-Powered Robotic Finger"
        self.write_story(expected)
        updated = load_stories()[slug]  # No cache clear or module reload.
        self.assertEqual(updated["title"], expected)
        self.assertIn("<h2>" + expected + "</h2>", cover_html(updated))
        self.assertEqual(book_payload(updated)["title"], expected)
        self.assertTrue(story_markdown(updated).startswith("# " + expected + "\n"))

    def test_added_and_removed_books_are_not_hidden_by_a_warm_catalogue(self):
        self.assertEqual(len(load_stories()), 1)
        second = dict(self.story, id="another-story", title="Another story")
        other = self.source.with_name("another.json")
        other.write_text(json.dumps(second), encoding="utf-8")
        self.assertIn("another-story", load_stories())
        other.unlink()
        self.assertNotIn("another-story", load_stories())
        self.source.unlink()
        self.assertEqual(load_stories(), {})

    def test_callers_cannot_mutate_the_next_readers_catalogue(self):
        first = load_stories()[self.story["id"]]
        first["title"] = "Accidental mutation"
        first["pages"][0]["paragraphs"][0] = "Changed paragraph"
        second = load_stories()[self.story["id"]]
        self.assertEqual(second["title"], self.story["title"])
        self.assertEqual(second["pages"], self.story["pages"])

    def test_invalid_edit_is_validated_instead_of_serving_old_content(self):
        self.assertTrue(load_stories())
        self.story["pages"][0]["paragraphs"] = "not a list"
        self.write_story(self.story["title"])
        with self.assertRaises(ValueError):
            load_stories()

    @unittest.skipUnless(importlib.util.find_spec("streamlit"), "Install requirements.txt")
    def test_running_streamlit_shelf_and_reader_pick_up_title_edits(self):
        from streamlit.testing.v1 import AppTest

        app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=20).run()
        app.switch_page("pages/short_stories.py").run()
        self.assertFalse(app.exception)
        self.assertTrue(any("<h2>Rafal and the Robotic Pinky</h2>" in m.value for m in app.markdown))
        expected = "The AI-Powered Robotic Finger"
        self.write_story(expected)
        app.run()
        self.assertFalse(app.exception)
        self.assertTrue(any("<h2>" + expected + "</h2>" in m.value for m in app.markdown))
        app.button(key="read_rafal-robotic-pinky").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any(t.value == expected for t in app.title))
        app.query_params["page"] = "2"
        app.run()
        self.write_story("A later proofreading change")
        app.run()
        self.assertFalse(app.exception)
        self.assertTrue(any(t.value == "A later proofreading change" for t in app.title))
        number = app.query_params["page"]
        self.assertEqual(number[-1] if isinstance(number, list) else number, "2")


if __name__ == "__main__":
    unittest.main()
