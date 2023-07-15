from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/topics")
def find_topic_items(search: Union[str, None] = None):
    return {"item_id": search}

@app.get("/topics/{title}")
def find_topic_detail_by_title(title: str):
    print(title)
    return {}
