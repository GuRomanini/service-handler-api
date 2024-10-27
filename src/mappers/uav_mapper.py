from models import UAVModel


class UAVMapper:
    @staticmethod
    def to_dto(model: UAVModel) -> dict:
        return {
            "uav_key": model.uav_key,
            "uav_name": model.uav_name,
            "uav_status": model.uav_status.enumerator,
        }
