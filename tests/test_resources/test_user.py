"""Tests for the User resource."""

import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport
from raindrop_client.resources.user import UserResource

from tests.conftest import make_user

BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestUserResource:
    def _make_resource(self):
        transport = HttpTransport(token="test-token")
        return UserResource(transport), transport

    def test_get(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/user").respond(200, json={
                "result": True,
                "user": make_user(),
            })
            resource, transport = self._make_resource()
            result = resource.get()
            assert result.id == 1001
            assert result.full_name == "Test User"
            assert result.pro is True
            transport.close()

    def test_update(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/user").respond(200, json={
                "result": True,
                "user": make_user(fullName="Updated Name"),
            })
            resource, transport = self._make_resource()
            result = resource.update(full_name="Updated Name")
            assert result.full_name == "Updated Name"
            transport.close()

    def test_get_public(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/user/johndoe").respond(200, json={
                "result": True,
                "user": make_user(_id=2002, fullName="John Doe"),
            })
            resource, transport = self._make_resource()
            result = resource.get_public("johndoe")
            assert result.id == 2002
            assert result.full_name == "John Doe"
            transport.close()

    def test_get_stats(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/user/stats").respond(200, json={
                "items": 500,
                "trash": 10,
                "pro": True,
            })
            resource, transport = self._make_resource()
            result = resource.get_stats()
            assert result.items == 500
            assert result.trash == 10
            transport.close()

    def test_disconnect(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/user/connect/google").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.disconnect("google")
            assert result is True
            transport.close()
