from __future__ import unicode_literals

import unittest

from grafana_api_client import GrafanaClient


class TestCase(unittest.TestCase):
    def test_token_auth(self):
        gc = GrafanaClient("api_key")
        self.assertEquals(gc.session.auth.token, "api_key")

    def test_basic_auth(self):
        gc = GrafanaClient(("login", "password"))
        self.assertEquals(gc.session.auth.username, "login")
        self.assertEquals(gc.session.auth.password, "password")

    def test_construct_api_url(self):
        gc = GrafanaClient("test", "a", 1000, "b", "https")
        self.assertEquals(gc.construct_api_url("c"), "https://a:1000/b/api/c")
        gc = GrafanaClient("test")
        self.assertEquals(gc.construct_api_url("a"), "http://127.0.0.1/api/a")
        self.assertEquals(repr(gc), "<GrafanaApiClient at 'http://127.0.0.1/api/'>")

    def test_deferred_requests_constructor(self):
        class MockGrafanaClient(GrafanaClient):
            def make_raw_request(self, method, endpoint, payload):
                return method.upper(), endpoint

        gc = MockGrafanaClient("test")
        self.assertEquals(gc.a.b.c.get(), ("GET", "a/b/c"))
        self.assertEquals(gc.a.b["c"].get(), ("GET", "a/b/c"))
        self.assertEquals(gc.a.b[123].get(), ("GET", "a/b/123"))
        self.assertEquals(gc.a.b[123](), ("GET", "a/b/123"))
        self.assertEquals(gc.a.b[123].replace(), ("PUT", "a/b/123"))
        self.assertEquals(gc.a.b[123].update(), ("PATCH", "a/b/123"))
        self.assertEquals(gc.dashboards.db.c_d_e.get(), ("GET", "dashboards/db/c-d-e"))


if __name__ == '__main__':
    unittest.main()
