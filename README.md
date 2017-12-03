Very basic Grafana API wrapper. Supports Grafana v2.1.0 

Usage:

    >>> from grafana_api_client import GrafanaClient
    >>> client = GrafanaClient(("admin", "admin"), host="127.0.0.1", port=3000) # or, alternatively:
    >>> client = GrafanaClient("yourapikey", host="127.0.0.1", port=3000)
    >>> client.org()
        {"id":1,"name":"Main Org."}
    >>> client.org.replace(name="Your Org Ltd.")
        {"id":1,"name":"Your Org Ltd."}
    >>> client.dashboards.db.create(dashboard={...}, overwrite=False)
        {"dashboard": {...}, "overwrite": False}

Please refer to the [Grafana API Documentation](http://docs.grafana.org/reference/http_api/) for a list of available methods.


