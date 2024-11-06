from uuid import uuid4

from mappers import UAVMapper
from models import UAVModel
from repositories import UAVRepository

from utils.context import Context
from utils.logger import Logger


class UAVController:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def create_by_data(self, uav_data: dict) -> dict:
        self.logger.info("Registering a new UAV")

        uav_repository = UAVRepository(context=self.context)

        uav_model = UAVModel()
        uav_model.uav_key = str(uuid4())
        uav_model.uav_status = uav_repository.get_uav_status_model_by_enumerator("ready")
        uav_model.uav_name = uav_data["uav_name"]

        self.context.db_session.add(uav_model)
        self.context.db_session.commit()

        return UAVMapper.to_dto(uav_model)
