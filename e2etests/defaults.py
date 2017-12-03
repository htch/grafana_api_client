from __future__ import unicode_literals, print_function

import os
import unittest

from grafana_api_client import GrafanaClient, GrafanaUnauthorizedError


class AuthTestCase(unittest.TestCase):
    def test_unauthorized(self):
        gc = GrafanaClient(None, os.getenv("DOCKER_HOST"), 3000)
        with self.assertRaises(GrafanaUnauthorizedError):
            dashboard = gc.dashboards.home.get()

    def test_login(self):
        gc = GrafanaClient(("admin", "admin"), os.getenv("DOCKER_HOST"), 3000)
        org = gc.org.get()
        self.assertEqual(org["name"], "Main Org.")


class ApiKeyTestCase(unittest.TestCase):
    def test_create_apikey(self):
        gc = GrafanaClient(("admin", "admin"), os.getenv("DOCKER_HOST"), 3000)
        keys = gc.auth.keys.get()
        self.assertEqual(keys, [])

        created = gc.auth.keys.create(name="test-key", role="Admin")
        self.assertIsInstance(created, dict)
        
        gc = GrafanaClient(created["key"], os.getenv("DOCKER_HOST"), 3000)
        org = gc.org.get()
        self.assertEqual(org["name"], "Main Org.")



if __name__ == '__main__':
    unittest.main()
