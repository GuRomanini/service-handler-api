from typing import List

from models import UAVModel, UAVStatusModel

from utils.context import Context
from utils.logger import Logger


class UAVRepository:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def get_uav_status_model_by_enumerator(self, enumerator: str) -> UAVStatusModel:
        return self.context.db_session.query(UAVStatusModel).filter(UAVStatusModel.enumerator == enumerator).one()

    def get_with_filters(
        self,
        page: int,
        page_size: int,
        uav_key: str,
        uav_name: str,
        uav_status_enumerator: str,
    ) -> List[UAVModel]:
        query = self.context.db_session.query(UAVModel)

        if uav_key:
            query = query.filter(UAVModel.uav_key == uav_key)
        if uav_name:
            query = query.filter(UAVModel.uav_name == uav_name)
        if uav_status_enumerator:
            query = query.filter(
                UAVModel.uav_status == self.get_uav_status_model_by_enumerator(enumerator=uav_status_enumerator)
            )

        return query.order_by(UAVModel.id.desc()).limit(page_size).offset((page - 1) * page_size).all()
