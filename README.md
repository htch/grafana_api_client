Very basic Grafana API wrapper. Supports Grafana v2.1.0 

Usage:
    
    >>> client = GrafanaClient(("admin", "admin"), host="127.0.0.1", port=3000)
    >>> client.org.get()
        {"id":1,"name":"Main Org."}
    >>> client.dashboards["db"].post({"dashboard": {...}, "overwrite": false})
        {"dashboard": {...}, "overwrite": false}

Please refer to the [Grafana API Documentation](http://docs.grafana.org/reference/http_api/) for a list of available methods.