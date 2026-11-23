from playwright.sync_api import Page, expect
import pytest
import allure
from helpers import expect_checkbox_result, expect_radiobox_result, expand_checkbox_node, expect_checkbox_state
import os


@allure.feature("Elements")
@allure.story("Text Box")
@allure.title("Заполнение и отправка Text Box")
@allure.severity(allure.severity_level.NORMAL)
def test_text_box(elements_page: Page):
    elements_page.get_by_role("link", name="Text Box").click()
    expect(elements_page).to_have_url("https://demoqa.com/text-box")

    elements_page.get_by_placeholder("Full Name").press_sequentially("Roman Kulikov", delay=150)
    elements_page.get_by_placeholder("name@example.com").fill("kulikov@mail.ru")
    elements_page.locator("#currentAddress").fill("Moscow")
    elements_page.locator("textarea#permanentAddress").fill("Crimea") 

    button = elements_page.get_by_role("button", name="Submit")
    button.hover()
    button.click()


@allure.feature("Elements")
@allure.story("Check Box")
@allure.title("Проверка выбора чекбоксов и вложенных элементов")
@allure.severity(allure.severity_level.CRITICAL)
def test_check_box(elements_page: Page):
    elements_page.get_by_role("link", name="Check Box").click()
    expect(elements_page).to_have_url("https://demoqa.com/checkbox")

    result = elements_page.locator("#result")

    expand_checkbox_node(elements_page, "Home")

    home = elements_page.locator('[aria-label="Select Home"]')
    desktop = elements_page.locator('[aria-label="Select Desktop"]')
    documents = elements_page.locator('[aria-label="Select Documents"]')
    downloads = elements_page.locator('[aria-label="Select Downloads"]')
    notes = elements_page.locator('[aria-label="Select Notes"]')
    commands = elements_page.locator('[aria-label="Select Commands"]')

    expect(desktop).to_be_visible()
    expect(documents).to_be_visible()
    expect(downloads).to_be_visible()

    expand_checkbox_node(elements_page, "Desktop")

    expect(notes).to_be_visible()
    expect(commands).to_be_visible()

    desktop.check()

    expect_checkbox_state(elements_page, "Desktop")
    expect_checkbox_state(elements_page, "Notes")
    expect_checkbox_state(elements_page, "Commands")
    expect_checkbox_result(result, {"desktop", "notes", "commands"})

    desktop.uncheck()

    for name in ["Desktop", "Notes", "Commands"]:
        expect_checkbox_state(elements_page, name, False)

    notes.check()
    commands.check()

    expect_checkbox_state(elements_page, "Notes")
    expect_checkbox_state(elements_page, "Commands")
    expect_checkbox_state(elements_page, "Desktop")

    expect_checkbox_result(result, {"desktop", "notes", "commands"})

    expand_checkbox_node(elements_page, "Documents")

    workspace = elements_page.locator('[aria-label="Select WorkSpace"]')
    office = elements_page.locator('[aria-label="Select Office"]')

    expect(workspace).to_be_visible()
    expect(office).to_be_visible()

    documents.check()

    expected_documents = {
        "desktop", "notes", "commands",
        "documents",
        "workspace", "react", "angular", "veu",
        "office", "public", "private", "classified", "general",
    }

    expect_checkbox_state(elements_page, "Documents")
    expect_checkbox_state(elements_page, "WorkSpace")
    expect_checkbox_state(elements_page, "Office")
    expect_checkbox_result(result, expected_documents)

    documents.uncheck()

    expect_checkbox_state(elements_page, "Documents", False)

    expand_checkbox_node(elements_page, "Documents")
    expand_checkbox_node(elements_page, "WorkSpace")
    expand_checkbox_node(elements_page, "Office")

    for name in [
        "WorkSpace", "React", "Angular", "Veu",
        "Office", "Public", "Private", "Classified", "General",
    ]:
        expect_checkbox_state(elements_page, name, False)

    home.check()

    expected_all = {
        "home",
        "desktop", "notes", "commands",
        "documents", "workspace", "react", "angular", "veu",
        "office", "public", "private", "classified", "general",
        "downloads", "wordFile", "excelFile",
    }

    expect_checkbox_state(elements_page, "Home")
    expect_checkbox_result(result, expected_all)

    home.uncheck()

    expand_checkbox_node(elements_page, "Downloads")

    for name in [
        "Home", "Desktop", "Notes", "Commands",
        "Documents", "WorkSpace", "React", "Angular", "Veu",
        "Office", "Public", "Private", "Classified", "General",
        "Downloads", "Word File.doc", "Excel File.doc",
    ]:
        expect_checkbox_state(elements_page, name, False)


@allure.feature("Elements")
@allure.story("Radio Button")
@allure.title("Проверка выбора Radio Button")
@allure.severity(allure.severity_level.NORMAL)
def test_radio_box(elements_page: Page):
    elements_page.get_by_role("link", name="Radio Button").click()
    expect(elements_page).to_have_url("https://demoqa.com/radio-button")

    elements_page.get_by_role("radio", name="Yes").click()
    expect_radiobox_result(elements_page.locator("p"))
    elements_page.get_by_role("radio", name="Impressive").click()
    expect_radiobox_result(elements_page.locator("p"))


