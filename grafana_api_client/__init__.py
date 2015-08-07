from __future__ import unicode_literals

import requests

__all__ = map(str, ["GrafanaException", "GrafanaServerError", "GrafanaClientError",
 "GrafanaBadInputError", "GrafanaUnauthorizedError", "GrafanaPreconditionFailedError",
 "GrafanaClient"])

class GrafanaException(Exception):
    pass


class GrafanaServerError(Exception):
    """
    Something unpleasant happened to grafana server (5xx errors)
    """
    pass


class GrafanaClientError(Exception):
    """
    Invalid input (4xx errors)
    """
    pass


class GrafanaBadInputError(GrafanaClientError):
    """
    `400 - Errors (invalid json, missing or invalid fields, etc)`
    """
    pass


class GrafanaUnauthorizedError(GrafanaClientError):
    """
    `401 - Unauthorized`
    """
    pass


class GrafanaPreconditionFailedError(GrafanaClientError):
    """
    `412 - Precondition failed`
    `The 412 status code is used when a newer dashboard already exists (newer, its version is greater than the version that was sent). The same status code is also used if another dashboard exists with the same title.`
    """
    pass


class DeferredClientRequest(object):
    def __init__(self, client, path_sections):
        self.client = client
        self.path_sections = path_sections

    def __getattr__(self, path_section):
        self.path_sections.append(path_section)
        return self

    def __getitem__(self, path_section):
        self.path_sections.append(unicode(path_section))
        return self

    def make_request(self, method, payload):
        endpoint = "/".join(self.path_sections)
        return self.client.make_raw_request(method, endpoint, payload)

    def __call__(self, **payload):
        return self.get(**payload)

    def get(self, **payload):
        return self.make_request("get", payload)

    def create(self, **payload):
        return self.make_request("post", payload)

    def delete(self, **payload):
        return self.make_request("delete", payload)

    def replace(self, **payload):
        return self.make_request("put", payload)

    def update(self, **payload):
        return self.make_request("patch", payload)

    def __repr__(self):
        return "<grafana_api_client.DeferredClientRequest for '{0}'>".format("/".join(self.path_sections))

AUTHENTICATE_WITH_API_KEY = type(str(""), (object,), {})
AUTHENTICATE_WITH_LOGIN_CREDENTIALS = type(str(""), (object,), {})


class GrafanaClient(object):
    def __init__(self, authenticate_with, host="127.0.0.1", port=None, url_path_prefix="", protocol="http"):
        """Instantiates Grafana API Client

        Usage:

        >>> client = GrafanaClient(("admin", "admin"))
        >>> client.org.get()
        {"id":1,"name":"Main Org."}

        >>> client.dashboards.db.post(dashboard={...}, overwrite=False)
        {"dashboard": {...}, "overwrite": false}

        :param authenticate_with: Authentication parameters, either string (api_key) or 2-ary tuple with login credentials (("login", "password"))
        :param host: Grafana instance hostname
        :type state: str.
        :param port: Grafana instance port
        :type state: int.
        :param url_path_prefix: Grafana url path prefix (such as "grafana" if your grafana instance is available on http://127.0.0.1/grafana/)
        :type state: str.
        :param protocol: Protocol ("http" or "https")
        :type state: str.
        """
        self.url_protocol = protocol
        self.url_host = host
        if isinstance(port, int):
            port = str(port)
        self.url_port = port
        if url_path_prefix and not url_path_prefix.endswith("/"):
            url_path_prefix = "{0}/".format(url_path_prefix)
        self.url_path_prefix = url_path_prefix

        self.custom_requests_params = {}
        
        if isinstance(authenticate_with, basestring):
            self.authenticate_with_api_key(authenticate_with)
        else:
            self.authenticate_with_login_credentials(*authenticate_with)

    def construct_api_url(self, endpoint):
        params = {
            "protocol": self.url_protocol,
            "host": self.url_host,
            "path_prefix": self.url_path_prefix,
            "endpoint": endpoint,
        }
        if self.authentication_method == AUTHENTICATE_WITH_LOGIN_CREDENTIALS:
            if self.url_port is None:
                url_pattern = "{protocol}://{login}:{password}@{host}/{path_prefix}api/{endpoint}"
            else:
                params["port"] = self.url_port
                url_pattern = "{protocol}://{login}:{password}@{host}:{port}/{path_prefix}api/{endpoint}"
            params["login"] = self.login
            params["password"] = self.password
        elif self.authentication_method == AUTHENTICATE_WITH_API_KEY:
            if self.url_port is None:
                url_pattern = "{protocol}://{host}/{path_prefix}api/{endpoint}"
            else:
                params["port"] = self.url_port
                url_pattern = "{protocol}://{host}:{port}/{path_prefix}api/{endpoint}"
        return url_pattern.format(**params)

    def construct_headers(self):
        headers = {"Accept": "application/json; charset=UTF-8"}
        if self.authentication_method == AUTHENTICATE_WITH_API_KEY:
            headers["Authorization"] = "Bearer {0}".format(self.api_key)
        return headers

    def authenticate_with_login_credentials(self, login, password):
        self.authentication_method = AUTHENTICATE_WITH_LOGIN_CREDENTIALS
        self.login, self.password = login, password

    def authenticate_with_api_key(self, api_key):
        self.authentication_method = AUTHENTICATE_WITH_API_KEY
        self.api_key = api_key

    def make_raw_request(self, method, endpoint, payload):
        url = self.construct_api_url(endpoint)
        headers = self.construct_headers()
        if method.upper() == "GET":
            r = requests.request("GET", url, params=payload, headers=headers, **self.custom_requests_params)
        else:
            r = requests.request(method.upper(), url, json=payload, headers=headers, **self.custom_requests_params)
        if 500 <= r.status_code < 600:
            raise GrafanaServerError("Server Error {0}: {1}".format(r.status_code, r.content.decode("ascii", "replace")))      # because who knows what else is broken about the server response
        elif r.status_code == 400:
            raise GrafanaBadInputError("Bad Input: `{0}`".format(r.text))
        elif r.status_code == 401:
            if self.authentication_method == AUTHENTICATE_WITH_LOGIN_CREDENTIALS:
                raise GrafanaUnauthorizedError("Unauthorized (authorization with login credentials failed)")
            else:
                raise GrafanaUnauthorizedError("Unauthorized (authorization with api key failed)")
        elif r.status_code == 412:
            response_data = r.json()
            raise GrafanaPreconditionFailedError("Precondition failed: {status} (`{message}`)".format(**response_data))
        elif 400 <= r.status_code < 500:
            raise GrafanaClientError("Client Error {0}: {1}".format(r.status_code, r.text))
        return r.json()

    def __getattr__(self, path_section):
        return DeferredClientRequest(self, [path_section])

    def __getitem__(self, path_section):
        return DeferredClientRequest(self, [path_section])

    def __repr__(self):
        return "<GrafanaApiClient at '{0}'>".format(self.construct_api_url(""))


GrafanaClient.AUTHENTICATE_WITH_API_KEY = AUTHENTICATE_WITH_API_KEY         # hiding these guys from the package namespace
GrafanaClient.AUTHENTICATE_WITH_LOGIN_CREDENTIALS = AUTHENTICATE_WITH_LOGIN_CREDENTIALS