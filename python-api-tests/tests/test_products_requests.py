import requests


def test_get_all_products_requests():
    response = requests.get("https://fakestoreapi.com/products")

    assert response.status_code == 200

    products = response.json()

    assert isinstance(products, list)
    assert len(products) > 0


def test_get_product_by_id_requests():
    product_id = 1

    response = requests.get(
        f"https://fakestoreapi.com/products/{product_id}"
    )

    assert response.status_code == 200

    product = response.json()

    assert product["id"] == product_id
    assert product["title"]
    assert product["price"] > 0
    assert product["category"]


def test_create_product_requests():
    new_product = {
        "title": "Requests Test Product",
        "price": 99.99,
        "description": "Product for Requests API testing",
        "category": "electronics"
    }

    response = requests.post(
        "https://fakestoreapi.com/products",
        json=new_product
    )

    assert response.status_code == 201

    created_product = response.json()

    assert created_product["title"] == new_product["title"]
    assert created_product["price"] == new_product["price"]
    assert "id" in created_product


def test_patch_product_requests():
    updated_data = {
        "price": 199.99
    }

    response = requests.patch(
        "https://fakestoreapi.com/products/1",
        json=updated_data
    )

    assert response.status_code == 200

    product = response.json()

    assert product["price"] == updated_data["price"]


def test_update_product_requests():
    updated_product = {
        "title": "Updated Requests Product",
        "price": 149.99,
        "description": "Updated description",
        "category": "electronics"
    }

    response = requests.put(
        "https://fakestoreapi.com/products/1",
        json=updated_product
    )

    assert response.status_code == 200

    product = response.json()

    assert product["title"] == updated_product["title"]
    assert product["price"] == updated_product["price"]
    assert product["category"] == updated_product["category"]


def test_delete_product_requests():
    response = requests.delete(
        "https://fakestoreapi.com/products/1"
    )

    assert response.status_code == 200

    result = response.json()

    assert result["id"] == 1