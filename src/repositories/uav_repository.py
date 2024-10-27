from models import UAVStatusModel

from utils.context import Context
from utils.logger import Logger

class UAVRepository:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context
    
    def get_uav_status_model_by_enumerator(self, enumerator: str) -> UAVStatusModel:
        return self.context.db_session.query(UAVStatusModel).filter(UAVStatusModel.enumerator == enumerator).one()