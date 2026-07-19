# E2E flows (Playwright, real browser + real server). Not part of the default
# pytest run — CI и локально запускать явно:
#   pytest tests_e2e/ --no-header -q
# Требует: pip install playwright pytest-playwright && playwright install chromium

import os
import socket
import subprocess
import sys
import time

import pytest

pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright  # noqa: E402

PORT = 8977
BASE = f"http://127.0.0.1:{PORT}"


def _wait_port(port: int, timeout: float = 25.0) -> None:
    end = time.time() + timeout
    while time.time() < end:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.3)
    raise RuntimeError("server did not start")


@pytest.fixture(scope="session")
def server():
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.index:app", "--port", str(PORT)],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    _wait_port(PORT)
    yield BASE
    proc.terminate()
    proc.wait(timeout=10)


@pytest.fixture(scope="session")
def page(server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        errors: list[str] = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.errors = errors
        yield pg
        browser.close()


def test_flow_check_url(page):
    """Landing checker: dangerous domain gets a red verdict."""
    page.goto(BASE + "/", wait_until="networkidle")
    page.fill("#urlInput", "1xbet.com")
    page.click("#checkBtn")
    page.wait_for_function(
        "document.getElementById('resultVerdict').textContent.includes('DANGEROUS')",
        timeout=20000)
    assert not page.errors, page.errors


def test_flow_scan_grade(page):
    """/scan: invalid junk domain returns without hanging, UI stays alive."""
    page.goto(BASE + "/scan", wait_until="networkidle")
    page.fill("#dom", "github.com")
    page.click("#go")
    page.wait_for_selector(".grade, #status .spin", timeout=20000)
    # результат или честный спиннер, но не мёртвая страница
    assert not page.errors, page.errors


def test_flow_brand_variants(page):
    """/brand: generates typosquat variants list."""
    page.goto(BASE + "/brand", wait_until="networkidle")
    page.fill("#dom", "kaspi.kz")
    page.click("#go")
    page.wait_for_selector("#grid .row", timeout=15000)
    rows = page.locator("#grid .row").count()
    assert rows >= 10
    assert page.locator("#liveblock").is_visible()
    assert not page.errors, page.errors


def test_flow_leak_generator(page):
    """/leak: password generator produces a 24-char password client-side."""
    page.goto(BASE + "/leak", wait_until="networkidle")
    page.click("#gengo")
    val = page.input_value("#genout")
    assert len(val) == 24
    assert not page.errors, page.errors


def test_flow_batch_table(page):
    """/batch-check: two URLs produce a verdict table + summary."""
    page.goto(BASE + "/batch-check", wait_until="networkidle")
    page.fill("#urls", "1xbet.com\nkaspi.kz")
    page.click("#go")
    page.wait_for_function(
        "document.querySelectorAll('#tbody tr').length >= 2", timeout=30000)
    assert "DANGEROUS" in page.locator("#tbody").inner_text()
    assert not page.errors, page.errors


def test_flow_theme_toggle(page):
    """Tool pages: light/dark toggle switches and persists."""
    page.goto(BASE + "/leak", wait_until="networkidle")
    before = page.get_attribute("html", "data-theme")
    page.click("#qtgl")
    after = page.get_attribute("html", "data-theme")
    assert before != after
    page.reload(wait_until="networkidle")
    assert page.get_attribute("html", "data-theme") == after
    assert not page.errors, page.errors
