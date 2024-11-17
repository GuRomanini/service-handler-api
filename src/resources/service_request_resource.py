import falcon
from falcon import Request, Response

from controllers import ServiceRequestController

from utils.pagination_handlers import (
    parse_str_page_with_validation,
    parse_str_page_size_with_validation,
    format_response_with_pagination,
)
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

    def on_get(self, req: Request, resp: Response):
        SecurityTools.validate_master_request(req)

        uav_key = req.get_param("uav_key")
        service_key = req.get_param("service_key")
        service_request_status = req.get_param("service_request_status")
        parsed_page = parse_str_page_with_validation(page=req.get_param("page"))
        parsed_page_size = parse_str_page_size_with_validation(page_size=req.get_param("page_size"))

        service_request_controller = ServiceRequestController(req.context.instance)
        response = service_request_controller.retrieve_service_requests(
            uav_key=uav_key,
            service_key=service_key,
            service_request_status_enumerator=service_request_status,
            page=parsed_page,
            page_size=parsed_page_size,
        )

        resp.status = falcon.code_to_http_status(200)
        resp.media = format_response_with_pagination(
            data=response,
            page=parsed_page,
            page_size=parsed_page_size,
        )
