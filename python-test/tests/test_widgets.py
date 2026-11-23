import re
import allure
from playwright.sync_api import Page, expect


@allure.feature("Widgets")
@allure.story("Accordian")
@allure.title("Проверка раскрытия секций Accordian")
@allure.severity(allure.severity_level.NORMAL)
def test_accordian(widgets_page: Page):
    widgets_page.get_by_role("link", name="Accordian").click()
    expect(widgets_page).to_have_url("https://demoqa.com/accordian")

    sections = [
        ("What is Lorem Ipsum?", "Lorem Ipsum is simply dummy text"),
        ("Where does it come from?", "Contrary to popular belief"),
        ("Why do we use it?", "It is a long established fact"),
    ]

    for title, expected_text in sections:
        heading = widgets_page.get_by_role("heading", name=title)
        button = heading.get_by_role("button")
        content = heading.locator("xpath=following-sibling::div")

        if not content.is_visible():
            button.click()

        expect(content).to_be_visible()
        expect(content).to_contain_text(expected_text)


@allure.feature("Widgets")
@allure.story("Auto Complete")
@allure.title("Проверка множественного выбора значений Auto Complete")
@allure.severity(allure.severity_level.NORMAL)
def test_auto_complete_multiple(widgets_page: Page):
    widgets_page.get_by_role("link", name="Auto Complete").click()
    expect(widgets_page).to_have_url("https://demoqa.com/auto-complete")

    input_field = widgets_page.locator("#autoCompleteMultipleInput")

    for color in ["Red", "Green", "Blue"]:
        input_field.fill(color)
        option = widgets_page.locator(".auto-complete__option").filter(has_text=color)
        expect(option).to_be_visible()
        option.click()

        expect(widgets_page.get_by_role("button", name=f"Remove {color}")).to_be_visible()

    expect(widgets_page.get_by_role("button", name="Remove Red")).to_be_visible()
    expect(widgets_page.get_by_role("button", name="Remove Green")).to_be_visible()
    expect(widgets_page.get_by_role("button", name="Remove Blue")).to_be_visible()

    widgets_page.get_by_role("button", name="Remove Red").click()

    expect(widgets_page.get_by_role("button", name="Remove Red")).to_be_hidden()
    expect(widgets_page.get_by_role("button", name="Remove Green")).to_be_visible()
    expect(widgets_page.get_by_role("button", name="Remove Blue")).to_be_visible()


@allure.feature("Widgets")
@allure.story("Auto Complete")
@allure.title("Проверка одиночного выбора значений Auto Complete")
@allure.severity(allure.severity_level.NORMAL)
def test_auto_complete_single(widgets_page: Page):
    widgets_page.get_by_role("link", name="Auto Complete").click()

    input_field = widgets_page.locator("#autoCompleteSingleInput")

    input_field.fill("Blue")
    option = widgets_page.locator(".auto-complete__option").filter(has_text="Blue")

    expect(option).to_be_visible()
    option.click()

    selected_value = widgets_page.locator(".auto-complete__single-value")
    expect(selected_value).to_have_text("Blue")

    input_field.fill("Black")
    widgets_page.locator(".auto-complete__option").filter(has_text="Black").click()
    expect(selected_value).to_have_text("Black")


@allure.feature("Widgets")
@allure.story("Date Picker")
@allure.title("Проверка выбора даты и времени")
@allure.severity(allure.severity_level.NORMAL)
def test_date_picker(widgets_page: Page):
    widgets_page.get_by_role("link", name="Date Picker").click()
    expect(widgets_page).to_have_url("https://demoqa.com/date-picker")

    date_input = widgets_page.locator("#datePickerMonthYearInput")

    date_input.fill("05/21/2026")
    date_input.press("Enter")
    expect(date_input).to_have_value("05/21/2026")

    date_input.fill("11/21/2026")
    date_input.press("Enter")
    expect(date_input).to_have_value("11/21/2026")

    date_time_input = widgets_page.locator("#dateAndTimePickerInput")
    date_time_input.fill("May 21, 2026 3:00 PM")
    date_time_input.press("Enter")

    expect(date_time_input).to_have_value("May 21, 2026 3:00 PM")
    date_time_input.fill("November 21, 2026 10:30 AM")
    date_time_input.press("Enter")

    expect(date_time_input).to_have_value("November 21, 2026 10:30 AM")


