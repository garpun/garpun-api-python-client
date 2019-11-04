import time

import requests

from garpunauth.client import GarpunCredentials
from garpunapiclient.errors import HttpError
from garpunapiclient.model import JsonModel


class GarpunApi:
    """
    Garpun API's client
    """

    def __init__(
            self,
            base_url,
            credentials: GarpunCredentials = None,
            max_retries=10,
            http_session=None
    ):
        if http_session is None:
            http_session = requests.Session()

        self.http_session = http_session
        self.base_url = base_url
        self.credentials = credentials
        self.max_retries = max_retries

    def get(self, method_path, query_params=None, model=None):
        return self.request("GET", method_path, query_params, model=model)

    def post(self, method_path, query_params=None, body_value=None, model=None):
        return self.request("POST", method_path, query_params, body_value, model=model)

    def request(
            self, http_method, method_path, query_params=None, body_value=None, model=None
    ):
        if model is None:
            model = JsonModel()

        if query_params is None:
            query_params = {}

        uri = self.base_url + "/" + method_path

        headers = {}
        (headers, query, body_value) = model.request(headers, query_params, body_value)
        uri += query

        if not self.credentials.access_token_expired:
            self.__refresh_access_token()

        auth_error_cnt = 0
        for _try_idx in range(self.max_retries):
            # access_token can refresh into this loop
            headers["Authorization"] = "Bearer " + self.credentials.access_token

            req_param = {
                "url": uri,
                "method": http_method,
                "headers": headers,
                "stream": model.is_stream()
            }

            if body_value:
                req_param["data"] = body_value

            resp = self.http_session.request(**req_param)

            if resp.status_code == 200:
                return model.response(resp)

            elif resp.status_code == 401:
                auth_error_cnt += 1
                if auth_error_cnt >= 2:
                    raise HttpError(resp, uri)
                self.__refresh_access_token()
                continue

            elif resp.status_code in [502, 503, 504]:
                if _try_idx == self.max_retries - 1:
                    raise HttpError(resp, uri)
                else:
                    time.sleep(10)
                    continue

            else:
                # skip all retries, because in internal server error and we
                # must not increase the load.
                raise HttpError(resp, uri)

    def __refresh_access_token(self):
        import httplib2
        http = httplib2.Http()
        http = self.credentials.authorize(http)
        self.credentials.refresh(http)

    @staticmethod
    def build(api_name: str, api_version: str):
        """
        :param api_name: Example hello
        :param api_version: Example v1, v2alpha
        :return: GarpunApi
        """
        if api_name == 'meta':
            api_host = "http://apimeta.devision.io/api/meta/" + api_version
        else:
            api_host = "http://" + api_name + ".apis.devision.io/" + api_version
        default_credentials, project_id = GarpunCredentials.get_application_default()
        return GarpunApi(
            base_url=api_host, credentials=default_credentials
        )
