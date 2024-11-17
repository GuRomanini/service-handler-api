from typing import List
from uuid import uuid4

from errors import ServiceNotFoundByName, UAVNotFound
from mappers import UAVServiceMapper
from models import ServiceModel, UAVModel, UAVServiceModel
from repositories import UAVServiceRepository

from utils.context import Context
from utils.logger import Logger


class UAVServiceController:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def create_by_data(self, uav_service_data: dict) -> dict:
        self.logger.info("Creating a new UAVService")

        uav_model: UAVModel = (
            self.context.db_session.query(UAVModel).filter(UAVModel.uav_key == uav_service_data["uav_key"]).first()
        )

        if uav_model is None:
            raise UAVNotFound(extra_fields={"uav_key": uav_service_data["uav_key"]})

        service_model: ServiceModel = (
            self.context.db_session.query(ServiceModel)
            .filter(ServiceModel.service_name == uav_service_data["service_name"])
            .filter(ServiceModel.is_active == 1)
            .one()
        )

        if uav_model is None:
            raise ServiceNotFoundByName(extra_fields={"service_name": uav_service_data["service_name"]})

        uav_service_model = UAVServiceModel()
        uav_service_model.uav_service_key = str(uuid4())
        uav_service_model.uav_key = uav_model.uav_key
        uav_service_model.service_key = service_model.service_key
        uav_service_model.uav = uav_model
        uav_service_model.service = service_model
        uav_service_model.base_url = uav_service_data["base_url"]
        uav_service_model.is_active = 1

        self.context.db_session.add(uav_service_model)
        self.context.db_session.commit()

        return UAVServiceMapper.to_dto(uav_service_model)

    def retrieve_uav_services(self, uav_key: str, service_key: str, page: int, page_size: int) -> List[dict]:
        uav_service_repository = UAVServiceRepository(self.context)
        uav_service_models: List[UAVModel] = uav_service_repository.get_with_filters(
            page=page,
            page_size=page_size,
            uav_key=uav_key,
            service_key=service_key,
        )

        return [UAVServiceMapper.to_dto(uav_service_model) for uav_service_model in uav_service_models]
