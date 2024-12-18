import os
from datetime import datetime, timezone
from urllib.parse import quote_plus
from dataclasses import dataclass


from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
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

class ArticleUpdate(SQLModel):
    author: str | None
    title: str | None
    body: str | None

# Comment class
@dataclass
class Comment(SQLModel, table= True):
    __tablename__="comments"
    id: int | None = Field(default=None, primary_key=True)
    article_id: int | None = Field(default=None)
    author: str 
    body: str | None = Field(default=None)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))

class CommentUpdate(SQLModel):
    author: str | None
    title: str | None
    body: str | None

# API Operations
@app.get("/")
def root():
    return {
        "message": "Simple Blogging System!"
    }
    
# Article APIs    
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
        # The `session.exec(statement)` fetches results from the database as a SQLAlchemy object which is not JSON-serializable, 
        # so `.all()`` converts the query results into a list of Article objects, compatible with the `response_model` definition.
        articles = session.exec(statement).all()
        return articles
    
@app.get("/articles/{article_id}", 
         response_model=Article,
         )
def get_article(article_id: int):
    with Session(myblog_db) as session:
        article = session.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article

@app.delete("/articles/{article_id}")
def delete_article(article_id):
    with Session(myblog_db) as session:
        article = session.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        session.delete(article)
        session.commit()
        return {
            "deleted": True
        }

# @app.put("/articles") ==> need all the fieds object in one shot
@app.patch("/articles/{articles_id}") # Will update some fields of the object
def update_article(article_id: int, article: ArticleUpdate):
    with Session(myblog_db) as session:
        # Get the article from database
        article_db = session.get(Article, article_id)
        # Check if it is found
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        # Map the update data with the fields from the database
        article_data = article.model_dump(exclude_unset=True)
        # effectively update the article from the database
        article_db.sqlmodel_update(article_data)
        # Mark this article as "updatable"
        session.add(article_db)
        # Commit the update to the database
        session.commit()
        # Refresh the instance of the article of the session from the db
        session.refresh(article_db)
        # Return the result
        return article_db

# Comments APIs
@app.post("/comments/")
def create_comment(article_id: int, comment: Comment):
    session = Session(myblog_db)
    # Check if article exist
    if not session.get(Article, article_id):
        raise HTTPException(status_code=404, detail="Comment not possible. Article not found")
    comment.article_id = article_id
    session.add(comment)
    session.commit()
    session.refresh(comment)
    print("New comment: ", comment.id)
    return comment


@app.get("/comments", response_model=list[Comment])
def list_comments():
    with Session(myblog_db) as session:
        statement = select(Comment)
        print(statement)
        comments = session.exec(statement).all()
        return comments
    
@app.get("/comments/{comment_id}", 
         response_model=Comment,
         )
def get_comment(comment_id: int):
    with Session(myblog_db) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id):
    with Session(myblog_db) as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        session.delete(comment)
        session.commit()
        return {
            "deleted": True
        }

@app.patch("/comments/{comment_id}") 
def update_comment(comment_id: int, comment: CommentUpdate):
    with Session(myblog_db) as session:
        comment_db = session.get(Comment, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found!")
        comment_data = comment.model_dump(exclude_unset=True)
        comment_db.sqlmodel_update(comment_data)
        session.add(comment_db)
        session.commit()
        session.refresh(comment_db)
        return comment_db