@allure.feature("Widgets")
@allure.story("Slider")
@allure.title("Проверка изменения значения Slider")
@allure.severity(allure.severity_level.NORMAL)
def test_slider(widgets_page: Page):
    widgets_page.get_by_role("link", name="Slider").click()
    expect(widgets_page).to_have_url("https://demoqa.com/slider")

    slider = widgets_page.locator('input[type="range"]')
    slider.focus()
    slider.press("Home")
    expect(slider).to_have_value("0")

    for _ in range(10):
        slider.press("ArrowRight")

    expect(slider).to_have_value("10")
    slider.press("End")
    expect(slider).to_have_value("100")
    slider.press("Home")
    expect(slider).to_have_value("0")


@allure.feature("Widgets")
@allure.story("Progress Bar")
@allure.title("Проверка запуска, остановки и сброса Progress Bar")
@allure.severity(allure.severity_level.NORMAL)
def test_progress_bar(widgets_page: Page):
    widgets_page.get_by_role("link", name="Progress Bar").click()
    expect(widgets_page).to_have_url("https://demoqa.com/progress-bar")

    def get_progress_value(progress_bar):
        match = re.search(r"\d+", progress_bar.inner_text())
        assert match is not None, "Progress Bar не содержит числового значения"
        return int(match.group())

    progress_bar = widgets_page.locator("#progressBar .progress-bar")

    expect(progress_bar).to_have_text("0%")

    start_button = widgets_page.get_by_role("button", name="Start")
    start_button.click()

    widgets_page.wait_for_function(
        """
        () => {
            const bar = document.querySelector("#progressBar .progress-bar");
            return bar && parseInt(bar.textContent, 10) >= 73;
        }
        """,
        timeout=15000
    )

    widgets_page.get_by_role("button", name="Stop").click()

    match = re.search(r"\d+", progress_bar.inner_text())
    assert match is not None

    stopped_value = int(match.group())
    assert 73 <= stopped_value <= 85

    expect(start_button).to_be_visible()

    widgets_page.wait_for_timeout(500)

    assert get_progress_value(progress_bar) == stopped_value

    start_button.click()
    expect(progress_bar).to_have_text("100%", timeout=15000)

    reset_button = widgets_page.get_by_role("button", name="Reset")
    expect(reset_button).to_be_visible()
    reset_button.click()

    expect(progress_bar).to_have_text("0%")

    start_button.click()
    expect(progress_bar).to_have_text("100%", timeout=15000)


@allure.feature("Widgets")
@allure.story("Tabs")
@allure.title("Проверка переключения вкладок")
@allure.severity(allure.severity_level.NORMAL)
def test_tabs(widgets_page: Page):
    widgets_page.get_by_role("link", name="Tabs").click()
    expect(widgets_page).to_have_url("https://demoqa.com/tabs")

    tabs = [
        ("What", "demo-tab-what"),
        ("Origin", "demo-tab-origin"),
        ("Use", "demo-tab-use"),
    ]

    for name, tab_id in tabs:
        tab = widgets_page.get_by_role("tab", name=name)
        tab.click()
        expect(tab).to_have_attribute("aria-selected", "true")

        active_tabs = widgets_page.locator('[role="tab"][aria-selected="true"]')
        expect(active_tabs).to_have_count(1)

        panel = widgets_page.get_by_role("tabpanel")

        expect(panel).to_be_visible()
        expect(panel).to_contain_text("Lorem Ipsum")
        expect(panel).to_have_attribute("aria-labelledby", tab_id)

    disabled_tab = widgets_page.get_by_role("tab", name="More")
    expect(disabled_tab).to_be_disabled()


@allure.feature("Widgets")
@allure.story("Tool Tips")
@allure.title("Проверка отображения всплывающих подсказок")
@allure.severity(allure.severity_level.NORMAL)
def test_tool_tips(widgets_page: Page):
    widgets_page.get_by_role("link", name="Tool Tips").click()
    expect(widgets_page).to_have_url("https://demoqa.com/tool-tips")

    tooltip = widgets_page.locator(".tooltip")

    button = widgets_page.locator("#toolTipButton")
    button.hover()

    expect(tooltip).to_be_visible()
    expect(tooltip).to_contain_text("You hovered over the Button")

    input_field = widgets_page.locator("#toolTipTextField")
    input_field.scroll_into_view_if_needed()
    input_field.hover()
    input_field.focus()

    expect(input_field).to_be_focused()
    expect(tooltip).to_be_visible()
    expect(tooltip).to_contain_text(re.compile("You hovered over the text field", re.IGNORECASE))

    contrary = widgets_page.get_by_role("link", name="Contrary")
    contrary.hover()

    expect(tooltip).to_be_visible()
    expect(tooltip).to_contain_text("You hovered over the Contrary")

    number = widgets_page.get_by_role("link", name="1.10.32")
    number.hover()

    expect(tooltip).to_be_visible()
    expect(tooltip).to_contain_text("You hovered over the 1.10.32")

    widgets_page.get_by_role("heading", name="Tool Tips").hover()
    expect(tooltip).to_be_hidden()


