from models import ServiceRequestModel


class ServiceRequestMapper:
    @staticmethod
    def to_dto(model: ServiceRequestModel) -> dict:
        return {
            "service_request_key": model.service_request_key,
            "service_request_status": model.service_request_status.enumerator,
            "uav_key": model.uav_service.uav_key,
            "service_key": model.uav_service.service_key,
        }
