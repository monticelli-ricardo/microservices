from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
articles = []

class Article(BaseModel):
    id: int | None = 0
    author: str
    title: str
    body: str
    created_at: datetime | None = datetime.now(timezone.utc)


@app.get("/")
def root():
    return {
        "message": "Hello World !"
    }
    
@app.get("/add")
def add(a: int, b: int):
    return {
        "result": a + b
    }
    
@app.post("/articles/")
def create_article(article: Article):
    article.id = recompute_id()
    articles.append(article)
    print("New article: ", article.id)
    return article

def recompute_id():
    return get_max_id() + 1

def get_max_id():
    if len(articles) == 0:
        return 0
    return [article.id for article in articles].sort()[-1]
    