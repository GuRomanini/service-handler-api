import falcon
from falcon import HTTPError
import traceback
import json

from errors import BaseException, MethodNotAllowed, InternalError
from utils.logger import Logger


class APIErrorHandler:
    @staticmethod
    def uaas_exception(req, resp, ex, params):
        raise FalconBaseException(ex)

    @staticmethod
    def method_not_allowed(*args):
        raise FalconBaseException(MethodNotAllowed())

    @staticmethod
    def unexpected(req, *args):
        stack_trace_limit = 10
        logger = Logger(req.context.instance, __name__)
        _traceback = traceback.format_exc(stack_trace_limit)
        logger.fatal(_traceback)
        raise FalconBaseException(InternalError())


class FalconBaseException(HTTPError):
    def __init__(self, rsfn_exception: BaseException):
        HTTPError.__init__(self, getattr(falcon, f"HTTP_{str(rsfn_exception.http_status)}"))
        self.title = rsfn_exception.title
        self.description = rsfn_exception.description
        self.translation = rsfn_exception.translation
        self.code = rsfn_exception.code

    def to_dict(self):
        obj = dict()
        obj["title"] = self.title
        obj["description"] = self.description
        obj["translation"] = self.translation
        obj["code"] = self.code

        if self.link is not None:
            obj["link"] = self.link

        return obj

    def to_json(self, *args):
        obj = self.to_dict()
        json_str = json.dumps(obj, ensure_ascii=False)
        return str.encode(json_str)
