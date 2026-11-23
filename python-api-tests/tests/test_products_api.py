from playwright.sync_api import APIResponse
import pytest


def test_get_all_products(api_context):
    response: APIResponse = api_context.get("/products")

    assert response.status == 200

    products = response.json()

    assert isinstance(products, list)
    assert len(products) > 0



@pytest.mark.parametrize("product_id", [1, 2, 3, 4, 5])
def test_get_product_by_id(api_context, product_id):
    response = api_context.get(f"/products/{product_id}")

    assert response.status == 200

    product = response.json()

    assert product["id"] == product_id
    assert product["title"]
    assert product["price"] > 0
    assert product["category"]


def test_create_product(api_context):
    new_product = {
        "title": "Test Product",
        "price": 99.99,
        "description": "Product for API testing",
        "category": "electronics"
    }

    response = api_context.post(
        "/products",
        data=new_product
    )

    assert response.status == 201

    created_product = response.json()

    assert created_product["title"] == new_product["title"]
    assert created_product["price"] == new_product["price"]
    assert "id" in created_product


def test_update_product(api_context):
    updated_product = {
        "title": "Updated Product",
        "price": 149.99,
        "description": "Updated description",
        "image": "https://i.pravatar.cc",
        "category": "electronics"
    }

    response = api_context.put(
        "/products/1",
        data=updated_product
    )

    assert response.status == 200

    product = response.json()

    assert product["title"] == updated_product["title"]
    assert product["price"] == updated_product["price"]


def test_patch_product(api_context):
    updated_data = {
        "price": 199.99
    }

    response = api_context.patch(
        "/products/1",
        data=updated_data
    )

    assert response.status == 200

    product = response.json()

    assert product["price"] == updated_data["price"]



def test_delete_product(api_context):
    response = api_context.delete("/products/1")

    assert response.status == 200

    result = response.json()

    assert result["id"] == 1
