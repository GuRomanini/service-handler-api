import falcon
from falcon import Request, Response

from controllers import UAVServiceController

from utils.pagination_handlers import (
    parse_str_page_with_validation,
    parse_str_page_size_with_validation,
    format_response_with_pagination,
)
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

    def on_get(self, req: Request, resp: Response):
        SecurityTools.validate_master_request(req)

        uav_key = req.get_param("uav_key")
        service_key = req.get_param("service_key")
        parsed_page = parse_str_page_with_validation(page=req.get_param("page"))
        parsed_page_size = parse_str_page_size_with_validation(page_size=req.get_param("page_size"))

        uav_service_controller = UAVServiceController(req.context.instance)
        response = uav_service_controller.retrieve_uav_services(
            uav_key=uav_key,
            service_key=service_key,
            page=parsed_page,
            page_size=parsed_page_size,
        )

        resp.status = falcon.code_to_http_status(200)
        resp.media = format_response_with_pagination(
            data=response,
            page=parsed_page,
            page_size=parsed_page_size,
        )
