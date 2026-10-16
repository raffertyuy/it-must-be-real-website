"""Real browser/Streamlit tests, including animation, URL state and mobile controls."""
import os
import re
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "test-artifacts"
BASE_URL = "http://127.0.0.1:8501"
STORY_URL = BASE_URL + "/short_stories?story=rafal-robotic-pinky&page=1"


def wait_for_server(process):
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Streamlit exited")
        try:
            with urllib.request.urlopen(BASE_URL + "/_stcore/health", timeout=2) as r:
                if r.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(.3)
    raise RuntimeError("Server did not become ready")


def ready(page, number):
    expect(page.locator(".reader .book-spread")).to_have_count(1, timeout=30000)
    expect(page.locator(".turn-leaf")).to_have_count(0, timeout=10000)
    expect(page.locator(".reader .book-eyebrow")).to_have_text(f"PAGE {number:02} / 08")
    expect(page.locator('[data-testid="stException"]')).to_have_count(0)
    image = page.locator(".reader .book-art img")
    expect(image).to_have_count(1)
    page.wait_for_function("img => img.complete && img.naturalWidth > 0", arg=image.element_handle())


def main():
    ARTIFACTS.mkdir(exist_ok=True)
    with (ARTIFACTS / "streamlit.log").open("w") as log:
        server = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.headless=true", "--server.port=8501", "--browser.gatherUsageStats=false"], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        try:
            wait_for_server(server)
            with sync_playwright() as pw:
                kwargs = {"executable_path": os.environ["CHROMIUM_PATH"]} if os.getenv("CHROMIUM_PATH") else {}
                browser = pw.chromium.launch(**kwargs)
                page = browser.new_page(viewport={"width":1440,"height":1100})
                errors=[]
                page.on("pageerror", lambda error: errors.append(str(error)))
                try:
                    page.goto(STORY_URL)
                    ready(page,1)
                    expect(page.locator(".sidebar-header")).to_have_count(1)
                    expect(page.get_by_role("button",name="Previous page",exact=True)).to_be_disabled()
                    page.get_by_role("button",name="Next page",exact=True).click()
                    expect(page.locator(".turn-leaf")).to_have_count(1)
                    # Inspect the running rotation rather than racing the first compositor frame.
                    assert page.locator(".turn-leaf").evaluate("e=>e.getAnimations().some(a=>a.effect.getTiming().duration>0 && a.effect.getKeyframes().some(f=>String(f.transform).includes('rotateY')))")
                    ready(page,2)
                    expect(page).to_have_url(re.compile(r"page=2"))
                    page.screenshot(path=str(ARTIFACTS/"reader-desktop.png"),full_page=True)
                    page.get_by_role("button",name="Previous page",exact=True).click();ready(page,1)
                    page.get_by_label("Go to page",exact=True).select_option("6");ready(page,6)
                    expect(page).to_have_url(re.compile(r"page=6"))
                    page.reload();ready(page,6)
                    page.get_by_role("button",name="Read all pages",exact=True).click()
                    expect(page.locator(".reader .book-spread")).to_have_count(8)
                    page.get_by_role("button",name="Read all pages",exact=True).click();ready(page,6)
                    page.locator(".reader").focus();page.keyboard.press("End");ready(page,8)
                    expect(page.get_by_role("button",name="Next page",exact=True)).to_be_disabled()
                    page.keyboard.press("Home");ready(page,1)
                    print("PASS desktop: real rotation, previous/next, jump, read-all, keyboard, boundaries and refreshable URL")

                    mobile = browser.new_page(viewport={"width":393,"height":900},is_mobile=True,has_touch=True)
                    mobile.goto(STORY_URL.replace("page=1","page=4"));ready(mobile,4)
                    assert mobile.evaluate("document.documentElement.scrollWidth<=innerWidth")
                    art=mobile.locator(".reader .book-art").bounding_box();copy=mobile.locator(".reader .book-copy").bounding_box()
                    assert copy["y"]>=art["y"]+art["height"]-2,"Mobile text must stack below portrait"
                    mobile.screenshot(path=str(ARTIFACTS/"reader-mobile.png"),full_page=True)
                    mobile.get_by_role("button",name="Next page",exact=True).click();ready(mobile,5)
                    expect(mobile).to_have_url(re.compile(r"page=5"))
                    mobile.emulate_media(reduced_motion="reduce")
                    mobile.get_by_role("button",name="Next page",exact=True).click();ready(mobile,6)
                    assert mobile.locator(".reader").evaluate("e=>e.getAnimations({subtree:true}).length") == 0
                    mobile.get_by_role("button",name="← All short stories",exact=True).click()
                    expect(mobile.locator(".story-cover")).to_have_count(1)
                    expect(mobile.locator(".reader")).to_have_count(0)
                    mobile.screenshot(path=str(ARTIFACTS/"bookshelf-mobile.png"),full_page=True)
                    print("PASS mobile: portrait stacking, no overflow, URL sync, reduced motion and shelf navigation")
                    assert not errors, errors
                except Exception:
                    (ARTIFACTS/"failure.txt").write_text(traceback.format_exc())
                    page.screenshot(path=str(ARTIFACTS/"failure.png"),full_page=True)
                    raise
                finally:
                    browser.close()
        finally:
            server.terminate()
            try: server.wait(timeout=10)
            except subprocess.TimeoutExpired: server.kill();server.wait(timeout=5)


if __name__ == "__main__":
    main()
