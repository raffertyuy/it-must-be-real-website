"""Export the production reader as a standalone HTML preview (no server needed)."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from stories.library import load_stories
from stories.render import book_payload


def preview(story):
    css = (ROOT / "stories/frontend/book.css").read_text(encoding="utf-8")
    js = (ROOT / "stories/frontend/book.js").read_text(encoding="utf-8").replace("export default function renderBook", "function renderBook", 1)
    payload = {"story": book_payload(story), "page": 1, "sequence": 0,
               "revision": hashlib.sha256(json.dumps(story).encode()).hexdigest()}
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    title = story["title"].replace("&", "&amp;").replace("<", "&lt;")
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><style>body{{margin:0;background:#0e1117;color:#eef4fc;font-family:system-ui}}'
            'main{max-width:1200px;margin:auto;padding:24px 18px 50px}h1{font-size:24px;margin:8px 0}header p{color:#9fb1c6;font-size:13px}'
            f'{css}</style></head><body><main><header><p>IT MUST BE REAL / SHORT STORIES</p><h1>{title}</h1>'
            '<p>Interactive preview · Story text is selectable and editable separately from the illustrations.</p></header><div id="book"></div></main>'
            f'<script>{js}\nconst payload={data};const bridge={{parentElement:document.getElementById("book"),data:payload,'
            'setStateValue:(key,value)=>{payload.page=value.page;payload.sequence=value.sequence;renderBook(bridge);}};renderBook(bridge);</script></body></html>')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("story_preview.html"))
    parser.add_argument("--story", default="rafal-robotic-pinky")
    args = parser.parse_args()
    args.output.write_text(preview(load_stories()[args.story]), encoding="utf-8")
    print(args.output)
