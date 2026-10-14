def test_login_with_valid_credentials_returns_authorization(api, create_user):
    user = create_user()
    response = api.post("/login", json={"email": user["email"], "password": user["password"]})

    assert response.status_code == 200, response.text
    body = response.json()
    assert body.get("message")
    assert isinstance(body.get("authorization"), str)
    assert body["authorization"].strip()


def test_login_with_wrong_password_is_rejected(api, create_user):
    user = create_user()
    response = api.post("/login", json={"email": user["email"], "password": "wrong-password"})

    assert response.status_code in (400, 401), response.text


def test_login_with_missing_fields_is_rejected(api):
    response = api.post("/login", json={})

    assert response.status_code in (400, 401, 422), response.text
