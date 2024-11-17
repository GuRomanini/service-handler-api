from typing import List

from models import ServiceModel, ServiceRequestModel, ServiceRequestStatusModel, UAVModel

from utils.context import Context
from utils.logger import Logger


class ServiceRequestRepository:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def get_service_request_status_model_by_enumerator(self, enumerator: str) -> ServiceRequestStatusModel:
        return (
            self.context.db_session.query(ServiceRequestStatusModel)
            .filter(ServiceRequestStatusModel.enumerator == enumerator)
            .one()
        )

    def get_with_filters(
        self,
        page: int,
        page_size: int,
        uav_key: str,
        service_key: str,
        service_request_status_enumerator: str,
    ) -> List[ServiceRequestModel]:
        query = self.context.db_session.query(ServiceRequestModel)

        if uav_key:
            uav_model = self.context.db_session.query(UAVModel).filter(UAVModel.uav_key == uav_key).first()

            query = query.filter(ServiceRequestModel.uav_service.uav == uav_model)

        if service_key:
            service_model = (
                self.context.db_session.query(ServiceModel).filter(ServiceModel.service_key == service_key).first()
            )

            query = query.filter(ServiceRequestModel.uav_service.service == service_model)

        if service_request_status_enumerator:
            query = query.filter(
                ServiceRequestModel.service_request_status
                == self.get_service_request_status_model_by_enumerator(enumerator=service_request_status_enumerator)
            )

        return query.order_by(ServiceRequestModel.id.desc()).limit(page_size).offset((page - 1) * page_size).all()
