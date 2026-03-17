import json
import time
import pytest

from src.api.client import ApiClient
from src.api.users_api import UsersApi
from src.config.settings import API_BASE_URL


def assert_user_contract(user: dict):
    # Minimal contract checks (no extra libs)
    required_keys = ["id", "name", "username", "email"]
    for key in required_keys:
        assert key in user, f"Missing key: {key}"

    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str) and user["name"]
    assert isinstance(user["username"], str) and user["username"]
    assert isinstance(user["email"], str) and "@" in user["email"]


@pytest.fixture
def users_api():
    return UsersApi(ApiClient(API_BASE_URL, timeout_s=10))


@pytest.mark.api
@pytest.mark.api_smoke
def test_list_users_smoke(users_api):
    resp = users_api.list_users()
    assert resp.status_code == 200

    data = resp.json()
    print(json.dumps(data, indent=2))
    assert isinstance(data, list)
    assert len(data) == 10

    # Data consistency quick checks
    ids = [u["id"] for u in data]
    assert len(ids) == len(set(ids)), "User IDs are not unique"

    # Contract check for first item
    assert_user_contract(data[0])


@pytest.mark.api
@pytest.mark.regression
def test_get_user_contract(users_api):
    resp = users_api.get_user(1)
    assert resp.status_code == 200

    user = resp.json()
    assert user["id"] == 1
    assert_user_contract(user)


@pytest.mark.api
@pytest.mark.regression
def test_get_user_not_found(users_api):
    resp = users_api.get_user(999999)
    assert resp.status_code == 404


@pytest.mark.api
@pytest.mark.regression
def test_list_users_basic_performance(users_api):
    start = time.time()
    resp = users_api.list_users()
    end = time.time()
    diff = round(end-start, 2)
    assert resp.status_code == 200
    assert diff < 2.0, f"Too slow: {diff:.2f}s"