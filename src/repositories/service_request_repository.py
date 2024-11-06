from models import ServiceRequestStatusModel

from utils.context import Context
from utils.logger import Logger


class ServiceRequestRepository:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def get_service_request_status_model_by_enumerator(self, enumerator: str) -> ServiceRequestStatusModel:
        return self.context.db_session.query(ServiceRequestStatusModel).filter(ServiceRequestStatusModel.enumerator == enumerator).one()
