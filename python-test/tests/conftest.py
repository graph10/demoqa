import pytest
import allure
from playwright.sync_api import Page, expect, sync_playwright
import tempfile
import shutil
import os

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page") or item.funcargs.get("elements_page") or item.funcargs.get("alerts_page") or item.funargs.get("widgets_page")
        if page:
            allure.attach(
                page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=0)
        try:
            yield browser
        finally:
            browser.close()

@pytest.fixture
def elements_page(browser):
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto("https://demoqa.com/elements")
        yield page
    finally:
        context.close()

@pytest.fixture
def alerts_page(browser):
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto("https://demoqa.com/alertsWindows")
        yield page
    finally:
        context.close()

@pytest.fixture
def widgets_page(browser):
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto("https://demoqa.com/widgets")
        yield page
    finally:
        context.close()

@pytest.fixture
def download_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)