from sqlalchemy import Column, Integer, String, DateTime
from models.base import Base


class UAVStatusModel(Base):
    __tablename__ = "UAVStatus"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    enumerator = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")
