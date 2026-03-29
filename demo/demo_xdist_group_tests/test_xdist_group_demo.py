"""Demo: xdist_group grouping guarantee in hash mode.

All tests sharing the same xdist_group marker are assigned to the same shard.
In the Allure Timeline view, tests of the same group will appear on the same
thread (worker), proving they ran inside the same shard process.
"""

import allure
import pytest


# ---------------------------------------------------------------------------
# group: database — tests that require shared DB state
# ---------------------------------------------------------------------------

@allure.feature("xdist_group: database")
@allure.story("Create")
@pytest.mark.xdist_group("database")
def test_db_create_user():
    assert {"id": 1, "name": "alice"} == {"id": 1, "name": "alice"}


@allure.feature("xdist_group: database")
@allure.story("Read")
@pytest.mark.xdist_group("database")
def test_db_read_user():
    assert "alice" in ["alice", "bob"]


@allure.feature("xdist_group: database")
@allure.story("Update")
@pytest.mark.xdist_group("database")
def test_db_update_user():
    record = {"name": "alice"}
    record["name"] = "alice_updated"
    assert record["name"] == "alice_updated"


@allure.feature("xdist_group: database")
@allure.story("Delete")
@pytest.mark.xdist_group("database")
def test_db_delete_user():
    users = ["alice", "bob"]
    users.remove("alice")
    assert "alice" not in users


@allure.feature("xdist_group: database")
@allure.story("Count")
@pytest.mark.xdist_group("database")
def test_db_count_users():
    assert len(["alice", "bob"]) == 2


# ---------------------------------------------------------------------------
# group: cache — tests that share an in-memory cache
# ---------------------------------------------------------------------------

@allure.feature("xdist_group: cache")
@allure.story("Set")
@pytest.mark.xdist_group("cache")
def test_cache_set():
    cache: dict = {}
    cache["key"] = "value"
    assert cache["key"] == "value"


@allure.feature("xdist_group: cache")
@allure.story("Get")
@pytest.mark.xdist_group("cache")
def test_cache_get():
    cache = {"key": "value"}
    assert cache.get("key") == "value"


@allure.feature("xdist_group: cache")
@allure.story("Expire")
@pytest.mark.xdist_group("cache")
def test_cache_expire():
    cache = {"key": "value"}
    del cache["key"]
    assert "key" not in cache


@allure.feature("xdist_group: cache")
@allure.story("Miss")
@pytest.mark.xdist_group("cache")
def test_cache_miss():
    cache: dict = {}
    assert cache.get("missing") is None


# ---------------------------------------------------------------------------
# group: auth — tests that depend on a shared auth token
# ---------------------------------------------------------------------------

@allure.feature("xdist_group: auth")
@allure.story("Login")
@pytest.mark.xdist_group("auth")
def test_auth_login():
    assert "token_abc123" != ""


@allure.feature("xdist_group: auth")
@allure.story("Verify token")
@pytest.mark.xdist_group("auth")
def test_auth_verify_token():
    token = "token_abc123"
    assert token.startswith("token_")


@allure.feature("xdist_group: auth")
@allure.story("Refresh token")
@pytest.mark.xdist_group("auth")
def test_auth_refresh_token():
    old_token = "token_abc123"
    new_token = "token_xyz789"
    assert old_token != new_token


@allure.feature("xdist_group: auth")
@allure.story("Logout")
@pytest.mark.xdist_group("auth")
def test_auth_logout():
    session = {"token": "token_abc123", "user": "alice"}
    session.clear()
    assert session == {}


# ---------------------------------------------------------------------------
# Standalone tests — no xdist_group, hashed by node ID
# ---------------------------------------------------------------------------

@allure.feature("No xdist_group (standalone)")
@allure.story("Math")
def test_standalone_add():
    assert 1 + 1 == 2


@allure.feature("No xdist_group (standalone)")
@allure.story("Math")
def test_standalone_mul():
    assert 3 * 4 == 12


@allure.feature("No xdist_group (standalone)")
@allure.story("String")
def test_standalone_upper():
    assert "hello".upper() == "HELLO"


@allure.feature("No xdist_group (standalone)")
@allure.story("List")
def test_standalone_sort():
    assert sorted([3, 1, 2]) == [1, 2, 3]
