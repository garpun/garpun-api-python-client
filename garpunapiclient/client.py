import requests

from garpunauth.client import GarpunCredentials

from garpunapiclient.http import HttpRequest
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
        http_session=None,
    ):
        if http_session is None:
            http_session = requests.Session()

        self._http_session = http_session
        self._base_url = base_url
        self._credentials = credentials
        self._max_retries = max_retries

    def get(self, method_path, query_params=None, model=None):
        return self.request("GET", method_path, query_params, model=model)

    def post(self, method_path, query_params=None, body_value=None, model=None):
        return self.request("POST", method_path, query_params, body_value, model=model)

    def request(
        self, http_method, method_path, query_params=None, body_value=None, model=None
    ) -> HttpRequest:
        if model is None:
            model = JsonModel()

        if query_params is None:
            query_params = {}

        url = self._base_url + "/" + method_path

        headers = {}
        (headers, query, body_value) = model.request(headers, query_params, body_value)
        url += query

        return HttpRequest(
            self._max_retries,
            model,
            self._http_session,
            self._credentials,
            http_method,
            headers,
            url,
            body_value,
        )

    @staticmethod
    def build(api_name: str, api_version: str):
        """
        :param api_name: Example hello
        :param api_version: Example v1, v2alpha
        :return: GarpunApi
        """
        if api_name == "meta":
            api_host = "http://apimeta.devision.io/api/meta/" + api_version
        else:
            api_host = "http://" + api_name + ".apis.devision.io/" + api_version
        default_credentials, project_id = GarpunCredentials.get_application_default()
        return GarpunApi(base_url=api_host, credentials=default_credentials)
