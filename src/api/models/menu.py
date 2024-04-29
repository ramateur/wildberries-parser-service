from pydantic import BaseModel


class ChildModel(BaseModel):
    id: int | None = None
    parent: int | None = None
    name: str | None = None
    url: str | None = None
    shard: str | None = None
    query: str | None = None
    childs: list['ChildModel'] | None = None


class CategoryModel(BaseModel):
    id: int | None = None
    name: str | None = None
    url: str | None = None
    shard: str | None = None
    query: str | None = None
    landing: bool | None = None
    childs: list[ChildModel] | None = None
