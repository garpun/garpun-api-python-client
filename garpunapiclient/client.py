import json
import time
import httplib2
import requests

from garpunauth.client import GarpunCredentials

from garpunapiclient.errors import HttpError


class GarpunApi:
    """
    Garpun API's client
    """

    def __init__(
        self,
        host,
        api_version,
        credentials: GarpunCredentials = None,
        http=None,
        max_retries=10,
    ):
        if http is None:
            http = httplib2.Http()

        self.http = http
        self.host = host
        self.api_version = api_version
        self.credentials = credentials
        self.max_retries = max_retries

    def get(self, method_path, get_params=None):
        return self.request("GET", method_path, get_params)

    def post(self, method_path, get_params=None, post_data=None):
        return self.request("POST", method_path, get_params, post_data)

    def request(self, http_method, method_path, get_params=None, post_data=None):
        url = self.host + "/" + self.api_version + "/" + method_path

        if not self.credentials.access_token_expired:
            self.__refresh_access_token()

        auth_error_cnt = 0
        for _try_idx in range(self.max_retries):
            headers = {"Authorization": "Bearer " + self.credentials.access_token}

            req_param = {
                "method": http_method,
                "url": url,
                "data": get_params,
                "json": post_data,
                "headers": headers,
            }
            resp = requests.request(**req_param)
            if resp.status_code == 200:
                return resp

            elif resp.status_code == 401:
                auth_error_cnt += 1
                if auth_error_cnt >= 2:
                    raise HttpError(resp, url)
                self.__refresh_access_token()
                continue

            elif resp.status_code in [502, 503, 504]:
                if _try_idx == self.max_retries - 1:
                    raise HttpError(resp, url)
                else:
                    time.sleep(15)
                    continue

            else:
                # skip all retries, because in internal server error and we
                # must not increase the load.
                raise HttpError(resp, url)

    def __refresh_access_token(self):
        http = self.credentials.authorize(self.http)
        self.credentials.refresh(http)

    @staticmethod
    def build(api_name: str, api_version: str):
        """
        :param api_name: Example hello
        :param api_version: Example v1, v2alpha
        :return: GarpunApi
        """
        api_host = "http://" + api_name + ".apis.devision.io"
        default_credentials, project_id = GarpunCredentials.get_application_default()
        return GarpunApi(
            host=api_host, api_version=api_version, credentials=default_credentials
        )
