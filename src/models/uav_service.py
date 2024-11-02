from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from models.service import ServiceModel
from models.uav import UAVModel


class UAVServiceModel(Base):
    __tablename__ = "UAVService"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    uav_id = Column(Integer, ForeignKey(UAVModel.id), nullable=False)
    service_id = Column(Integer, ForeignKey(ServiceModel.id), nullable=False)
    base_url = Column(String)

    uav: UAVModel = relationship("UAVModel", foreign_keys=[uav_id], lazy="selectin")
    service: ServiceModel = relationship("ServiceModel", foreign_keys=[service_id], lazy="selectin")

    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")