@allure.feature("Elements")
@allure.story("Buttons")
@allure.title("Проверка одинарного, двойного и правого клика")
@allure.severity(allure.severity_level.NORMAL)
def test_buttons(elements_page: Page):
    elements_page.get_by_role("link", name="Buttons").click()
    expect(elements_page).to_have_url("https://demoqa.com/buttons")

    elements_page.get_by_role("button", name="Double Click Me").dblclick()
    elements_page.get_by_role("button", name="Right Click Me").click(button="right")
    elements_page.get_by_role("button", name="Click Me", exact=True).click()
    expect(elements_page.locator("p")).to_have_count(3)


@allure.feature("Elements")
@allure.story("Links")
@allure.title("Проверка ссылки: {locator_value}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("locator_type, locator_value, expected_value, is_navigation", [
    pytest.param("role", "Home", "https://demoqa.com/", True, id="home_static"),
    pytest.param("css", "#dynamicLink", "https://demoqa.com/", True, id="home_random"),
    pytest.param("role", "Created", "201", False, id="created"),
    pytest.param("role", "No Content", "204", False, id="no_content"),
    pytest.param("role", "Moved", "301", False, id="moved"),
    pytest.param("role", "Bad Request", "400", False, id="bad_request"),
    pytest.param("role", "Unauthorized", "401", False, id="unauthorized"),
    pytest.param("role", "Forbidden", "403", False, id="forbidden"),
    pytest.param("role", "Not Found", "404", False, id="not_found")
])
def test_links(elements_page: Page, locator_type, locator_value, expected_value, is_navigation):
    elements_page.get_by_role("link", name="Links", exact=True).click()
    expect(elements_page).to_have_url("https://demoqa.com/links")

    if locator_type == "role":
        link = elements_page.get_by_role("link", name=locator_value, exact=True)
    else:
        link = elements_page.locator(locator_value)

    if is_navigation:
        with elements_page.context.expect_page() as new_page_info:
            link.click()
        
        new_page = new_page_info.value
        new_page.wait_for_load_state()
        expect(new_page).to_have_url(expected_value)
        new_page.close()
    else:
        link.click()
        response = elements_page.locator("#linkResponse")
        expect(response).to_contain_text(expected_value)



@allure.feature("Elements")
@allure.story("Broken Links - Images")
@allure.title("Проверка загрузки изображений")
@allure.severity(allure.severity_level.NORMAL)
def test_valid_and_broken_images(elements_page: Page):
    elements_page.get_by_role("link", name="Broken Links - Images").click()
    expect(elements_page).to_have_url("https://demoqa.com/broken")

    images = elements_page.locator("img")
    expect(images).to_have_count(3)

    expect(images.nth(0)).to_have_js_property("naturalWidth", 347)
    expect(images.nth(1)).to_have_js_property("naturalWidth", 0)


@allure.feature("Elements")
@allure.story("Broken Links - Images")
@allure.title("Проверка рабочих и сломанных ссылок")
@allure.severity(allure.severity_level.NORMAL)
def test_valid_and_broken_links(elements_page: Page):
    elements_page.get_by_role("link", name="Broken Links - Images").click()
    expect(elements_page).to_have_url("https://demoqa.com/broken")

    valid_link = elements_page.get_by_role("link", name="Click Here for Valid Link")
    broken_link = elements_page.get_by_role("link", name="Click Here for Broken Link")

    expect(valid_link).to_have_attribute("href", "http://demoqa.com")

    expect(broken_link).to_have_attribute("href", "http://the-internet.herokuapp.com/status_codes/500")


@allure.feature("Elements")
@allure.story("Upload and Download")
@allure.title("Скачивание и загрузка файла")
@allure.severity(allure.severity_level.NORMAL)
def test_upload_download_file(elements_page: Page, download_dir):
    elements_page.get_by_role("link", name="Upload and Download").click()
    expect(elements_page).to_have_url("https://demoqa.com/upload-download")

    with elements_page.expect_download() as download_info:
        elements_page.get_by_role("button", name="Download").click()
    download = download_info.value
    file_path = os.path.join(download_dir, download.suggested_filename)
    download.save_as(file_path)

    elements_page.locator("#uploadFile").set_input_files(file_path)
    elements_page.locator("#uploadFile").set_input_files([])


@allure.feature("Elements")
@allure.story("Dynamic Properties")
@allure.title("Проверка динамических свойств элементов")
@allure.severity(allure.severity_level.NORMAL)
def test_dynamic(elements_page: Page):
    elements_page.get_by_role("link", name="Dynamic Properties").click()
    expect(elements_page).to_have_url("https://demoqa.com/dynamic-properties")

    expect(elements_page.get_by_role("button", name="Will Enable 5 Seconds")).to_be_enabled()
    expect(elements_page.get_by_role("button", name="Color Change")).to_be_visible()
    expect(elements_page.get_by_role("button", name="Visible After 5 Seconds")).to_be_visible()


