from pydantic import BaseModel


class PriceModel(BaseModel):
    basic: int | None = None
    product: int | None = None
    total: int | None = None
    logistics: int | None = None


class SizeModel(BaseModel):
    name: str | None = None
    origName: str | None = None
    rank: int | None = None
    optionId: int | None = None
    wh: int | None = None
    dtype: int | None = None
    price: PriceModel | None = None
    saleConditions: int | None = None
    payload: str | None = None


class ProductModel(BaseModel):
    __sort: int | None = None
    ksort: int | None = None
    time1: int | None = None
    time2: int | None = None
    wh: int | None = None
    dtype: int | None = None
    dist: int | None = None
    id: int | None = None
    root: int | None = None
    kindId: int | None = None
    brand: str | None = None
    brandId: int | None = None
    siteBrandId: int | None = None
    colors: list | None = None
    subjectId: int | None = None
    subjectParentId: int | None = None
    name: str | None = None
    supplier: str | None = None
    supplierId: int | None = None
    supplierRating: float | None = None
    supplierFlags: int | None = None
    pics: int | None = None
    rating: int | None = None
    reviewRating: float | None = None
    feedbacks: int | None = None
    panelPromoId: int | None = None
    promoTextCard: str | None = None
    promoTextCat: str | None = None
    volume: int | None = None
    viewFlags: int | None = None
    sizes: list[SizeModel] | None = None
    log: dict | None = None


class ProductListModel(BaseModel):
    total: int
    products: list[ProductModel]


class CatalogResponseModel(BaseModel):
    state: int
    version: int
    payloadVersion: int
    data: ProductListModel
