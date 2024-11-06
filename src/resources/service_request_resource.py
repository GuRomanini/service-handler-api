import falcon
from falcon import Request, Response

from controllers import ServiceRequestController

from utils.schema_handler import SchemaHandler
from utils.security_tools import SecurityTools


class ServiceRequestResource:
    @SchemaHandler.validate("post_service_request.json")
    def on_post(self, req: Request, resp: Response):
        SecurityTools.validate_master_request(req)
        service_request_controller = ServiceRequestController(req.context.instance)
        response = service_request_controller.create_by_data_and_forward_to_uav(
            service_request_data=req.context.instance.media
        )

        resp.media = response
        resp.status = falcon.code_to_http_status(201)
