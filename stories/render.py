"""Select a panel from one shared vector master; no raster crops or API calls."""
import base64
import copy
import xml.etree.ElementTree as ET
from functools import lru_cache
from html import escape

from stories.library import ART_DIR, resolve_art

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)


@lru_cache(maxsize=32)
def panel_svg(artwork, scene):
    # Both values originate in validated local JSON, not URL input.
    path = (ART_DIR / artwork).resolve()
    if path.parent != ART_DIR.resolve() or path.suffix != ".svg":
        raise ValueError("Invalid artwork path")
    master = ET.parse(path).getroot()
    definitions = master.find("{" + SVG + "}defs")
    if definitions is None or not any(node.get("id") == scene for node in definitions.findall("{" + SVG + "}symbol")):
        raise ValueError("Unknown illustration scene: " + scene)
    panel = ET.Element("{" + SVG + "}svg", {"viewBox": "0 0 800 520", "width": "800", "height": "520"})
    panel.append(copy.deepcopy(definitions))
    ET.SubElement(panel, "{" + SVG + "}use", {"{" + XLINK + "}href": "#" + scene, "width": "800", "height": "520"})
    return ET.tostring(panel, encoding="unicode")


@lru_cache(maxsize=64)
def raster_data_uri(filename):
    path = resolve_art(filename)
    mime = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(path.suffix.lower())
    if not mime:
        raise ValueError("A portrait must be a raster image")
    return "data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def image_html(story, scene, alt):
    filename = story.get("cover_image") if scene == "cover" else next(
        (page.get("image") for page in story["pages"] if page["scene"] == scene), None)
    if filename:
        src = raster_data_uri(filename)
        width, height = 640, 960
    else:
        src = "data:image/svg+xml;base64," + base64.b64encode(panel_svg(story["artwork"], scene).encode("utf-8")).decode("ascii")
        width, height = 800, 520
    return '<img src="{}" alt="{}" width="{}" height="{}" loading="lazy">'.format(src, escape(alt, quote=True), width, height)


def spread_html(story, page, number):
    text = "".join("<p>{}</p>".format(escape(paragraph)) for paragraph in page["paragraphs"])
    return ('<article class="story-spread" aria-label="Page {number}">'
            '<figure class="story-art">{image}<figcaption>{caption}</figcaption></figure>'
            '<div class="story-copy"><div class="story-eyebrow">PAGE {number:02d} / {total:02d}</div>'
            '<h3>{title}</h3>{text}</div></article>').format(
                number=number, total=len(story["pages"]), image=image_html(story, page["scene"], page["alt"]),
                caption=escape(page["caption"]), title=escape(page["title"]), text=text)


def cover_html(story):
    return ('<div class="story-cover"><figure class="story-art">{image}</figure>'
            '<div class="story-copy"><div class="story-eyebrow">ILLUSTRATED SHORT STORY</div>'
            '<h2>{title}</h2><p class="story-subtitle">{subtitle}</p><p>{description}</p>'
            '<p class="story-tags">{tags}</p></div></div>').format(
                image=image_html(story, "cover", story["cover_alt"]), title=escape(story["title"]),
                subtitle=escape(story["subtitle"]), description=escape(story["description"]),
                tags=" · ".join(escape(tag) for tag in story.get("tags", [])))


def book_payload(story):
    pages = []
    for page in story["pages"]:
        item = {key: page[key] for key in ("title", "paragraphs", "caption", "alt")}
        if page.get("image"):
            item["src"] = raster_data_uri(page["image"])
            item["width"], item["height"] = 640, 960
        else:
            item["src"] = "data:image/svg+xml;base64," + base64.b64encode(panel_svg(story["artwork"], page["scene"]).encode()).decode()
            item["width"], item["height"] = 800, 520
        pages.append(item)
    return {"id": story["id"], "title": story["title"], "pages": pages}

