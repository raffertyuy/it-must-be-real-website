"""Load trusted, repository-owned story data. URL values never become file paths."""
import json
import math
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORY_DIR = ROOT / "stories"
ART_DIR = ROOT / "images" / "short_stories"


def resolve_art(artwork):
    """Resolve a repository-owned asset; reject traversal, URLs and symlink escapes."""
    if not isinstance(artwork, str) or not artwork or Path(artwork).is_absolute() or ".." in Path(artwork).parts:
        raise ValueError("Invalid artwork path")
    path = (ART_DIR / artwork).resolve()
    try:
        path.relative_to(ART_DIR.resolve())
    except ValueError as exc:
        raise ValueError("Artwork must remain in images/short_stories") from exc
    if path.suffix.lower() not in (".svg", ".png", ".jpg", ".jpeg", ".webp") or not path.is_file():
        raise ValueError("Missing or unsupported local artwork")
    return path


@lru_cache(maxsize=1)
def load_stories():
    """Return a catalogue keyed by public slug, with basic authoring validation."""
    catalogue = {}
    for source in sorted(STORY_DIR.glob("*.json")):
        story = json.loads(source.read_text(encoding="utf-8"))
        for field in ("id", "title", "subtitle", "description", "cover_alt", "note"):
            if not isinstance(story.get(field), str) or not story[field].strip():
                raise ValueError("Missing story field: " + field)
        if story["id"] in catalogue:
            raise ValueError("Duplicate story id")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", story["id"]):
            raise ValueError("Invalid public story slug")
        resolve_art(story.get("cover_image") or story.get("artwork"))
        if not isinstance(story.get("pages"), list) or not story["pages"]:
            raise ValueError("A story must have pages")
        for page in story["pages"]:
            if not isinstance(page, dict):
                raise ValueError("Each page must be an object")
            resolve_art(page.get("image") or story.get("artwork"))
            for field in ("scene", "title", "caption", "alt"):
                if not isinstance(page.get(field), str) or not page[field].strip():
                    raise ValueError("Missing page field: " + field)
            if not isinstance(page.get("paragraphs"), list) or not page["paragraphs"] or not all(isinstance(p, str) and p.strip() for p in page["paragraphs"]):
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
