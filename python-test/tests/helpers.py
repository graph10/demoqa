import re
from playwright.sync_api import Locator, expect, Page

def expect_checkbox_result(result_locator: Locator, expected: set[str] | None = None):
    if expected is None:
        expect(result_locator).to_have_text(
            re.compile(r"You have selected :.*", re.DOTALL)
        )
        return

    items = result_locator.locator(".text-success")
    expect(items).to_have_count(len(expected))

    actual = {text.strip() for text in items.all_text_contents()}

    assert actual == expected, (
        f"Expected: {expected}\n"
        f"Actual: {actual}"
    )

def expect_radiobox_result(page_locator: Locator):
    expect(page_locator).to_have_text(
        re.compile(r"You have selected.*", re.DOTALL)
    )


def expand_checkbox_node(page: Page, name: str):
    node = page.locator(
        f'[role="treeitem"]:has([aria-label="Select {name}"])'
    )

    if node.get_attribute("aria-expanded") == "false":
        node.locator(".rc-tree-switcher").click()


def expect_checkbox_state(page: Page, name: str, checked: bool = True):
    checkbox = page.locator(f'[aria-label="Select {name}"]')

    if checked:
        expect(checkbox).to_be_checked()
    else:
        expect(checkbox).not_to_be_checked()
