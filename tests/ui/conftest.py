import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import os
from datetime import datetime

import pytest
from playwright.sync_api import sync_playwright

from src.pages.login_page import LoginPage
from src.config.settings import UI_USERNAME, UI_PASSWORD, BROWSER, HEADLESS, TIMEOUT_MS

ARTIFACTS_DIR = "artifacts"
SCREENSHOTS_DIR = os.path.join(ARTIFACTS_DIR, "screenshots")
TRACES_DIR = os.path.join(ARTIFACTS_DIR, "traces")
VIDEOS_DIR = os.path.join(ARTIFACTS_DIR, "videos")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser_type = getattr(p, BROWSER)  # chromium / firefox / webkit
        browser = browser_type.launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser, request):
    _ensure_artifacts_dir()
    context = browser.new_context(
        record_video_dir=VIDEOS_DIR
    )
    context.set_default_timeout(TIMEOUT_MS)

    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    yield page

    failed = getattr(request.node, "failed", False)

    if failed:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_path = os.path.join(TRACES_DIR, f"{request.node.name}_{BROWSER}_{ts}_trace.zip")
        context.tracing.stop(path=trace_path)
    else:
        context.tracing.stop()

    video = page.video
    context.close()

    if video:
        video_path = video.path()
        if not failed and os.path.exists(video_path):
            os.remove(video_path)


@pytest.fixture(scope="function")
def dashboard_page(page):
    login_page = LoginPage(page)
    login_page.open()
    return login_page.login_success(UI_USERNAME, UI_PASSWORD)


def _ensure_artifacts_dir():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(TRACES_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    yield
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        _ensure_artifacts_dir()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(SCREENSHOTS_DIR, f"{request.node.name}_{BROWSER}_{ts}.png")
        page.screenshot(path=path, full_page=True)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    if rep.when == "call":
        setattr(item, "failed", rep.failed)