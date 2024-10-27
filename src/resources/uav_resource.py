import falcon
from falcon import Request, Response

from controllers import UAVController
from utils.schema_handler import SchemaHandler
from utils.security_tools import SecurityTools


class UAVResource:
    @SchemaHandler.validate("post_uav.json")
    def on_post(self, req: Request, resp: Response):
        SecurityTools.validate_master_request(req)
        uav_controller = UAVController(req.context.instance)
        response = uav_controller.create_by_data(uav_data=req.context.instance.media)

        resp.media = response
        resp.status = falcon.code_to_http_status(201)
