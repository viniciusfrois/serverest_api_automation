def test_list_products_returns_collection(api):
    response = api.get("/produtos")

    assert response.status_code == 200, response.text
    body = response.json()
    assert isinstance(body.get("produtos"), list)
    assert isinstance(body.get("quantidade"), int)


def test_products_endpoint_rejects_create_without_admin_token(api):
    payload = {
        "nome": "QA GenAI unauthorized product",
        "preco": 10,
        "descricao": "Product used to validate authorization",
        "quantidade": 1,
    }
    response = api.post("/produtos", json=payload)

    assert response.status_code in (401, 403), response.text


def test_admin_can_create_and_delete_product(api, admin_session):
    import uuid

    product_id = None
    payload = {
        "nome": f"QA GenAI Product {uuid.uuid4().hex[:8]}",
        "preco": 19,
        "descricao": "Temporary product created by automated test",
        "quantidade": 2,
    }
    response = api.post("/produtos", json=payload, headers=admin_session["headers"])
    assert response.status_code in (200, 201), response.text
    product_id = response.json().get("_id")
    assert product_id, response.text

    try:
        detail = api.get(f"/produtos/{product_id}")
        assert detail.status_code == 200, detail.text
        assert detail.json().get("nome") == payload["nome"]
    finally:
        deleted = api.delete(f"/produtos/{product_id}", headers=admin_session["headers"])
        assert deleted.status_code in (200, 204, 404), deleted.text
