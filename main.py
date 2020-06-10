from enum import Enum
from typing import List

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


class Models(str, Enum):
    foo = "foo"
    bar = "bar"
    baz = "baz"


class Item(BaseModel):
    name: str
    price: float
    description: str = None
    tax: float = None


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.get("/item/{item_id}")
async def get_item_by_id(item_id: int, foo: str, q: str = None):
    return {"item_id": item_id, "foo": foo, "q": q}


@app.post("/item")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        item_dict.update({"price_with_tax": item.price + item.tax})
    return item


@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item):
    item_dict = item.dict()
    item_dict["id"] = item_id
    return item_dict


@app.get("/model/{model_name}")
async def get_model_by_name(model_name: Models):
    if model_name == Models.bar:
        return {"model": model_name}
    elif model_name.value == "foo":
        return {"model": model_name}
    return {"model": model_name}


@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    # http://localhost:8000:/files//home/foo/bar.txt
    # {"file_path": "/home/foo/bar.txt"}
    return {"file_path": file_path}


@app.get("/items")
async def get_items_in_range(
        skip: int = 0,
        limit: int = 10,
        q1: str = Query(None, min_length=3, max_length=50),
        q2: List[int] = Query(None),
        q3: float = Query(None, alias="alias-item"),
):
    result = {"skip": skip, "limit": limit}
    if q1:
        result.update({"q1": q1})

    if q2:
        result.update({"q2": q2})

    if q3:
        result.update({"q3": q3})
    return result
