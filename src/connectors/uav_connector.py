from utils.context import Context
from connectors.rest_connector import BaseConnectorException, BaseConnectorResponse, RestConnector


class UAVConnector(RestConnector):
    def __init__(self, context: Context, base_url: str) -> None:
        super().__init__(context, __name__, base_url=base_url, timeout=60)

    def request_service(self, service_key: str) -> dict:
        response: BaseConnectorResponse = self.send(
            endpoint="/request", method="POST", payload={"service_key": service_key}, headers={"roles": "master"}
        )

        if response.response_status != 200:
            raise BaseConnectorException(response)

        return response.response_json
