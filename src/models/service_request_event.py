from sqlalchemy import Column, ForeignKey, Integer, DateTime
from models.base import Base
from sqlalchemy.orm import relationship
from models.service_request import ServiceRequestModel
from models.service_request_status import ServiceRequestStatusModel


class ServiceRequestEventModel(Base):
    __tablename__ = "ServiceRequestEvent"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    service_request_id = Column(Integer, ForeignKey(ServiceRequestModel.id))
    service_request_status_id = Column(Integer, ForeignKey(ServiceRequestStatusModel.id))
    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")

    service_request = relationship(
        "ServiceRequestModel",
        foreign_keys=[service_request_id],
        lazy="joined",
    )
    service_request_status = relationship(
        "ServiceRequestStatusModel", foreign_keys=[service_request_status_id], lazy="joined"
    )
