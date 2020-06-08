from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class Models(str, Enum):
    foo = "foo"
    bar = "bar"
    baz = "baz"


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.get("/item/{item_id}")
async def get_item_by_id(item_id: int, foo: str, q: str = None):
    return {"item_id": item_id, "foo": foo, "q": q}


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
async def get_items_in_range(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