@allure.feature("Widgets")
@allure.story("Menu")
@allure.title("Проверка отображения пунктов меню и подменю")
@allure.severity(allure.severity_level.NORMAL)
def test_menu(widgets_page: Page):
    widgets_page.get_by_role("link", name="Menu", exact=True).click()
    expect(widgets_page).to_have_url("https://demoqa.com/menu")

    menu = widgets_page.locator("#nav")

    main_item_1 = menu.get_by_role("link", name="Main Item 1")
    main_item_2 = menu.get_by_role("link", name="Main Item 2")
    main_item_3 = menu.get_by_role("link", name="Main Item 3")

    expect(main_item_1).to_be_visible()
    expect(main_item_2).to_be_visible()
    expect(main_item_3).to_be_visible()

    main_item_2.hover()

    sub_items = menu.get_by_role("link", name="Sub Item", exact=True)
    expect(sub_items).to_have_count(2)

    for i in range(2):
        expect(sub_items.nth(i)).to_be_visible()

    sub_sub_list = menu.get_by_role("link", name="SUB SUB LIST »")
    expect(sub_sub_list).to_be_visible()
    sub_sub_list.hover()
    expect(menu.get_by_role("link", name="Sub Sub Item 1")).to_be_visible()
    expect(menu.get_by_role("link", name="Sub Sub Item 2")).to_be_visible()


@allure.feature("Widgets")
@allure.story("Select Menu")
@allure.title("Проверка выбора значений в Select Menu")
@allure.severity(allure.severity_level.NORMAL)
def test_select_menu(widgets_page: Page):
    widgets_page.get_by_role("link", name="Select Menu").click()
    expect(widgets_page).to_have_url("https://demoqa.com/select-menu")

    opt_group = widgets_page.locator("#withOptGroup")
    opt_group.click()

    widgets_page.get_by_text("Group 1, option 1", exact=True).click()
    expect(opt_group).to_contain_text("Group 1, option 1")

    select_one = widgets_page.locator("#selectOne")
    select_one.click()

    widgets_page.get_by_text("Dr.", exact=True).click()
    expect(select_one).to_contain_text("Dr.")

    select_one.click()
    widgets_page.get_by_text("Mr.", exact=True).click()
    expect(select_one).to_contain_text("Mr.")

    old_select = widgets_page.locator("#oldSelectMenu")

    old_select.select_option(label="Red")
    expect(old_select.locator("option:checked")).to_have_text("Red")

    old_select.select_option(label="Blue")
    expect(old_select.locator("option:checked")).to_have_text("Blue")

    old_select.select_option(label="Green")
    expect(old_select.locator("option:checked")).to_have_text("Green")

    multi_dropdown = widgets_page.locator('input[id^="react-select-"][id$="-input"]').nth(2)

    multi_dropdown.scroll_into_view_if_needed()
    multi_dropdown.click()

    multi_listbox = widgets_page.get_by_role("listbox").first
    multi_listbox.get_by_role("option", name="Green").click()

    expect(widgets_page.get_by_role("button", name="Remove Green")).to_be_visible()

    multi_dropdown.click()
    multi_listbox = widgets_page.get_by_role("listbox").first
    multi_listbox.get_by_role("option", name="Blue").click()

    expect(widgets_page.get_by_role("button", name="Remove Green")).to_be_visible()
    expect(widgets_page.get_by_role("button", name="Remove Blue")).to_be_visible()

    widgets_page.get_by_role("button", name="Remove Green").click()
    expect(widgets_page.get_by_role("button", name="Remove Green")).to_have_count(0)

    widgets_page.get_by_role("button", name="Remove Blue").click()
    expect(widgets_page.get_by_role("button", name="Remove Blue")).to_have_count(0)

    multi_select = widgets_page.locator("#cars")

    multi_select.select_option(["volvo", "saab"])
    expect(multi_select.locator("option:checked")).to_have_count(2)

    multi_select.select_option(["opel", "audi"])
    expect(multi_select.locator("option:checked")).to_have_count(2)

    multi_select.select_option([])
    expect(multi_select.locator("option:checked")).to_have_count(0)