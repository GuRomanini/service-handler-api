from uuid import uuid4

from errors import ServiceNotFound, UAVNotFound
from mappers import UAVServiceMapper
from models import ServiceModel, UAVModel, UAVServiceModel
from repositories import ServiceRepository

from utils.context import Context
from utils.logger import Logger


class UAVServiceController:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def create_by_data(self, uav_service_data: dict) -> dict:
        self.logger.debug("Creating a new UAVService")

        uav_model = self.context.db_session.query(UAVModel).filter(UAVModel.uav_key == uav_service_data["uav_key"]).first()

        if uav_model is None:
            raise UAVNotFound(extra_fields={"uav_key": uav_service_data["uav_key"]})

        service_repository = ServiceRepository(context=self.context)

        active_service_status = service_repository.get_service_status_model_by_enumerator("active")

        service_model: ServiceModel = self.context.db_session.query(ServiceModel).filter(ServiceModel.service_name == uav_service_data["service_name"]).filter(ServiceModel.service_status == active_service_status).one()

        if uav_model is None:
            raise ServiceNotFound(extra_fields={"service_name": uav_service_data["service_name"]})

        uav_service_model = UAVServiceModel()
        uav_service_model.uav = uav_model
        uav_service_model.service = service_model
        uav_service_model.base_url = uav_service_data["base_url"]

        self.context.db_session.add(uav_service_model)
        self.context.db_session.commit()

        return UAVServiceMapper.to_dto(uav_service_model)
