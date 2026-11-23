from playwright.sync_api import Page, expect, Dialog
import pytest
import allure


@allure.feature("Alerts")
@allure.story("Alerts")
@allure.title("Проверка обычного и отложенного Alert")
@allure.severity(allure.severity_level.CRITICAL)
def test_alerts_dialogs(alerts_page: Page):
    alerts_page.clock.install()
    alerts_page.get_by_role("link", name="Alerts").click()
    expect(alerts_page).to_have_url("https://demoqa.com/alerts")

    alerts_page.once("dialog", lambda d: d.accept())
    alerts_page.get_by_role("button").nth(0).click()

    def handle_dialog(dialog: Dialog):
        assert dialog.type == "alert"
        assert dialog.message == "This alert appeared after 5 seconds"
        dialog.accept()

    alerts_page.once("dialog", handle_dialog)
    alerts_page.get_by_role("button").nth(1).click()
    alerts_page.clock.fast_forward(5000)


@allure.feature("Alerts")
@allure.story("Confirm Dialog")
@allure.title("Проверка Confirm Dialog: {action}")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("action", [
    pytest.param("accept", id="accept"),
    pytest.param("dismiss", id="dismiss")
])
def test_confirm(alerts_page: Page, action):
    alerts_page.get_by_role("link", name="Alerts").click()
    expect(alerts_page).to_have_url("https://demoqa.com/alerts")
    def handle_confirm(dialog: Dialog):
            assert dialog.type == "confirm"
            if action == "accept":
                dialog.accept()
                expect(alerts_page.locator("#confirmResult")).to_have_text("You selected Ok")
            else:
                dialog.dismiss()
                expect(alerts_page.locator("#confirmResult")).to_have_text("You selected Cancel")
    alerts_page.once("dialog", handle_confirm)
    alerts_page.get_by_role("button").nth(2).click()


@allure.feature("Alerts")
@allure.story("Prompt Dialog")
@allure.title("Проверка Prompt Dialog: {action}, {input}")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("input", [
    pytest.param("Roman", id="input-Roman"),
    pytest.param("Kulikov", id="input-Kulikov"),
    pytest.param("QA", id="QA"),
    pytest.param("", id="nothing")
])
@pytest.mark.parametrize("action", [
    pytest.param("accept", id="accept"),
    pytest.param("dismiss", id="dismiss")
])
def test_prompt(alerts_page: Page, input, action):
    alerts_page.get_by_role("link", name="Alerts").click()
    expect(alerts_page).to_have_url("https://demoqa.com/alerts")
    def handle_prompt(dialog: Dialog):
            assert dialog.type == "prompt"
            if action == "accept":
                dialog.accept(input)
            else:
                dialog.dismiss()
    alerts_page.once("dialog", handle_prompt)
    alerts_page.get_by_role("button").nth(3).click()

    if action == "accept" and input != "":
        expect(alerts_page.locator("#promptResult")).to_be_visible()
        expect(alerts_page.locator("#promptResult")).to_contain_text(input)
    else:
        expect(alerts_page.locator("#promptResult")).to_be_hidden()


@allure.feature("Alerts")
@allure.story("Frames")
@allure.title("Проверка содержимого обычных фреймов")
@allure.severity(allure.severity_level.NORMAL)
def test_frames(alerts_page: Page):
    alerts_page.get_by_role("link", name="Frames", exact=True).click()
    expect(alerts_page).to_have_url("https://demoqa.com/frames")

    big_frame = alerts_page.frame_locator("#frame1")
    expect(big_frame.locator("#sampleHeading")).to_have_text("This is a sample page")

    small_frame = alerts_page.frame_locator("#frame2")
    expect(small_frame.locator("#sampleHeading")).to_have_text("This is a sample page")


@allure.feature("Alerts")
@allure.story("Nested Frames")
@allure.title("Проверка вложенных фреймов")
@allure.severity(allure.severity_level.NORMAL)
def test_nested_frames(alerts_page: Page):
    alerts_page.get_by_role("link", name="Nested Frames", exact=True).click()
    expect(alerts_page).to_have_url("https://demoqa.com/nestedframes")

    outer_frame = alerts_page.frame_locator("#frame1")
    expect(outer_frame.locator("body")).to_contain_text("Parent frame")
    inner_frame = outer_frame.frame_locator("iframe")
    expect(inner_frame.locator("body")).to_have_text("Child Iframe")


@allure.feature("Alerts")
@allure.story("Modal Dialogs")
@allure.title("Проверка закрытия модального окна: {modal_size}, {close_type}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("modal_size, close_type", [
    ("Small modal", "button"),
    ("Small modal", "cross"),
    ("Large modal", "button"),
    ("Large modal", "cross"),
])
def test_modal_closing(alerts_page: Page, modal_size, close_type):
    alerts_page.get_by_role("link", name="Modal Dialogs", exact=True).click()
    alerts_page.get_by_role("button", name=modal_size).click()
    modal = alerts_page.get_by_role("dialog")
    expect(modal).to_be_visible()

    if close_type == "button":
        if modal_size == "Small modal":
            modal.locator("#closeSmallModal").click()
        else:
            modal.locator("#closeLargeModal").click()
    else:
        modal.get_by_label("Close").click()
    expect(modal).to_be_hidden()


@allure.feature("Alerts")
@allure.story("Modal Dialogs")
@allure.title("Проверка расположения кнопки закрытия Small Modal")
@allure.severity(allure.severity_level.MINOR)
def test_cross_position_small_modal(alerts_page: Page):
    alerts_page.get_by_role("link", name="Modal Dialogs", exact=True).click()
    alerts_page.get_by_role("button", name="Small modal").click()
    modal = alerts_page.get_by_role("dialog")
    cross = modal.get_by_label("Close")
    expect(modal).to_be_visible()
    expect(cross).to_be_visible()
    modal_box = modal.bounding_box()
    cross_box = cross.bounding_box()
    assert modal_box is not None
    assert cross_box is not None
    assert cross_box["x"] > modal_box["x"] + (modal_box["width"] / 2)
    assert cross_box["y"] < modal_box["y"] + (modal_box["height"] / 2)


@allure.feature("Alerts")
@allure.story("Modal Dialogs")
@allure.title("Проверка расположения кнопки закрытия Large Modal")
@allure.severity(allure.severity_level.MINOR)
def test_cross_position_large_modal(alerts_page: Page):
    alerts_page.get_by_role("link", name="Modal Dialogs", exact=True).click()
    alerts_page.get_by_role("button", name="Large modal").click()
    modal = alerts_page.get_by_role("dialog")
    cross = modal.get_by_label("Close")
    expect(modal).to_be_visible()
    expect(cross).to_be_visible()
    modal_box = modal.bounding_box()
    cross_box = cross.bounding_box()
    assert modal_box is not None
    assert cross_box is not None
    assert cross_box["x"] > modal_box["x"] + (modal_box["width"] / 2)
    assert cross_box["y"] < modal_box["y"] + (modal_box["height"] / 2)