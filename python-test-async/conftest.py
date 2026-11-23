import pytest
import pytest_asyncio
import allure

from playwright.async_api import Page, expect, async_playwright


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest_asyncio.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            slow_mo=0
        )
        try:
            yield browser
        finally:
            await browser.close()


@pytest_asyncio.fixture
async def practice_form_page(browser, request):
    context = await browser.new_context()
    page = await context.new_page()

    try:
        await page.goto("https://demoqa.com/automation-practice-form")
        yield page

    finally:
        rep = getattr(request.node, "rep_call", None)

        if rep and rep.failed:
            allure.attach(
                await page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )

        await context.close()