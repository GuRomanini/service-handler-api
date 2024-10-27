from models import ServiceStatusModel, ServiceTypeModel

from utils.context import Context
from utils.logger import Logger


class ServiceRepository:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def get_service_type_model_by_enumerator(self, enumerator: str) -> ServiceTypeModel:
        return self.context.db_session.query(ServiceTypeModel).filter(ServiceTypeModel.enumerator == enumerator).one()

    def get_service_status_model_by_enumerator(self, enumerator: str) -> ServiceStatusModel:
        return (
            self.context.db_session.query(ServiceStatusModel).filter(ServiceStatusModel.enumerator == enumerator).one()
        )
