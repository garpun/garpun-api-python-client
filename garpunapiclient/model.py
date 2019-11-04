import json
import logging
import platform
from urllib.parse import urlencode

from garpunapiclient.errors import HttpError

LOGGER = logging.getLogger(__name__)
_PY_VERSION = platform.python_version()

dump_request_response = False


def _abstract():
    raise NotImplementedError("You need to override this function")


class Model(object):
    def request(self, headers, query_params, post_data):
        _abstract()

    def response(self, resp, content):
        _abstract()


class BaseModel(Model):
    accept = None
    content_type = None
    no_content_response = None
    alt_param = None

    def request(self, headers, query_params, body_value):
        query = self._build_query(query_params)
        headers["accept"] = self.accept
        headers["accept-encoding"] = "gzip, deflate"
        if "user-agent" in headers:
            headers["user-agent"] += " "
        else:
            headers["user-agent"] = ""
        headers["user-agent"] += "(gzip)"

        if body_value is not None:
            headers["content-type"] = self.content_type
            body_value = self.serialize(body_value)
        return (headers, query, body_value)

    def _build_query(self, params):
        astuples = []
        for key, value in params.items():
            if type(value) == type([]):
                for x in value:
                    x = x.encode("utf-8")
                    astuples.append((key, x))
            else:
                if isinstance(value, str) and callable(value.encode):
                    value = value.encode("utf-8")
                astuples.append((key, value))
        return "?" + urlencode(astuples)

    def response(self, resp, content):
        # Error handling is TBD, for example, do we retry
        # for some operation/error combinations?
        if resp.status < 300:
            if resp.status == 204:
                # A 204: No Content response should be treated differently
                # to all the other success states
                return self.no_content_response
            return self.deserialize(content)
        else:
            LOGGER.debug("Content from bad request was: %s" % content)
            raise HttpError(resp, content)

    def serialize(self, body_value):
        _abstract()

    def deserialize(self, content):
        _abstract()


class JsonModel(BaseModel):
    accept = "application/json"
    content_type = "application/json"
    alt_param = "json"

    def __init__(self, data_wrapper=False):
        self._data_wrapper = data_wrapper

    def serialize(self, body_value):
        return json.dumps(body_value)

    def deserialize(self, content):
        try:
            content = content.decode("utf-8")
        except AttributeError:
            pass
        return json.loads(content)

    @property
    def no_content_response(self):
        return {}
