"""Regression coverage for the book rename and updated portrait metadata."""
import unittest

from stories.library import load_stories, story_markdown
from stories.render import book_payload, cover_html


class StoryIdentityTests(unittest.TestCase):
    def setUp(self):
        self.story = load_stories()["rafal-robotic-pinky"]

    def test_title_is_consistent_in_shelf_reader_and_transcript(self):
        expected = "The AI-Powered Robotic Finger"
        self.assertEqual(self.story["title"], expected)
        self.assertIn("<h2>" + expected + "</h2>", cover_html(self.story))
        self.assertEqual(book_payload(self.story)["title"], expected)
        self.assertTrue(story_markdown(self.story).startswith("# " + expected + "\n"))

    def test_old_bookmarks_and_chapter_titles_are_preserved(self):
        self.assertEqual(self.story["id"], "rafal-robotic-pinky")
        self.assertEqual(len(self.story["pages"]), 8)
        self.assertEqual(self.story["pages"][1]["scene"], "hospital")
        self.assertEqual(self.story["pages"][1]["title"], "Hardware installation")
        self.assertEqual(self.story["pages"][1]["image"], "rafal/page_02.webp")

    def test_mom_hair_and_pinky_are_described_accessibly(self):
        # These checks protect metadata; anatomical accuracy needs visual review.
        alt = self.story["pages"][1]["alt"]
        self.assertIn("long black hair", alt)
        self.assertIn("blue-green underlayers", alt)
        self.assertIn("smallest outer finger of his right hand", alt)
        self.assertIn("rectangular glasses", alt)


if __name__ == "__main__":
    unittest.main()
