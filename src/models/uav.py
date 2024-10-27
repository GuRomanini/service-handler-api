from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from models.uav_status import UAVStatusModel


class UAVModel(Base):
    __tablename__ = "UAV"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    uav_key = Column(String, nullable=False)
    uav_name = Column(String, nullable=False)
    uav_status_id = Column(Integer, ForeignKey(UAVStatusModel.id), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")


    uav_status: UAVStatusModel = relationship(
        "UAVStatusModel", foreign_keys=[uav_status_id], lazy="joined"
    )
