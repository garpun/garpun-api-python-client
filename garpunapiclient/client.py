import json
import time
import urllib
import httplib2

import garpun.auth
import garpun.auth.client
import garpunapiclient
import garpunapiclient.errors


class GarpunApi:
    """
    Garpun API's client
    """

    def __init__(self, host, api_version, credentials=None, http=None, max_retries=10):
        if http is None:
            http = httplib2.Http()

        self.http = http
        self.host = host
        self.api_version = api_version
        self.credentials = credentials
        self.max_retries = max_retries

    def get(self, method_path, query_string=None):
        return self.request("GET", method_path, query_string)

    def post(self, method_path, query_string=None, post_data=None):
        return self.request("POST", method_path, query_string, post_data)

    def request(self, http_method, method_path, query_string=None, post_data=None):
        uri = self.host + '/' + self.api_version + '/' + method_path
        if query_string:
            query_string = urllib.urlencode(query_string)
            if "?" in uri:
                uri += "&" + query_string
            else:
                uri += "?" + query_string

        if not self.credentials.access_token_expired:
            self.__refresh_access_token()

        auth_error_cnt = 0
        for _try_idx in range(self.max_retries):
            headers = {"Authorization": "Bearer " + self.credentials.access_token}

            req_param = {
                "uri": uri,
                "method": http_method,
                "headers": headers,
            }
            if post_data:
                req_param['body'] = json.dumps(post_data)

            resp, content = self.http.request(**req_param)
            if resp['status'] == '200':
                return resp, content

            elif resp['status'] == '401':
                auth_error_cnt += 1
                if auth_error_cnt >= 2:
                    raise garpunapiclient.errors.HttpError(resp, content, uri)
                self.__refresh_access_token()
                continue

            elif resp['status'] in ['502', '503', '504']:
                if _try_idx == self.max_retries - 1:
                    raise garpunapiclient.errors.HttpError(resp, content, uri)
                else:
                    time.sleep(15)
                    continue
            else:
                # skip all retries, because in internal server error and we
                # must not increase the load.
                raise garpunapiclient.errors.HttpError(resp, content, uri)

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
        default_credentials = garpun.auth.client.GarpunCredentials.get_application_default()
        return GarpunApi(
            host=api_host,
            api_version=api_version,
            credentials=default_credentials
        )
