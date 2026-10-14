import os
import uuid

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://compassuol.serverest.dev").rstrip("/")
TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "15"))


@pytest.fixture
def api():
    """Small API client shared by tests; keeps URL and timeout in one place."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})

    class Client:
        base_url = BASE_URL

        def request(self, method, path, **kwargs):
            kwargs.setdefault("timeout", TIMEOUT)
            return session.request(method, f"{BASE_URL}{path}", **kwargs)

        def get(self, path, **kwargs):
            return self.request("GET", path, **kwargs)

        def post(self, path, **kwargs):
            return self.request("POST", path, **kwargs)

        def put(self, path, **kwargs):
            return self.request("PUT", path, **kwargs)

        def delete(self, path, **kwargs):
            return self.request("DELETE", path, **kwargs)

    yield Client()
    session.close()


@pytest.fixture
def unique_email():
    return f"qa.genai.{uuid.uuid4().hex[:12]}@example.com"


@pytest.fixture
def create_user(api):
    """Creates a unique user and attempts cleanup after the test."""
    created_ids = []

    def _create(is_admin="false"):
        email = f"qa.genai.{uuid.uuid4().hex[:12]}@example.com"
        payload = {
            "nome": "QA GenAI Automation",
            "email": email,
            "password": "Test@12345",
            "administrador": is_admin,
        }
        response = api.post("/usuarios", json=payload)
        assert response.status_code in (200, 201), (
            f"User creation failed: HTTP {response.status_code}; body={response.text}"
        )
        body = response.json()
        user_id = body.get("_id")
        if user_id:
            created_ids.append(user_id)
        return {"id": user_id, "email": email, "password": payload["password"], "body": body}

    yield _create

    # Cleanup is best-effort: shared test environments can change between requests.
    for user_id in created_ids:
        try:
            api.delete(f"/usuarios/{user_id}")
        except requests.RequestException:
            pass


@pytest.fixture
def admin_session(api, create_user):
    user = create_user(is_admin="true")
    login = api.post("/login", json={"email": user["email"], "password": user["password"]})
    assert login.status_code == 200, f"Admin login failed: HTTP {login.status_code}; body={login.text}"
    token = login.json().get("authorization")
    assert token, f"Login response did not include authorization token: {login.text}"
    return {"user": user, "headers": {"Authorization": token}}


@pytest.fixture
def regular_session(api, create_user):
    user = create_user(is_admin="false")
    login = api.post("/login", json={"email": user["email"], "password": user["password"]})
    assert login.status_code == 200, f"User login failed: HTTP {login.status_code}; body={login.text}"
    token = login.json().get("authorization")
    assert token, f"Login response did not include authorization token: {login.text}"
    return {"user": user, "headers": {"Authorization": token}}
