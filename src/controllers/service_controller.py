from uuid import uuid4

from mappers import ServiceMapper
from models import ServiceModel
from repositories import ServiceRepository

from utils.context import Context
from utils.logger import Logger


class ServiceController:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def create_by_data(self, service_data: dict) -> dict:
        self.logger.debug("Creating a new Service")

        service_repository = ServiceRepository(context=self.context)

        service_model = ServiceModel()
        service_model.service_key = str(uuid4())
        service_model.service_type = service_repository.get_service_type_model_by_enumerator(
            service_data["service_type"]
        )
        service_model.service_name = service_data["service_name"]
        service_model.is_active = 1

        self.context.db_session.add(service_model)
        self.context.db_session.commit()

        return ServiceMapper.to_dto(service_model)
