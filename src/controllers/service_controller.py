from sqlalchemy.exc import IntegrityError
from traceback import format_exc
from typing import List
from uuid import uuid4

from errors import ServiceAlreadyExists, ServiceNotFoundByKey
from mappers import ServiceMapper
from models import ServiceModel, UAVServiceModel
from repositories import ServiceRepository

from utils.context import Context
from utils.logger import Logger


class ServiceController:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def create_by_data(self, service_data: dict) -> dict:
        self.logger.info("Creating a new Service")

        service_repository = ServiceRepository(context=self.context)

        service_model = ServiceModel()
        service_model.service_key = str(uuid4())
        service_model.service_type = service_repository.get_service_type_model_by_enumerator(
            service_data["service_type"]
        )
        service_model.service_name = service_data["service_name"]
        service_model.is_active = 1

        self.context.db_session.add(service_model)

        try:
            self.context.db_session.commit()
        except IntegrityError as integrity_ex:
            if integrity_ex.orig.args[0] == 1062 and "Service.service_name" in integrity_ex.orig.args[1]:
                self.logger.error(f"Service already exists: {service_data['service_name']}")
                raise ServiceAlreadyExists(extra_fields={"service_name": service_data["service_name"]})
            else:
                _traceback = format_exc()
                self.logger.error(
                    msg="Unexpected database error",
                    message_json={"traceback": _traceback},
                )
                raise integrity_ex

        return ServiceMapper.to_dto(service_model)

    def retrieve_services(
        self, service_key: str, service_name: str, service_type_enumerator: str, page: int, page_size: int
    ) -> List[dict]:
        service_repository = ServiceRepository(self.context)
        service_models: List[ServiceModel] = service_repository.get_with_filters(
            page=page,
            page_size=page_size,
            service_key=service_key,
            service_name=service_name,
            uav_status=service_type_enumerator,
        )

        return [ServiceMapper.to_dto(service_model) for service_model in service_models]

    def deactivate_service(self, service_key: str) -> dict:
        service_model: ServiceModel = (
            self.context.db_session.query(ServiceModel).filter(ServiceModel.service_key == service_key).first()
        )

        if service_model is None:
            raise ServiceNotFoundByKey(extra_fields={"service_key": service_key})

        service_model.is_active = 0

        uav_service_models: List[UAVServiceModel] = (
            self.context.db_session.query(UAVServiceModel)
            .filter(UAVServiceModel.service_id == service_model.id)
            .filter(UAVServiceModel.is_active == 1)
            .all()
        )

        for uav_service_model in uav_service_models:
            uav_service_model.is_active = 0

        self.context.db_session.commit()

        return ServiceMapper.to_dto(service_model)
