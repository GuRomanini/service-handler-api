from utils.context import Context
from utils.logger import Logger


class ServiceRequestController:
    def __init__(self, context: Context) -> None:
        self.logger = Logger(context, __name__)
        self.context = context
