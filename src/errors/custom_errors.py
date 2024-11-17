from errors import BaseException


class UAVNotFound(BaseException):
    code = "SVH000001"

    def __init__(self, extra_fields: dict) -> None:
        title = "Not Found"
        http_status = 404
        description = "UAV not found for the given key (uav_key)."
        translation = "UAV não encontrado para a chave (uav_key) fornecida."
        super().__init__(title, self.code, http_status, description, translation, extra_fields=extra_fields)


class ServiceNotFoundByName(BaseException):
    code = "SVH000002"

    def __init__(self, extra_fields: dict) -> None:
        title = "Not Found"
        http_status = 404
        description = "No active Service found for the given name (service_name)."
        translation = "Nenhum Serviço ativo encontrado para o nome (service_name) fornecido."
        super().__init__(title, self.code, http_status, description, translation, extra_fields=extra_fields)


class ServiceNotFoundByKey(BaseException):
    code = "SVH000003"

    def __init__(self, extra_fields: dict) -> None:
        title = "Not Found"
        http_status = 404
        description = "No active Service found for the given key (service_key)."
        translation = "Nenhum Serviço ativo encontrado para a chave (service_key) fornecida."
        super().__init__(title, self.code, http_status, description, translation, extra_fields=extra_fields)


class ServiceIsNotActive(BaseException):
    code = "SVH000004"

    def __init__(self) -> None:
        title = "Bad Request"
        http_status = 400
        description = "Service is not active."
        translation = "O serviço não está ativo."
        super().__init__(title, self.code, http_status, description, translation)


class NoAvailableUAVForTheService(BaseException):
    code = "SVH000005"

    def __init__(self) -> None:
        title = "Service Unavailable"
        http_status = 503
        description = "No available UAV was found to complete this task right now. Please, try again later."
        translation = "Não foi encontrado um drone disponível para completar essa tarefa no momento. Por favor, tente novamente mais tarde."
        super().__init__(title, self.code, http_status, description, translation)


class UAVIsNotAvailable(BaseException):
    code = "SVH000006"

    def __init__(self) -> None:
        title = "Service Unavailable"
        http_status = 503
        description = "Failure while trying to contact UAV."
        translation = "Falha ao contactar o UAV."
        super().__init__(title, self.code, http_status, description, translation)


class ServiceAlreadyExists(BaseException):
    code = "SVH000007"

    def __init__(self, extra_fields: dict) -> None:
        title = "Conflict"
        http_status = 409
        description = "A Service with the given name already exists."
        translation = "Já existe um Serviço com o nome fornecido."
        super().__init__(title, self.code, http_status, description, translation, extra_fields=extra_fields)


class InvalidPagination(BaseException):
    code = "SVH000008"

    def __init__(self) -> None:
        title = "Bad Request"
        http_status = 400
        description = "Invalid integer value for page or size query string parameters."
        translation = "Valor inválido para parâmetros de página ou tamanho de página."
        super().__init__(title, self.code, http_status, description, translation)
