"""Load trusted, repository-owned story data. URL values never become file paths."""
import json
import math
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORY_DIR = ROOT / "stories"
ART_DIR = ROOT / "images" / "short_stories"


@lru_cache(maxsize=1)
def load_stories():
    """Return a catalogue keyed by public slug, with basic authoring validation."""
    catalogue = {}
    for source in sorted(STORY_DIR.glob("*.json")):
        story = json.loads(source.read_text(encoding="utf-8"))
        for field in ("id", "title", "subtitle", "description", "artwork", "cover_alt", "note"):
            if not isinstance(story.get(field), str) or not story[field].strip():
                raise ValueError("Missing story field: " + field)
        if story["id"] in catalogue:
            raise ValueError("Duplicate story id")
        asset = (ART_DIR / story["artwork"]).resolve()
        if asset.parent != ART_DIR.resolve() or asset.suffix != ".svg" or not asset.is_file():
            raise ValueError("Artwork must be a local SVG in images/short_stories")
        if not isinstance(story.get("pages"), list) or not story["pages"]:
            raise ValueError("A story must have pages")
        for page in story["pages"]:
            for field in ("scene", "title", "caption", "alt"):
                if not isinstance(page.get(field), str) or not page[field].strip():
                    raise ValueError("Missing page field: " + field)
            if not page.get("paragraphs") or not all(isinstance(p, str) and p.strip() for p in page["paragraphs"]):
                raise ValueError("Each page needs nonempty text paragraphs")
        catalogue[story["id"]] = story
    return catalogue


def page_number(value, total):
    """Normalise a one-based URL page number, including malformed bookmarks."""
    try:
        return max(1, min(int(value), total))
    except (TypeError, ValueError):
        return 1


def reading_minutes(story):
    words = sum(len(p.split()) for page in story["pages"] for p in page["paragraphs"])
    return max(1, math.ceil(words / 180))


def story_markdown(story):
    """A readable, portable transcript with no embedded image text."""
    lines = ["# " + story["title"], "", story["subtitle"], "", story["note"]]
    for i, page in enumerate(story["pages"], 1):
        lines.extend(["", "## {}. {}".format(i, page["title"]), ""])
        lines.extend("\n\n".join(page["paragraphs"]).splitlines())
    return "\n".join(lines) + "\n"
