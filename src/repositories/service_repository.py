from typing import List

from models import ServiceModel, ServiceTypeModel

from utils.context import Context
from utils.logger import Logger


class ServiceRepository:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def get_service_type_model_by_enumerator(self, enumerator: str) -> ServiceTypeModel:
        return self.context.db_session.query(ServiceTypeModel).filter(ServiceTypeModel.enumerator == enumerator).one()

    def get_with_filters(
        self,
        page: int,
        page_size: int,
        service_key: str,
        service_name: str,
        service_type_enumerator: str,
    ) -> List[ServiceModel]:
        query = self.context.db_session.query(ServiceModel).filter(ServiceModel.is_active == 1)

        if service_key:
            query = query.filter(ServiceModel.service_key == service_key)
        if service_name:
            query = query.filter(ServiceModel.service_name == service_name)
        if service_type_enumerator:
            query = query.filter(
                ServiceModel.uav_status == self.get_service_type_model_by_enumerator(enumerator=service_type_enumerator)
            )

        return query.order_by(ServiceModel.id.desc()).limit(page_size).offset((page - 1) * page_size).all()
