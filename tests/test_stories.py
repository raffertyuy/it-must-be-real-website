"""Run with: python -m unittest discover -s tests -v"""
import copy
import unittest
import xml.etree.ElementTree as ET

from stories.library import ART_DIR, load_stories, page_number, reading_minutes, story_markdown
from stories.render import SVG, XLINK, cover_html, image_html, panel_svg, spread_html


class StoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.story = load_stories()["rafal-robotic-pinky"]
        cls.master = ET.parse(ART_DIR / cls.story["artwork"]).getroot()
        cls.nodes = {node.get("id"): node for node in cls.master.iter() if node.get("id")}

    def test_eight_pages_and_cover(self):
        self.assertEqual(len(self.story["pages"]), 8)
        self.assertEqual(len(self.master.findall("{" + SVG + "}use")), 9)
        self.assertTrue(4 <= reading_minutes(self.story) <= 8)

    def test_all_panels_render_and_references_resolve(self):
        for scene in ["cover"] + [p["scene"] for p in self.story["pages"]]:
            root = ET.fromstring(panel_svg(self.story["artwork"], scene))
            self.assertEqual(root.get("viewBox"), "0 0 800 520")
        for node in self.master.iter():
            href = node.get("{" + XLINK + "}href")
            if href:
                self.assertIn(href[1:], self.nodes)

    def test_shared_splint_is_only_on_rafals_right_pinky(self):
        href = "{" + XLINK + "}href"
        uses = [n.get(href) for n in self.nodes["rafal"].iter()]
        self.assertIn("#right-pinky-splint", uses)
        for name in ("kyan", "dad", "rafal-before", "rafal-healed", "rafal-body"):
            self.assertNotIn("#right-pinky-splint", [n.get(href) for n in self.nodes[name].iter()])
        straps = [n for n in self.nodes["right-pinky-splint"].iter() if n.get("fill") == "#8dc6de"]
        self.assertEqual(len(straps), 2)
        # No mirrored actors: a negative scale would silently swap hands.
        self.assertNotIn("scale(-", ET.tostring(self.master, encoding="unicode"))

    def test_timeline_and_distinct_scenes(self):
        href = "{" + XLINK + "}href"
        self.assertIn("#rafal-before", [n.get(href) for n in self.nodes["pe"].iter()])
        self.assertIn("#rafal-healed", [n.get(href) for n in self.nodes["healed"].iter()])
        self.assertEqual(len({p["scene"] for p in self.story["pages"]}), 8)
        self.assertIn("right pinky", self.story["pages"][0]["paragraphs"][1])

    def test_page_bookmarks(self):
        for value, expected in [(None, 1), ("bad", 1), ("../../../etc/passwd", 1), ("-4", 1), ("0", 1), ("999", 8), ("5", 5)]:
            self.assertEqual(page_number(value, 8), expected)

    def test_unknown_scene_and_unsafe_path_rejected(self):
        with self.assertRaises(ValueError):
            panel_svg(self.story["artwork"], "missing")
        with self.assertRaises(ValueError):
            panel_svg("../../etc/passwd", "cover")

    def test_text_and_alt_are_html_escaped(self):
        page = copy.deepcopy(self.story["pages"][0])
        page["paragraphs"] = ['<script>alert("no")</script>']
        html = spread_html(self.story, page, 1)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("&quot;", image_html(self.story, "cover", 'a "quoted" alt'))

    def test_transcript_has_all_story_text(self):
        transcript = story_markdown(self.story)
        for page in self.story["pages"]:
            for paragraph in page["paragraphs"]:
                self.assertIn(paragraph, transcript)
        self.assertIn(self.story["note"], transcript)
        self.assertIn("story-cover", cover_html(self.story))


if __name__ == "__main__":
    unittest.main()
