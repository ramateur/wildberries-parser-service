from json import JSONDecodeError
from typing import Any

import httpx
from httpx import Response

from src.api.exceptions import WildberriesAPIError
from src.utils import handle_errors


class BaseAPI:
    def _handle_response(self, response: Response) -> dict:
        try:
            if response.status_code != 200:
                content = (
                    response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
                )
                raise WildberriesAPIError(status=response.status_code, content=content)

            return response.json()
        except JSONDecodeError:
            raise WildberriesAPIError(status=response.status_code, content=response.text)

    @handle_errors(retries=3, delay_factor=2)
    def make_request(self, url: str, endpoint: str, headers: dict, params: dict = None, response_model: Any = None):
        clean_response = self._handle_response(httpx.get(url + endpoint, params=params, headers=headers))
        if response_model:
            return response_model(**clean_response)
        return clean_response
