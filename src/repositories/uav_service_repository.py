from typing import List

from models import UAVServiceModel

from utils.context import Context
from utils.logger import Logger


class UAVServiceRepository:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context

    def get_with_filters(
        self,
        page: int,
        page_size: int,
        uav_key: str,
        service_key: str,
    ) -> List[UAVServiceModel]:
        query = self.context.db_session.query(UAVServiceModel).filter(UAVServiceModel.is_active == 1)

        if uav_key:
            query = query.filter(UAVServiceModel.uav_key == uav_key)
        if service_key:
            query = query.filter(UAVServiceModel.service_key == service_key)

        return query.order_by(UAVServiceModel.id.desc()).limit(page_size).offset((page - 1) * page_size).all()
