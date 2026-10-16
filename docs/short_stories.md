# Short-story authoring and reader

## Editing the story

The published title is **The AI-Powered Robotic Finger**. Keep the existing
`rafal-robotic-pinky` story ID and filenames so shared bookmarks continue to work.

The only narrative source of truth is `stories/rafal_robotic_pinky.json`. Titles,
paragraphs, punchlines and accessible image descriptions are ordinary strings.
Edit these without regenerating artwork or changing reader code. Never bake the
right-hand story page into an image. The browser renders each paragraph using
`textContent`, not unsafe interpolated HTML. The downloadable Markdown transcript
and plain reading view use the same data.

The current story keeps the family details straight: Mom handles the hospital
trip and follow-up; Dad invents PINK-E 9000 and loses to Rafal at both Minecraft
Bed Wars and Tetris; Kyan is the skeptical witness. Age and ethnicity are not
narrated. The final exchange remains “So the AI wasn’t real?” / “Of course it
was. It’s on the website.”

## Website flow

Home → Short Stories bookshelf → Open the book → eight illustrated spreads.
The sidebar retains all existing categories. `← All short stories` returns to
the shelf. A direct bookmark looks like
`/short_stories?story=rafal-robotic-pinky&page=4`.

Desktop: a 2:3 portrait illustration on the left, editable HTML prose on the
right. Mobile: portrait above prose, without an inner scrolling text box.
Previous/Next, page selection, focused arrow keys, Home/End and horizontal
swipes on the artwork navigate. Page turns use a two-sided CSS 3D leaf around
the book spine. Page completion reports its bookmark through Streamlit's v2
component API; late acknowledgements cannot rewind a later local turn.

A Read all pages toggle and native plain-text expander provide alternatives.
The animation checkbox and `prefers-reduced-motion` disable movement. The reader
uses semantic controls, live page announcements, image alt text and visible
keyboard focus. It does not hijack arrow keys outside the book or within selects.

## Files and dependencies

- `stories/library.py`: trusted JSON catalogue and bounded local asset paths.
- `stories/render.py`: image data URIs, shelf rendering and reader payload.
- `stories/book.py`: Streamlit v2 registration, state and URL bridge.
- `stories/frontend/book.js` and `book.css`: isolated production component.
- `images/short_stories/rafal/*.webp`: optimized portrait artwork.
- `scripts/preview_story.py`: exports the same component for offline review.

Streamlit is pinned to 1.66.0, the tested version. There is no flipbook package,
CDN script, image API call or runtime image-generation key. The old SVG renderer
remains available for backwards compatibility with vector-based stories.

## Artwork and continuity

These are portrait crops of the previously generated cyber-style illustrations,
plus a generated hospital illustration with Mom. The right-side text panels are
not used. The cover art is intentionally reused for the PINK-E introduction.
The Tetris page uses a puzzle close-up, and the investigation page spotlights
Kyan. Those crops avoid the incorrect index-finger/wrist placement and ambiguous
hand poses in some rejected earlier mockups. They are not nine newly generated,
independent scenes and not a regenerated single master.

Page two uses a refreshed hospital portrait: Mom has long black hair with
blue-green underlayers. The generated prose and reader mockup were cropped away;
the background diagnostic display is defocused so generated labels are not
presented as an accurate X-ray. All story paragraphs remain unchanged.

Rafal wears rectangular glasses; Kyan does not. Rafal's device belongs on his
anatomical right little finger, opposite the thumb. A palm-facing-viewer right
hand has its thumb on the viewer's right and pinky on the viewer's left; a
back-of-hand view reverses that screen orientation. Check the whole arm and
hand, not just a left/right pixel coordinate. The hospital scene shows a plain
medical splint; neon glow in gaming scenes belongs to the joke. After clearance,
the final portrait shows a bare right hand.

Incidental environmental lettering is part of the art, not the narrative source.
Do not promise that tests verify a drawing's anatomy. Visually review each image
and its correspondence to the prose. `docs/rafal_art_brief.md` is the target brief
for future full-scene expansion, not a claim that every current crop shows all
characters described in that brief.

## Adding another book

Add one JSON file in `stories/` with a unique lowercase hyphenated `id`, `title`,
`subtitle`, `description`, `cover_image`, `cover_alt`, `note` and a `pages` array.
Each page has `scene`, `title`, `paragraphs` (a list of strings), `caption`, `alt`
and `image`, relative to `images/short_stories/`. Keep portrait art at 2:3 and
roughly 80–120 words per spread. The catalogue discovers it automatically.

## Checks

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/preview_story.py --output story_preview.html
# Browser-only developer dependency:
python -m pip install playwright
python -m playwright install chromium
python tests/browser_smoke.py
```

GitHub Actions runs the content and backend checks plus a real Chromium/Streamlit
integration test, and retains browser screenshots on success or failure.
