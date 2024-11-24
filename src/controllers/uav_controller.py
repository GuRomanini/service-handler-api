from typing import List
from uuid import uuid4

from errors import UAVNotFoundByKey
from mappers import UAVMapper
from models import UAVModel, UAVServiceModel
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

    def retrieve_uavs(
        self, uav_key: str, uav_name: str, uav_status_enumerator: str, page: int, page_size: int
    ) -> List[dict]:
        uav_repository = UAVRepository(self.context)
        uav_models: List[UAVModel] = uav_repository.get_with_filters(
            page=page,
            page_size=page_size,
            uav_key=uav_key,
            uav_name=uav_name,
            uav_status_enumerator=uav_status_enumerator,
        )

        return [UAVMapper.to_dto(uav_model) for uav_model in uav_models]

    def deactivate_uav(self, uav_key: str) -> dict:
        uav_model: UAVModel = self.context.db_session.query(UAVModel).filter(UAVModel.uav_key == uav_key).first()

        if uav_model is None:
            raise UAVNotFoundByKey(extra_fields={"uav_key": uav_key})

        uav_repository = UAVRepository(context=self.context)
        uav_model.uav_status = uav_repository.get_uav_status_model_by_enumerator("inactive")

        uav_service_models: List[UAVServiceModel] = (
            self.context.db_session.query(UAVServiceModel)
            .filter(UAVServiceModel.uav_id == uav_model.id)
            .filter(UAVServiceModel.is_active == 1)
            .all()
        )

        for uav_service_model in uav_service_models:
            uav_service_model.is_active = 0

        self.context.db_session.commit()

        return UAVMapper.to_dto(uav_model)
