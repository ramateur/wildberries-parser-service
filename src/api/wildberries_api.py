from src.api.base import BaseAPI
from src.api.models.catalog import CatalogResponseModel
from src.api.models.item_details import ItemDetailsResponseModel
from src.api.models.menu import CategoryModel


class WildberriesAPI(BaseAPI):
    COMMON_HEADERS = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/'
        '537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    def get_catalog_list(self) -> list[CategoryModel]:
        url = 'https://static-basket-01.wbbasket.ru/'
        endpoint = 'vol0/data/main-menu-ru-ru-v2.json'
        raw_response = self.make_request(url=url, endpoint=endpoint, headers=self.COMMON_HEADERS)
        return [CategoryModel(**item) for item in raw_response]

    def get_catalog_items_list(self, shard: str, cat: str, page: int) -> CatalogResponseModel:
        url = 'https://catalog.wb.ru/'
        endpoint = f'catalog/{shard}/v2/catalog'
        if '&' in cat:
            cat = cat.split('&')
            wbsize = cat[1].split('=')[1]
            cat = cat[0].split('=')[1]
            query = {
                'appType': '1',
                'curr': 'rub',
                'dest': '-1257786',
                'cat': cat,
                'wbsize': wbsize,
                'page': page,
                'spp': '30',
                'sort': 'popular',
            }
        else:
            query = {
                'appType': '1',
                'curr': 'rub',
                'dest': '-1257786',
                'cat': cat.split('=')[1],
                'page': page,
                'spp': '30',
                'sort': 'popular',
            }
        return self.make_request(
            response_model=CatalogResponseModel,
            url=url,
            endpoint=endpoint,
            params=query,
            headers=self.COMMON_HEADERS,
        )

    def get_item_details(self, item_id: int) -> ItemDetailsResponseModel:
        url = 'https://card.wb.ru/'
        endpoint = 'cards/v2/detail'
        query = {'appType': '1', 'curr': 'rub', 'dest': '-1257786', 'spp': '30', 'nm': item_id}
        return self.make_request(
            response_model=ItemDetailsResponseModel,
            url=url,
            endpoint=endpoint,
            params=query,
            headers=self.COMMON_HEADERS,
        )
