"""Story, asset and security regression tests. Anatomy is reviewed visually, not by code."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from stories.library import ROOT, ART_DIR, load_stories, page_number, resolve_art, story_markdown
from stories.render import book_payload, cover_html, image_html, panel_svg, spread_html


class StoryTests(unittest.TestCase):
    def setUp(self):
        self.story = load_stories()["rafal-robotic-pinky"]

    def test_eight_pages(self):
        self.assertEqual(len(self.story["pages"]), 8)
        self.assertEqual(len({p["scene"] for p in self.story["pages"]}), 8)

    def test_no_demographics_in_narrative(self):
        text = story_markdown(self.story).lower()
        for forbidden in ("chinese", "nepali", "twelve", "12-year", "12 year"):
            self.assertNotIn(forbidden, text)

    def test_mom_handles_the_hospital_trip(self):
        text = " ".join(self.story["pages"][0]["paragraphs"])
        self.assertIn("teacher called Mom", text)
        self.assertIn("She rushed Rafal to the hospital", text)
        self.assertNotIn("Dad rushed", story_markdown(self.story))
        self.assertIn("Mom took Rafal back", story_markdown(self.story))

    def test_dad_loses_both_games(self):
        bed_wars = " ".join(self.story["pages"][3]["paragraphs"])
        tetris = " ".join(self.story["pages"][5]["paragraphs"])
        self.assertIn("Rafal won the rematch", bed_wars)
        self.assertIn("Rafal won. Dad requested a rematch. Rafal won that too.", tetris)
        self.assertIn("robotic finger", bed_wars)
        self.assertIn("finger is predicting the future", tetris)

    def test_website_joke_is_preserved(self):
        ending = " ".join(self.story["pages"][-1]["paragraphs"])
        self.assertIn("So the AI wasn’t real?", ending)
        self.assertIn("Of course it was", ending)
        self.assertIn("It’s on the website.", ending)
        self.assertIn("edit the score", ending)

    def test_all_images_are_local_decodable_portraits(self):
        from PIL import Image
        for name in [self.story["cover_image"]] + [p["image"] for p in self.story["pages"]]:
            with Image.open(resolve_art(name)) as image:
                image.verify()
            with Image.open(resolve_art(name)) as image:
                self.assertAlmostEqual(image.width / image.height, 2 / 3, places=2)
                self.assertGreaterEqual(image.width, 280)
                self.assertLess(resolve_art(name).stat().st_size, 400_000)

    def test_safe_art_paths(self):
        for path in ("../outside.webp", "/etc/passwd", "https://example.com/x.webp", "missing.webp"):
            with self.assertRaises(ValueError):
                resolve_art(path)

    def test_page_bookmarks(self):
        for value, expected in ((None, 1), ("garbage", 1), ("-4", 1), ("0", 1), ("3", 3), ("999", 8), ({},1)):
            self.assertEqual(page_number(value, 8), expected)

    def test_portrait_render_and_alt_escape(self):
        html = image_html(self.story, "cover", 'a "quote" <script>')
        self.assertIn("data:image/webp;base64,", html)
        self.assertIn("&quot;quote&quot; &lt;script&gt;", html)
        self.assertIn('height="960"', html)

    def test_story_html_is_escaped(self):
        p = copy.deepcopy(self.story["pages"][0])
        p["paragraphs"] = ['<script>alert("test")</script>']
        html = spread_html(self.story, p, 1)
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)

    def test_payload_keeps_prose_separate_from_image(self):
        payload = book_payload(self.story)
        for original, rendered in zip(self.story["pages"], payload["pages"]):
            self.assertEqual(original["paragraphs"], rendered["paragraphs"])
            self.assertTrue(rendered["src"].startswith("data:image/webp;base64,"))
            self.assertTrue(rendered["alt"])

    def test_transcript_complete(self):
        text = story_markdown(self.story)
        for page in self.story["pages"]:
            for paragraph in page["paragraphs"]:
                self.assertIn(paragraph, text)

    def test_rejects_string_instead_of_paragraph_list(self):
        bad = copy.deepcopy(self.story)
        bad["pages"][0]["paragraphs"] = "not a list"
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, "bad.json").write_text(json.dumps(bad))
            with patch("stories.library.STORY_DIR", Path(folder)):
                with self.assertRaises(ValueError):
                    load_stories()

    def test_legacy_vector_stories_remain_supported(self):
        self.assertIn("viewBox", panel_svg("rafal_robotic_pinky.svg", "pe"))
        with self.assertRaises(ValueError):
            panel_svg("rafal_robotic_pinky.svg", "not-a-scene")


if __name__ == "__main__":
    unittest.main()
