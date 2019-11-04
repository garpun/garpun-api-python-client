import json


class Error(Exception):
    """Base error for this module."""

    pass


class HttpError(Error):
    """HTTP data was invalid or unexpected."""

    def __init__(self, resp, content, uri=None):
        self.resp = resp
        if not isinstance(content, bytes):
            raise TypeError("HTTP content should be bytes")
        self.content = content
        self.uri = uri
        self.error_details = ""

    def _get_reason(self):
        """Calculate the reason for the error from the response content."""
        reason = self.resp.reason
        try:
            data = json.loads(self.content.decode("utf-8"))
            if isinstance(data, dict):
                reason = data["error"]["message"]
                if "details" in data["error"]:
                    self.error_details = data["error"]["details"]
                elif "detail" in data["error"]:
                    self.error_details = data["error"]["detail"]
            elif isinstance(data, list) and len(data) > 0:
                first_error = data[0]
                reason = first_error["error"]["message"]
                if "details" in first_error["error"]:
                    self.error_details = first_error["error"]["details"]
        except (ValueError, KeyError, TypeError):
            pass
        if reason is None:
            reason = ""
        return reason
