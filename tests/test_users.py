def test_list_users_returns_collection(api):
    response = api.get("/usuarios")

    assert response.status_code == 200, response.text
    body = response.json()
    assert isinstance(body.get("usuarios"), list)
    assert isinstance(body.get("quantidade"), int)


def test_create_user_with_unique_email_succeeds(api, unique_email):
    payload = {
        "nome": "QA GenAI User Test",
        "email": unique_email,
        "password": "Test@12345",
        "administrador": "false",
    }
    response = api.post("/usuarios", json=payload)

    assert response.status_code in (200, 201), response.text
    body = response.json()
    assert body.get("_id")
    assert body.get("message")

    # Best-effort cleanup of this uniquely created resource.
    cleanup = api.delete(f"/usuarios/{body['_id']}")
    assert cleanup.status_code in (200, 204, 404), cleanup.text


def test_duplicate_user_email_is_rejected(api, create_user):
    user = create_user()
    payload = {
        "nome": "Duplicate QA User",
        "email": user["email"],
        "password": "Test@12345",
        "administrador": "false",
    }
    response = api.post("/usuarios", json=payload)

    assert response.status_code in (400, 409, 422), response.text


def test_get_user_with_nonexistent_id_returns_not_found(api):
    response = api.get("/usuarios/id-que-nao-existe-qa")

    assert response.status_code == 400 or response.status_code == 404, response.text
