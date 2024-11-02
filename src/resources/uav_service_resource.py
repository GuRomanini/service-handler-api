import falcon
from falcon import Request, Response

from controllers import UAVServiceController
from utils.schema_handler import SchemaHandler
from utils.security_tools import SecurityTools


class UAVServiceResource:
    @SchemaHandler.validate("post_uav_service.json")
    def on_post(self, req: Request, resp: Response):
        SecurityTools.validate_master_request(req)
        uav_service_controller = UAVServiceController(req.context.instance)
        response = uav_service_controller.create_by_data(uav_service_data=req.context.instance.media)

        resp.media = response
        resp.status = falcon.code_to_http_status(201)
