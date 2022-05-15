import json
from enum import IntEnum


class ResponseCode(IntEnum):
    OK = 0

    PERMISSION_DENIED = 301
    BAD_REQUEST = 302
    INTERNAL_SERVER_ERROR = 502
    NOT_FOUND = 404


class BaseResponse:
    def __init__(self, code, msg, **kwargs):
        self.data = {"code": code, "msg": msg}
        self.data.update(kwargs)

    def set_results(self, results):
        self.data["results"] = results

    def to_json(self):
        return json.dumps(self.data, default=str, ensure_ascii=False)

    def __str__(self):
        return self.to_json()
