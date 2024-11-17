import falcon
from falcon import Request, Response

from controllers import ServiceController

from utils.pagination_handlers import (
    parse_str_page_with_validation,
    parse_str_page_size_with_validation,
    format_response_with_pagination,
)
from utils.schema_handler import SchemaHandler
from utils.security_tools import SecurityTools


class ServiceResource:
    @SchemaHandler.validate("post_service.json")
    def on_post(self, req: Request, resp: Response):
        SecurityTools.validate_master_request(req)
        service_controller = ServiceController(req.context.instance)
        response = service_controller.create_by_data(service_data=req.context.instance.media)

        resp.media = response
        resp.status = falcon.code_to_http_status(201)

    def on_get(self, req: Request, resp: Response):
        SecurityTools.validate_master_request(req)

        service_key = req.get_param("service_key")
        service_name = req.get_param("service_name")
        service_type = req.get_param("service_type")
        parsed_page = parse_str_page_with_validation(page=req.get_param("page"))
        parsed_page_size = parse_str_page_size_with_validation(page_size=req.get_param("page_size"))

        service_controller = ServiceController(req.context.instance)
        response = service_controller.retrieve_services(
            service_key=service_key,
            service_name=service_name,
            service_type_enumerator=service_type,
            page=parsed_page,
            page_size=parsed_page_size,
        )

        resp.status = falcon.code_to_http_status(200)
        resp.media = format_response_with_pagination(
            data=response,
            page=parsed_page,
            page_size=parsed_page_size,
        )

    def on_patch_deactivate(self, req: Request, resp: Response, service_key: str):
        SecurityTools.validate_master_request(req)

        service_controller = ServiceController(req.context.instance)
        response = service_controller.deactivate_service(service_key)

        resp.media = response
        resp.status = falcon.code_to_http_status(200)
