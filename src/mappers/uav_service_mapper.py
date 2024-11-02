from models import UAVServiceModel


class UAVServiceMapper:
    @staticmethod
    def to_dto(model: UAVServiceModel) -> dict:
        return {
            "uav_key": model.uav.uav_key,
            "service_key": model.service.service_key,
            "base_url": model.base_url,
            "is_active": model.is_active,
        }
