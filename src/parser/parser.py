import logging

from src.adapters.bert.bert import BERTAdapter
from src.adapters.elasticsearch.category_to_index_mapping import wildberries_category_id_to_es_index_mapping
from src.adapters.elasticsearch.elasticsearch import ElasticsearchAdapter
from src.adapters.elasticsearch.models.product import Product
from src.api.models.menu import ChildModel
from src.api.wildberries_api import WildberriesAPI
from src.config import settings
from src.logging import logging_level
from src.parser.utils import generate_reproducible_id
from src.utils import handle_errors


logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)


class WildberriesParser:
    def __init__(self):
        self._wb_api = WildberriesAPI()
        (
            self._sub_categories_url_to_super_id_mapping,
            self._sub_categories_info_mapping,
        ) = self.get_sub_categories_mapping()
        self._super_category_id = None
        self._es_adapter = ElasticsearchAdapter(
            host=settings.ES_HOST, port=settings.ES_PORT, user=settings.ES_USER, password=settings.ES_PASSWORD
        )
        self._bert_adapter = BERTAdapter(model_name='paraphrase-multilingual-mpnet-base-v2')

    def get_sub_categories_mapping(self):
        api_answer = self._wb_api.get_catalog_list()
        url_to_super_id_mapping = {}
        info_mapping = {}

        def map_child_to_root(child: ChildModel, root_id: int):
            """
            Рекурсивная вспомогательная функция для обхода дерева дочерних элементов.
            """
            url_to_super_id_mapping[child.url] = root_id
            info_mapping[child.url] = child
            if child.childs:
                for sub_child in child.childs:
                    map_child_to_root(sub_child, root_id)

        for category in api_answer:
            if category.childs:
                for child in category.childs:
                    map_child_to_root(child, category.id)

        return url_to_super_id_mapping, info_mapping

    def _extract_category_url(self, category_link) -> str:
        return category_link.split('https://www.wildberries.ru')[1]

    def _upload_to_es(self, product: Product):
        # index in elasticsearch
        product_id = generate_reproducible_id('ozon' + str(product.sku))
        es_index = wildberries_category_id_to_es_index_mapping.get(self.super_category_id)
        product.description_vector = self._bert_adapter.text_to_vector(
            product.description if product.description is not None else ''
        )
        product.characteristics_vector = self._bert_adapter.text_to_vector(
            product.characteristics if product.characteristics is not None else ''
        )
        self._es_adapter.upsert_document(
            index=es_index,
            id=product_id,
            document=product.model_dump(),
            document_for_update=product.model_dump_for_update(),
        )

    @handle_errors(retries=3)
    def _parse_product(self, id: int):
        response = self._wb_api.get_item_details(item_id=id)
        product = Product(
            sku=response,
            title=response,
            price=response,
            link=response,
            photo_link=response,
            characteristics=response,
            description=response,
            rating=response,
            number_of_reviews=response,
        )
        self._upload_to_es(product=product)

    def _parse_products(self, product_ids: list[int]):
        for id in product_ids:
            self._parse_product(id)

    def _parse_pages(self, shard: str, cat: str, offset_page: int, pages_count: int) -> list[int]:
        product_ids = []
        current_page = offset_page

        while True:
            logger.info(f'Processing page №{current_page} ...')
            response = self._wb_api.get_catalog_items_list(shard=shard, cat=cat, page=current_page)

            product_ids.extend(product.id for product in response.data.products)
            if pages_count is not None and (current_page - offset_page) >= pages_count:
                break

            current_page += 1

        return product_ids

    def parse_category(self, category_link: str, offset_page: int = 1, pages_count: int | None = None):
        category_url = self._extract_category_url(category_link)
        self._super_category_id = self._sub_categories_url_to_super_id_mapping.get(category_url)
        category_info = self._sub_categories_info_mapping.get(category_url)
        product_ids = self._parse_pages(
            shard=category_info.shard, cat=category_info.query, offset_page=offset_page, pages_count=pages_count
        )
        self._parse_products(product_ids)
        logger.info('Totally parsed products count: ' + str(len(product_ids)))
