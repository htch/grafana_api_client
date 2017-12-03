from __future__ import unicode_literals, print_function

import os
import unittest

from grafana_api_client import GrafanaClient


class DashboardTestCase(unittest.TestCase):
    def test_home_dashboard(self):
        """Get home dashboard"""
        gc = GrafanaClient(None, os.getenv("DOCKER_HOST"), 3001)
        dashboard = gc.dashboards.home.get()
        self.assertIsInstance(dashboard, dict)

    def test_create_dashboard(self):
        """Create new dashboard"""
        gc = GrafanaClient(None, os.getenv("DOCKER_HOST"), 3001)
        dashboard = gc.dashboards.db.create(
          dashboard={
            "id": None,
            "title": "Test Dashboard",
            "tags": ["test"],
            "timezone": "browser",
            "rows": []
          },
          overwrite=False
        )
        self.assertEqual(dashboard["slug"], "test-dashboard")

        dashboard = gc.dashboards.db["test-dashboard"].get()
        self.assertIsInstance(dashboard, dict)
        self.assertEqual(dashboard["dashboard"]["title"], "Test Dashboard")


class DataSourceTestCase(unittest.TestCase):
    def test_create_datasource(self):
        """Create Data Source"""
        gc = GrafanaClient(None, os.getenv("DOCKER_HOST"), 3001)
        dss = gc.datasources.get()
        self.assertEqual(dss, [])

        created = gc.datasources.create(
            name="test-datasource",
            type="graphite",
            url="http://localhost",
            access="proxy",
            basicAuth=False
        )
        self.assertIsInstance(created, dict)

        byid = gc.datasources[created["id"]].get()
        self.assertEqual(byid["name"], "test-datasource")

        byname = gc.datasources.name["test-datasource"].get()
        self.assertEqual(byname["id"], created["id"])

        response = gc.datasources.name["test-datasource"].delete()
        self.assertDictEqual(response, {"message": "Data source deleted"})

        dss = gc.datasources.get()
        self.assertEqual(dss, [])


if __name__ == '__main__':
    unittest.main()
