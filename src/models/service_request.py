from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.service_request_status import ServiceRequestStatusModel


class ServiceRequestModel(Base):
    __tablename__ = "ServiceRequest"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    service_request_key = Column(String)
    requester_key = Column(String)
    service_request_status_id = Column(Integer, ForeignKey(ServiceRequestStatusModel.id))

    service_request_status = relationship(
        "ServiceRequestStatusModel", foreign_keys=[service_request_status_id], lazy="joined"
    )
