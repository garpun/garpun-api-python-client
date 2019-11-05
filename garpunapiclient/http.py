import shutil
import time

from garpunapiclient.errors import HttpError


class HttpRequest(object):
    def __init__(
            self,
            max_retries,
            model,
            http_session,
            credentials,
            http_method,
            headers,
            url,
            body_value,
    ):
        self._max_retries = max_retries
        self._model = model
        self._http_session = http_session
        self._credentials = credentials
        self._http_method = http_method
        self._headers = headers
        self._url = url
        self._body_value = body_value

    def execute(self):
        if not self._credentials.access_token_expired:
            self.__refresh_access_token()

        auth_error_cnt = 0
        for _try_idx in range(self._max_retries):
            # access_token can refresh into this loop
            self._headers["Authorization"] = "Bearer " + self._credentials.access_token

            req_param = {
                "url": self._url,
                "method": self._http_method,
                "headers": self._headers,
                "stream": self._model.is_stream(),
            }

            if self._body_value:
                req_param["data"] = self._body_value

            resp = self._http_session.request(**req_param)
            if resp.status_code == 200:
                return self._model.response(resp)

            elif resp.status_code == 401:
                auth_error_cnt += 1
                if auth_error_cnt >= 2:
                    raise HttpError(resp, self._url)
                self.__refresh_access_token()
                continue

            elif resp.status_code in [502, 503, 504]:
                if _try_idx == self._max_retries - 1:
                    raise HttpError(resp, self._url)
                else:
                    time.sleep(10)
                    continue

            else:
                # skip all retries, because in internal server error and we
                # must not increase the load.
                raise HttpError(resp, self._url)

    def __refresh_access_token(self):
        import httplib2
        http = httplib2.Http()
        http = self._credentials.authorize(http)
        self._credentials.refresh(http)


class MediaDownload(object):
    def __init__(self, request: HttpRequest, output_file_description):
        self._request = request
        self._output_file_descriptor = output_file_description

    def full_download(self):
        response = self._request.execute()
        print("response.headers = %s" % str(response.headers))
        # без этого файлы с mime application/json фигово скачиваются
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, self._output_file_descriptor)
