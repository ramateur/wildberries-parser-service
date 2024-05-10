from src.api.base import BaseAPI
from src.api.models.category_items import CategoryItemsResponseModel
from src.api.models.item_card import ItemCard
from src.api.models.item_details import ItemDetailsResponseModel
from src.api.models.item_reviews import ItemReview
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

    def get_catalog_items_list(self, shard: str, cat: str, page: int) -> CategoryItemsResponseModel:
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
            response_model=CategoryItemsResponseModel,
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

    def _get_server_url(self, item_id: int) -> str:
        _short_id = item_id // 100000
        if 0 <= _short_id <= 143:
            basket = '01'
        elif 144 <= _short_id <= 287:
            basket = '02'
        elif 288 <= _short_id <= 431:
            basket = '03'
        elif 432 <= _short_id <= 719:
            basket = '04'
        elif 720 <= _short_id <= 1007:
            basket = '05'
        elif 1008 <= _short_id <= 1061:
            basket = '06'
        elif 1062 <= _short_id <= 1115:
            basket = '07'
        elif 1116 <= _short_id <= 1169:
            basket = '08'
        elif 1170 <= _short_id <= 1313:
            basket = '09'
        elif 1314 <= _short_id <= 1601:
            basket = '10'
        elif 1602 <= _short_id <= 1655:
            basket = '11'
        elif 1656 <= _short_id <= 1919:
            basket = '12'
        elif 1920 <= _short_id <= 2045:
            basket = '13'
        elif 2046 <= _short_id <= 2189:
            basket = '14'
        elif 2190 <= _short_id <= 2405:
            basket = '15'
        else:
            basket = '16'

        return f'https://basket-{basket}.wbbasket.ru/vol{_short_id}/part{item_id // 1000}/{item_id}'

    def get_item_image(self, item_id: int) -> str:
        return f'{self._get_server_url(item_id)}/images/big/1.jpg'

    def get_item_card(self, item_id: int) -> ItemCard:
        url = self._get_server_url(item_id)
        endpoint = '/info/ru/card.json'
        raw_response = self.make_request(url=url, endpoint=endpoint, headers=self.COMMON_HEADERS)

        return ItemCard(**raw_response)

    def get_item_reviews(self, item_id: int) -> ItemReview:
        url = 'https://feedbacks2.wb.ru'
        endpoint = f'/feedbacks/v1/{item_id}'
        raw_response = self.make_request(url=url, endpoint=endpoint, headers=self.COMMON_HEADERS)

        return ItemReview(**raw_response)
