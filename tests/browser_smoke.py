"""Browser checks against a real local Streamlit server (CI-only dependency)."""
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "test-artifacts"
BASE_URL = "http://127.0.0.1:8501"
STORY_URL = BASE_URL + "/short-stories?story=rafal-robotic-pinky&page=1"


def wait_for_server(process):
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Streamlit exited before becoming ready")
        try:
            with urllib.request.urlopen(BASE_URL + "/_stcore/health", timeout=2) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.3)
    raise RuntimeError("Streamlit did not become ready")


def ready(page, count):
    expect(page.locator(".story-spread")).to_have_count(count, timeout=30000)
    expect(page.locator('[data-testid="stException"]')).to_have_count(0)
    # Scroll each panel into view: read-all intentionally lazy-loads illustrations.
    for image in page.locator(".story-art img").all():
        image.scroll_into_view_if_needed()
        page.wait_for_function("img => img.complete && img.naturalWidth > 0",
                               arg=image.element_handle(), timeout=30000)


def main():
    ARTIFACTS.mkdir(exist_ok=True)
    with (ARTIFACTS / "streamlit.log").open("w", encoding="utf-8") as log:
        server = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
             "--server.headless=true", "--server.port=8501", "--browser.gatherUsageStats=false"],
            cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        try:
            wait_for_server(server)
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                page = browser.new_page(viewport={"width": 1440, "height": 1100})
                try:
                    page.goto(STORY_URL)
                    ready(page, 1)
                    expect(page.get_by_role("button", name="← Previous", exact=True)).to_be_disabled()
                    page.get_by_role("button", name="Next →", exact=True).click()
                    expect(page.locator(".story-eyebrow")).to_have_text("PAGE 02 / 08")
                    page.get_by_role("button", name="← Previous", exact=True).click()
                    expect(page.locator(".story-eyebrow")).to_have_text("PAGE 01 / 08")
                    page.screenshot(path=str(ARTIFACTS / "reader-desktop.png"), full_page=True)
                    page.get_by_label("Read all pages", exact=True).check()
                    ready(page, 8)
                    print("PASS: desktop reader, SVG images, next/previous and read-all")

                    mobile = browser.new_page(viewport={"width": 393, "height": 900}, is_mobile=True)
                    mobile.goto(STORY_URL)
                    ready(mobile, 1)
                    assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "Mobile horizontal overflow"
                    mobile.locator(".story-spread").screenshot(path=str(ARTIFACTS / "reader-mobile.png"))
                    mobile.get_by_role("button", name="← All short stories", exact=True).click()
                    expect(mobile.locator(".story-cover")).to_have_count(1)
                    mobile.wait_for_function("document.querySelector('.story-cover img')?.naturalWidth > 0")
                    mobile.locator(".story-cover").screenshot(path=str(ARTIFACTS / "bookshelf-mobile.png"))
                    print("PASS: mobile layout, bookshelf, cover artwork and return navigation")
                except Exception:
                    page.screenshot(path=str(ARTIFACTS / "failure.png"), full_page=True)
                    raise
                finally:
                    browser.close()
        finally:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)


if __name__ == "__main__":
    main()
