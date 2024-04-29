from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Product(BaseModel):
    source: str = 'ozon'
    sku: int
    title: str
    price: Decimal
    link: str
    photo_link: str | None = None
    characteristics: str | None = None
    description: str | None = None
    rating: float | None = None
    number_of_reviews: int | None = None
    description_vector: list | None = None
    characteristics_vector: list | None = None
    updated_at: datetime = datetime.now()
    created_at: datetime = datetime.now()

    def model_dump_for_update(self) -> dict:
        return self.model_dump(exclude={'source', 'sku', 'category_name', 'link', 'created_at'})
