import pytest
from playwright.sync_api import Playwright


@pytest.fixture
def api_context(playwright: Playwright):
    context = playwright.request.new_context(
        base_url="https://fakestoreapi.com"
    )

    yield context

    context.dispose()