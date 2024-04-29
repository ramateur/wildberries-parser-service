from typing import Any

from src.exceptions import BaseParserException


class WildberriesAPIError(BaseParserException):
    def __init__(self, status: int, content: Any):
        self.status = status
        self.content = content

    def __str__(self):
        return 'Error with Wildberries API\n' f'Status: {self.status}\n' f'Content: {self.content}\n'
