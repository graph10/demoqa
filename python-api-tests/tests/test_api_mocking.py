from playwright.sync_api import Page, expect


def test_api_mocking_page(page: Page):
    page.goto("https://demo.playwright.dev/api-mocking")
    expect(page).to_have_title("Playwright API Mocking demo")


from playwright.sync_api import Page, expect


def test_mock_fruits(page: Page):
    def handle_route(route):
        mock_data = [
            {"name": "Pistol", "id": 21}
        ]

        route.fulfill(json=mock_data)

    page.route("**/api/v1/fruits", handle_route)

    page.goto("https://demo.playwright.dev/api-mocking")

    expect(page.get_by_text("Pistol")).to_be_visible()
    expect(page.get_by_text("Strawberry")).not_to_be_visible()


def test_modify_api_response(page: Page):
    def handle_route(route):
        response = route.fetch()
        data = response.json()

        data.append({"name": "Pistol", "id": 21})

        route.fulfill(response=response, json=data)

    page.route("**/api/v1/fruits", handle_route)

    page.goto("https://demo.playwright.dev/api-mocking")

    expect(page.get_by_text("Pistol")).to_be_visible()
    expect(page.get_by_text("Strawberry")).to_be_visible()


def test_mock_server_error(page: Page):
    def handle_route(route):
        route.fulfill(
            status=500,
            json={"error": "Internal Server Error"}
        )

    page.route("**/api/v1/fruits", handle_route)

    with page.expect_response("**/api/v1/fruits") as response_info:
        page.goto("https://demo.playwright.dev/api-mocking")

    response = response_info.value

    assert response.status == 500
    assert response.json() == {"error": "Internal Server Error"}


def test_mock_network_error(page: Page):
    def handle_route(route):
        route.abort()

    page.route("**/api/v1/fruits", handle_route)

    with page.expect_event(
        "requestfailed",
        predicate=lambda request: "/api/v1/fruits" in request.url
    ) as failed_request:
        page.goto("https://demo.playwright.dev/api-mocking")

    assert "/api/v1/fruits" in failed_request.value.url


def test_mock_request_by_condition(page: Page):
    def handle_route(route):
        request = route.request

        if request.method == "GET":
            route.fulfill(
                json=[{"name": "Only GET", "id": 100}]
            )
        else:
            route.continue_()

    page.route("**/api/v1/fruits", handle_route)

    page.goto("https://demo.playwright.dev/api-mocking")

    expect(page.get_by_text("Only GET")).to_be_visible()


def test_modify_request(page: Page):
    modified_headers = {}

    def handle_route(route):
        headers = {
            **route.request.headers,
            "x-test-header": "Playwright"
        }

        modified_headers.update(headers)

        route.continue_(headers=headers)

    page.route("**/api/v1/fruits**", handle_route)

    page.goto("https://demo.playwright.dev/api-mocking")
    page.wait_for_load_state("networkidle")

    assert modified_headers.get("x-test-header") == "Playwright"


def test_modify_request_url(page: Page):
    def handle_route(route):
        route.continue_(
            url="https://demo.playwright.dev/api/v1/fruits"
        )

    page.route("**/api/v1/fruits", handle_route)

    with page.expect_request(
        lambda request: "/api/v1/fruits" in request.url
    ) as request_info:
        page.goto("https://demo.playwright.dev/api-mocking")

    assert "/api/v1/fruits" in request_info.value.url


def test_record_har(browser):
    context = browser.new_context(
        record_har_path="tests/fruits.har"
    )

    page = context.new_page()
    page.goto("https://demo.playwright.dev/api-mocking")

    page.wait_for_load_state("networkidle")

    context.close()


def test_mock_from_har(browser):
    context = browser.new_context()

    context.route_from_har(
        "tests/fruits.har",
        url="**/api/v1/fruits",
        not_found="abort"
    )

    page = context.new_page()
    page.goto("https://demo.playwright.dev/api-mocking")

    expect(page.get_by_text("Strawberry")).to_be_visible()

    context.close()


def test_update_har(browser):
    context = browser.new_context()

    context.route_from_har(
        "tests/fruits_updated.har",
        url="**/api/v1/fruits",
        update=True
    )

    page = context.new_page()
    page.goto("https://demo.playwright.dev/api-mocking")

    expect(page.get_by_text("Strawberry")).to_be_visible()

    context.close()


def test_mock_from_updated_har(browser):
    context = browser.new_context()

    context.route_from_har(
        "tests/fruits_updated.har",
        url="**/api/v1/fruits",
        not_found="abort"
    )

    page = context.new_page()
    page.goto("https://demo.playwright.dev/api-mocking")

    expect(page.get_by_text("Strawberry")).to_be_visible()

    context.close()


def test_route_fallback(page: Page):
    def first_handler(route):
        route.fulfill(
            json=[{"name": "Fallback Fruit", "id": 100}]
        )

    def second_handler(route):
        route.fallback()

    page.route("**/api/v1/fruits", first_handler)
    page.route("**/api/v1/fruits", second_handler)

    page.goto("https://demo.playwright.dev/api-mocking")

    expect(page.get_by_text("Fallback Fruit")).to_be_visible()


def test_route_fallback_with_headers(page: Page):
    def first_handler(route):
        assert route.request.headers.get("x-test-header") == "Playwright"
        route.fulfill(
            json=[{"name": "Header Passed", "id": 101}]
        )

    def second_handler(route):
        route.fallback(
            headers={"x-test-header": "Playwright"}
        )

    page.route("**/api/v1/fruits", first_handler)
    page.route("**/api/v1/fruits", second_handler)

    page.goto("https://demo.playwright.dev/api-mocking")

    expect(page.get_by_text("Header Passed")).to_be_visible()


def test_modify_response_conditionally(page: Page):
    def handle_route(route):
        response = route.fetch()
        data = response.json()

        if not any(fruit["name"] == "Pistol" for fruit in data):
            data.append({"name": "Pistol", "id": 200})

        route.fulfill(response=response, json=data)

    page.route("**/api/v1/fruits", handle_route)

    page.goto("https://demo.playwright.dev/api-mocking")

    expect(page.get_by_text("Pistol")).to_be_visible()
    expect(page.get_by_text("Strawberry")).to_be_visible()


def test_mock_request_by_query(page: Page):
    def handle_route(route):
        request_url = route.request.url

        if "category=fruit" in request_url:
            route.fulfill(
                json=[{"name": "Filtered Fruit", "id": 300}]
            )
        else:
            route.continue_()

    page.route("**/api/v1/fruits**", handle_route)

    page.goto("https://demo.playwright.dev/api-mocking")

    result = page.evaluate("""
        async () => {
            const response = await fetch(
                '/api/v1/fruits?category=fruit'
            );
            return await response.json();
        }
    """)

    assert result == [{"name": "Filtered Fruit", "id": 300}]