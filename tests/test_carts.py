def test_list_carts_returns_collection(api):
    response = api.get("/carrinhos")

    assert response.status_code == 200, response.text
    body = response.json()
    assert isinstance(body.get("carrinhos"), list)
    assert isinstance(body.get("quantidade"), int)


def test_create_cart_without_authorization_is_rejected(api):
    response = api.post("/carrinhos", json={"produtos": []})

    assert response.status_code in (401, 403), response.text


def test_cart_creation_with_nonexistent_product_is_rejected(api, regular_session):
    payload = {"produtos": [{"idProduto": "produto-inexistente-qa", "quantidade": 1}]}
    response = api.post("/carrinhos", json=payload, headers=regular_session["headers"])

    assert response.status_code in (400, 404, 422), response.text
