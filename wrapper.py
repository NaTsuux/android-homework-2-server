import logging
import traceback
from functools import wraps
from http.client import INTERNAL_SERVER_ERROR

from flask import request

from RequestError import RequestError
from response import BaseResponse, ResponseCode


def catch_and_respond(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.debug('Request data is [{}]'.format(
                request.get_data().decode(encoding="UTF-8")
            ))
            ret = func(*args, **kwargs)
            return ret
        except RequestError as exc:
            logging.error('RequestError: {}\n'.format(traceback.format_exc()))
            return BaseResponse(exc.code, exc.message).to_json(), exc.http_code
        except Exception as exc:
            logging.error('Exception {}: {}\n'.format(exc.__class__, traceback.format_exc()))
            result = BaseResponse(ResponseCode.INTERNAL_SERVER_ERROR,
                                  "Error {}: {}".format(exc.__class__, traceback.format_exc()))
            return result.to_json(), INTERNAL_SERVER_ERROR

    return wrapper
