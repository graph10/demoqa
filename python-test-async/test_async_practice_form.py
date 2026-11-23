import pytest
import allure

from playwright.async_api import Page, expect


@allure.feature("Practice Form")
@allure.story("Form Elements")
@allure.title("Проверка элементов формы")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.asyncio
async def test_practice_form_elements(practice_form_page: Page, tmp_path):
    page = practice_form_page

    await page.locator("#firstName").fill("Roman")
    await page.locator("#lastName").fill("Kulikov")
    await page.locator("#userEmail").fill("roman@example.com")
    await page.locator("#userNumber").fill("1234567890")

    await expect(page.locator("#firstName")).to_have_value("Roman")
    await expect(page.locator("#lastName")).to_have_value("Kulikov")
    await expect(page.locator("#userEmail")).to_have_value("roman@example.com")

    await page.locator("label[for='gender-radio-1']").click()
    assert await page.locator("#gender-radio-1").is_checked()

    await page.locator("label[for='hobbies-checkbox-1']").click()
    await page.locator("label[for='hobbies-checkbox-2']").click()

    assert await page.locator("#hobbies-checkbox-1").is_checked()
    assert await page.locator("#hobbies-checkbox-2").is_checked()

    await page.locator("#dateOfBirthInput").fill("15 Aug 1995")

    await expect(page.locator("#dateOfBirthInput")).to_have_value("15 Aug 1995")

    subjects = page.locator("#subjectsInput")

    await subjects.fill("Maths")
    await subjects.press("Enter")

    await expect(page.locator(".subjects-auto-complete__multi-value")).to_contain_text("Maths")

    await page.locator("#state").click()
    await page.locator("#react-select-3-option-0").click()

    await expect(page.locator("#state")).to_contain_text("NCR")

    await page.locator("#city").click()
    await page.locator("#react-select-4-option-0").click()

    await expect(page.locator("#city")).to_contain_text("Delhi")

    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test file for Playwright")

    await page.locator("#uploadPicture").set_input_files(str(file_path))

    uploaded_file = await page.locator("#uploadPicture").evaluate("(element) => element.files[0].name")

    assert uploaded_file == "test_file.txt"


@allure.feature("Practice Form")
@allure.story("Form Submission")
@allure.title("Полное заполнение и отправка формы")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.asyncio
async def test_practice_form_submission(practice_form_page: Page, tmp_path):
    page = practice_form_page

    await page.locator("#firstName").fill("Roman")
    await page.locator("#lastName").fill("Kulikov")
    await page.locator("#userEmail").fill("roman@example.com")
    await page.locator("#userNumber").fill("1234567890")

    await page.locator("label[for='gender-radio-1']").click()

    await page.locator("#dateOfBirthInput").fill("15 Aug 1995")

    subjects = page.locator("#subjectsInput")
    await subjects.fill("Maths")
    await subjects.press("Enter")

    await page.locator("label[for='hobbies-checkbox-1']").click()
    await page.locator("label[for='hobbies-checkbox-2']").click()

    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test file for Playwright")

    await page.locator("#uploadPicture").set_input_files(str(file_path))

    await page.locator("#currentAddress").fill("Amsterdam, Netherlands")

    await page.locator("#state").click()
    await page.locator("#react-select-3-option-0").click()

    await page.locator("#city").click()
    await page.locator("#react-select-4-option-0").click()

    await page.locator("#submit").click()

    modal = page.locator(".modal-content")

    await expect(modal).to_be_visible()

    await expect(page.locator("#example-modal-sizes-title-lg")).to_have_text("Thanks for submitting the form")

    await expect(modal).to_contain_text("Roman Kulikov")
    await expect(modal).to_contain_text("roman@example.com")
    await expect(modal).to_contain_text("Male")
    await expect(modal).to_contain_text("15 August,1995")
    await expect(modal).to_contain_text("Maths")
    await expect(modal).to_contain_text("Sports")
    await expect(modal).to_contain_text("Reading")
    await expect(modal).to_contain_text("test_file.txt")
    await expect(modal).to_contain_text("NCR")
    await expect(modal).to_contain_text("Delhi")