from errors import BaseException


class UAVNotFound(BaseException):
    code = "SVH000001"

    def __init__(self, extra_fields: dict) -> None:
        title = "Not Found"
        http_status = 404
        description = "UAV not found for the given key (uav_key)."
        translation = "UAV não encontrado para a chave (uav_key) fornecida."
        super().__init__(title, self.code, http_status, description, translation, extra_fields=extra_fields)


class ServiceNotFound(BaseException):
    code = "SVH000002"

    def __init__(self, extra_fields: dict) -> None:
        title = "Not Found"
        http_status = 404
        description = "No active Service found for the given name (service_name)."
        translation = "Nenhum Serviço ativo encontrado para o nome (service_name) fornecido."
        super().__init__(title, self.code, http_status, description, translation, extra_fields=extra_fields)
