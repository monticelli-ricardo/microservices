import os
from datetime import datetime, timezone
from urllib.parse import quote_plus
from dataclasses import dataclass


from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine, Session, select, update, delete

# Load dotenv module
load_dotenv()

# Declare global vatiable
app = FastAPI()
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
CONNECTION_STRING = f"mysql+mysqlconnector://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}@localhost/{MYSQL_DATABASE}"
myblog_db = create_engine(CONNECTION_STRING)


# Article class
@dataclass
class Article(SQLModel, table =True):
    __tablename__="articles"
    id: int | None = Field(default=None, primary_key=True)
    author: str
    title: str
    body: str | None = Field(default=None)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))

# API Operations
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
    # Create a session to the DB
    session = Session(myblog_db)
    # then add the article
    session.add(article)
    # Commit the session
    session.commit()
    # Refresh Session
    session.refresh(article)

    print("New article: ", article.id)
    return article

@app.get("/articles", response_model=list[Article])
def list_articles():
    with Session(myblog_db) as session:
        statement = select(Article)
        print(statement)
        return session.exec(statement)
    