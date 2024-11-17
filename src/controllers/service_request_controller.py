from typing import List
from uuid import uuid4

from connectors import UAVConnector
from errors import NoAvailableUAVForTheService, ServiceIsNotActive, ServiceNotFoundByKey, UAVIsNotAvailable
from mappers import ServiceRequestMapper
from models import ServiceModel, ServiceRequestModel, UAVModel, UAVServiceModel
from repositories import ServiceRequestRepository, UAVRepository

from utils.context import Context
from utils.logger import Logger


class ServiceRequestController:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def create_by_data_and_forward_to_uav(self, service_request_data: dict) -> dict:
        self.logger.info("Creating Service Request")

        service_model: ServiceModel = (
            self.context.db_session.query(ServiceModel)
            .filter(ServiceModel.service_key == service_request_data["service_key"])
            .first()
        )

        if service_model is None:
            raise ServiceNotFoundByKey(extra_fields={"service_key": service_request_data["service_key"]})

        if service_model.is_active == 0:
            raise ServiceIsNotActive()

        service_request_repository = ServiceRequestRepository(context=self.context)
        uav_repository = UAVRepository(context=self.context)

        service_request_model = ServiceRequestModel()
        service_request_model.service_request_key = str(uuid4())

        ready_uav_status_model = uav_repository.get_uav_status_model_by_enumerator("ready")

        ready_uavs = (
            self.context.db_session.query(UAVModel.id).filter(UAVModel.uav_status == ready_uav_status_model).all()
        )
        uavs_id_list = [uav[0] for uav in ready_uavs]

        uav_service_model: UAVServiceModel = (
            self.context.db_session.query(UAVServiceModel)
            .filter(UAVServiceModel.is_active == 1)
            .filter(UAVServiceModel.uav_id.in_(uavs_id_list))
            .first()
        )

        if uav_service_model is None:
            raise NoAvailableUAVForTheService()

        service_request_model.uav_service = uav_service_model

        self.logger.info("Forwarding Service Request to UAV")
        try:
            uav_connector = UAVConnector(context=self.context, base_url=uav_service_model.base_url)
            uav_connector.request_service(service_key=uav_service_model.service_key)
        except Exception:
            self.logger.error("Failure while trying to connect with the UAV.")
            raise UAVIsNotAvailable()

        service_request_model.service_request_status = (
            service_request_repository.get_service_request_status_model_by_enumerator("completed")
        )

        self.context.db_session.add(service_request_model)
        self.context.db_session.commit()

        return ServiceRequestMapper.to_dto(service_request_model)

    def retrieve_service_requests(
        self, uav_key: str, service_key: str, service_request_status_enumerator: str, page: int, page_size: int
    ) -> List[dict]:
        service_request_repository = ServiceRequestRepository(self.context)
        service_request_models: List[ServiceRequestModel] = service_request_repository.get_with_filters(
            page=page,
            page_size=page_size,
            uav_key=uav_key,
            service_key=service_key,
            service_request_status_enumerator=service_request_status_enumerator,
        )

        return [ServiceRequestMapper.to_dto(service_request_model) for service_request_model in service_request_models]
