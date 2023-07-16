from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import topics

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/topics/{id}")
def find_topic_detail(id: int):
    return topics.find_detail(id)

class SearchBody(BaseModel):
    keyword: str
    history: List[str]

@app.post("/search")
def search_topics(body: SearchBody):
    result = topics.search(body.keyword, body.history)
    return result
