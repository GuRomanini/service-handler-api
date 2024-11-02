from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from models.service_status import ServiceStatusModel
from models.service_type import ServiceTypeModel


class ServiceModel(Base):
    __tablename__ = "Service"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    service_key = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    service_type_id = Column(Integer, ForeignKey(ServiceTypeModel.id), nullable=False)
    service_status_id = Column(Integer, ForeignKey(ServiceStatusModel.id), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")

    service_type: ServiceTypeModel = relationship("ServiceTypeModel", foreign_keys=[service_type_id], lazy="joined")

    service_status: ServiceStatusModel = relationship(
        "ServiceStatusModel", foreign_keys=[service_status_id], lazy="joined"
    )
