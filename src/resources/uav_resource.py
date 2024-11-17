import falcon
from falcon import Request, Response

from controllers import UAVController

from utils.pagination_handlers import (
    parse_str_page_with_validation,
    parse_str_page_size_with_validation,
    format_response_with_pagination,
)
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

    def on_get(self, req: Request, resp: Response):
        SecurityTools.validate_master_request(req)

        uav_key = req.get_param("uav_key")
        uav_name = req.get_param("uav_name")
        uav_status = req.get_param("uav_status")
        parsed_page = parse_str_page_with_validation(page=req.get_param("page"))
        parsed_page_size = parse_str_page_size_with_validation(page_size=req.get_param("page_size"))

        uav_controller = UAVController(req.context.instance)
        response = uav_controller.retrieve_uavs(
            uav_key=uav_key,
            uav_name=uav_name,
            uav_status_enumerator=uav_status,
            page=parsed_page,
            page_size=parsed_page_size,
        )

        resp.status = falcon.code_to_http_status(200)
        resp.media = format_response_with_pagination(
            data=response,
            page=parsed_page,
            page_size=parsed_page_size,
        )

    def on_patch_deactivate(self, req: Request, resp: Response, uav_key: str):
        SecurityTools.validate_master_request(req)

        uav_controller = UAVController(req.context.instance)
        response = uav_controller.deactivate_uav(uav_key)

        resp.media = response
        resp.status = falcon.code_to_http_status(200)
