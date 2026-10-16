# Illustrated short stories

## Reader

The existing Streamlit app registers **Short Stories** at `/short-stories`, with a home-page entry point. The bookshelf currently contains *Rafal and the Robotic Pinky*, an eight-page story plus a cover. Readers can turn pages, jump to a page, read everything vertically, restart, or download a Markdown transcript.

Bookmarks use `/short-stories?story=rafal-robotic-pinky&page=4`. Page values are clamped to the valid range, and unknown story IDs return the bookshelf with a notice. Only catalogue IDs are accepted; query strings never become filesystem paths. Native Streamlit controls remain keyboard-accessible. Story text is HTML text, not pixels inside an illustration. Images have descriptive alt text. Book CSS is scoped so the existing category image sizes remain unchanged.

## Artwork decision and character bible

Image generation was unavailable during implementation. These are original, code-authored SVG comic illustrations, **not AI-generated paintings**. There are no external image services, API keys, fonts, or paid dependencies. The artwork uses a single nine-panel master at `images/short_stories/rafal_robotic_pinky.svg`. The cover and eight panels share the same SVG character definitions. `stories/render.py` selects each panel at its native vector resolution instead of cropping a low-resolution raster sheet.

- **Rafal:** twelve-year-old Chinese boy; warm light skin, short side-swept black hair, teal T-shirt with a gold pixel bolt, navy trousers, cream shoes.
- **Kyan:** Nepali friend of the same age; warm brown skin, short textured black hair, orange hoodie, blue trousers, cream shoes. He never wears a splint.
- **Dad:** short dark hair, glasses, blue polo and navy trousers.
- **Splint:** a small silver plate with exactly two pale-blue straps on Rafal's **right pinky only**, not his index finger, thumb, entire hand, or left hand. For the front-facing character, the anatomical right hand is on the viewer's left. Never mirror the actor. The pinky is the outermost, shortest digit; the thumb faces inward.
- **Timeline:** cover is a promotional scene after fitting; page 1 has no splint; pages 2–7 use the same fitted splint; page 8 shows a bare right hand after medical clearance, with the retired splint displayed separately.
- **Imaginary effects:** the floating game worlds are Dad and the boys' pretend adventures. No electronics are added to the physical splint. Healing is never attributed to AI. Rafal directs Kyan while recovering and returns to playing only after clearance.

The exact same source definitions are reused rather than redrawing approximate lookalikes. Unit tests check reference integrity, no negative-scale mirroring, the two straps, and the before/after timeline. The complete master is a convenient consistency contact sheet. Future painted art can replace it, but should preserve this bible and the story's text/alt separation.

## Add a story

1. Add a UTF-8 JSON file to `stories/`, following `rafal_robotic_pinky.json`: unique `id`, title, subtitle, description, tags, artwork, cover alt text, note, and an ordered list of pages. Each page has a scene ID, title, paragraphs, caption, and alt text.
2. Add its SVG master under `images/short_stories/`. Include a `cover` symbol and one symbol per page, with `viewBox="0 0 800 520"`. Put shared character definitions in `defs` and reference them with `use`. The bookshelf discovers the JSON automatically; no new route is necessary.
3. Run `python -m unittest discover -s tests -v` from the repository root. Streamlit is required for the integration tests; without it those tests explicitly skip. GitHub Actions installs the existing requirements and runs both suites.
4. Run `streamlit run streamlit_app.py`. Check the home link, sidebar, previous/next boundaries, page picker, read-all toggle, restart, download, malformed bookmarks, and mobile layout. Visually check all illustrations for story continuity.

No new runtime packages are required. `functools.lru_cache` caches local content and rendered SVG; content changes take effect after an app process restart. The reader uses only trusted repository-owned content, HTML-escapes prose and attributes, and does not fetch user-provided image URLs.
