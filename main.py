import os
from urllib.parse import quote_plus
from datetime import datetime, timezone
from dataclasses import dataclass

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine, Session, select

load_dotenv()

app = FastAPI()
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

CONNECTION_STRING = f"mysql+mysqlconnector://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}@localhost/{MYSQL_DATABASE}"
myblog_db = create_engine(CONNECTION_STRING)


@dataclass
class Article(SQLModel, table=True):
    __tablename__="articles"
    id: int | None = Field(default=None, primary_key=True)
    author: str
    title: str
    body: str | None = Field(default=None)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))


class ArticleUpdate(SQLModel):
    author: str | None = None
    title: str | None = None
    body: str | None = None


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
    
@app.post("/articles/",
          description="""
Create a new article

Args:
- article (Article): Required fields are `author` and `title`

Returns:
- Article: The created article
          """)
def create_article(article: Article):
    # Create a session with the database
    # Add the article to the session: article in memory but not in the DB
    # Commit the session: The article is in the DB
    # Refresh session
    session = Session(myblog_db)
    session.add(article)
    session.commit()
    session.refresh(article)
    print("New article: ", article.id)
    return article

@app.get("/articles", response_model=list[Article])
def list_articles():
    with Session(myblog_db) as session:
        # select * from articles ==> Class Article
        statement = select(Article)
        print(statement)
        articles = session.exec(statement).all()
        return articles
        

@app.get("/articles/{article_id}",
         response_model=Article)
def get_article(article_id: int):
    with Session(myblog_db) as session:
        article = session.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    
@app.delete("/articles/{article_id}")
def delete_article(article_id: int):
    with Session(myblog_db) as session:
        article = session.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        session.delete(article)
        session.commit()
        return {
            "deleted": True
        }
        
# @app.put("/articles/") ==> need all the fields the object in one shot
@app.patch("/articles/{article_id}", # will update some fields of the object
           response_model=Article)
def update_article(article_id: int, article: ArticleUpdate):
    with Session(myblog_db) as session:
        # Get the article from the database
        article_db = session.get(Article, article_id)
        
        # Check if it is found
        if not article_db:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Map the update data with the fields from the database
        article_data = article.model_dump(exclude_unset=True)
        
        # Effectively Update the article from the database
        article_db.sqlmodel_update(article_data)
        
        # Mark this article as "Updatable"
        session.add(article_db)
        
        # Commit the update to the database
        session.commit()
        
        # Refresh the instance of the article of the session from the db
        session.refresh(article_db)
        
        # Return it.
        return article_db
    