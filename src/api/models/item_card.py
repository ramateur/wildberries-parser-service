from pydantic import BaseModel


class Composition(BaseModel):
    name: str


class Option(BaseModel):
    name: str
    value: str
    charc_type: int | None = None
    is_variable: bool | None = None


class Color(BaseModel):
    nm_id: int


class Certificate(BaseModel):
    verified: bool | None = None


class Selling(BaseModel):
    no_return_map: int | None = None
    brand_name: str | None = None
    brand_hash: str | None = None
    supplier_id: int | None = None


class GroupedOption(BaseModel):
    group_name: str | None = None
    options: list[Option]


class ItemCard(BaseModel):
    imt_id: int | None = None
    nm_id: int | None = None
    imt_name: str | None = None
    subj_name: str | None = None
    subj_root_name: str | None = None
    vendor_code: str | None = None
    description: str | None = None
    options: list[Option]
    compositions: list[Composition] | None = None
    certificate: Certificate | None = None
    colors: list[int]
    contents: str | None = None
    full_colors: list[Color]
    selling: Selling | None = None
    media: dict | None = None
    data: dict | None = None
    grouped_options: list[GroupedOption]
