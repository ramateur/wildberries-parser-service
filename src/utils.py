import logging
from time import sleep

import httpx

from src.api.exceptions import WildberriesAPIError
from src.logging import logging_level


logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)


def handle_errors(retries: int = 1, init_delay: float = 1, max_delay: float = 32, delay_factor: float = 1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            delay = init_delay
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except httpx.HTTPError as e:
                    # Handle HTTP errors (4xx and 5xx)
                    logger.error('HTTP error: %s', e)
                    exception = e
                except httpx.NetworkError as e:
                    # Handle network errors
                    logger.error('Network error: %s', e)
                    exception = e
                except WildberriesAPIError as e:
                    logger.error(e)
                    exception = e

                logger.info('Retry after %d seconds ...', delay)
                sleep(delay)
                delay = min(delay * delay_factor, max_delay)

            logger.error(
                'Maximum retries (%d) reached for method: %s\n' 'with args: %s\n' 'with kwargs: %s',
                retries,
                func.__name__,
                args,
                kwargs,
            )
            raise exception

        return wrapper

    return decorator
