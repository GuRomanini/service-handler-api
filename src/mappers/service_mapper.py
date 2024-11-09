from models import ServiceModel


class ServiceMapper:
    @staticmethod
    def to_dto(model: ServiceModel) -> dict:
        return {
            "service_key": model.service_key,
            "service_name": model.service_name,
            "service_type": model.service_type.enumerator,
            "is_active": True if model.is_active else False,
        }
