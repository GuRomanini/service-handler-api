from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from models.service_request_status import ServiceRequestStatusModel
from models.uav_service import UAVServiceModel


class ServiceRequestModel(Base):
    __tablename__ = "ServiceRequest"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    service_request_key = Column(String, nullable=False, unique=True)
    uav_service_id = Column(Integer, ForeignKey(UAVServiceModel.id), nullable=False)
    service_request_status_id = Column(Integer, ForeignKey(ServiceRequestStatusModel.id))
    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")

    uav_service = UAVServiceModel = relationship("UAVServiceModel", foreign_keys=[uav_service_id], lazy="selectin")
    service_request_status: ServiceRequestStatusModel = relationship(
        "ServiceRequestStatusModel", foreign_keys=[service_request_status_id], lazy="joined"
    )
    events = relationship(
        "ServiceRequestEventModel",
        back_populates="service_request",
        order_by="asc(ServiceRequestEventModel.created_at)",
    )
