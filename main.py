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
# MYSQL_PORT = os.getenv("MYSQL_PORT") # In case there is a conflict with another MYSQL instance
CONNECTION_STRING = f"mysql+mysqlconnector://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}@localhost/{MYSQL_DATABASE}" # Build f-String
myblog_db = create_engine(CONNECTION_STRING)


# Article class
@dataclass # Decorator to tie the class to the database
class Article(SQLModel, table =True):
    __tablename__="articles"
    id: int | None = Field(default=None, primary_key=True)
    author: str
    title: str
    body: str | None = Field(default=None)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))

class ArticleUpdate(SQLModel): # Data Model for FastAPI
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

class CommentUpdate(SQLModel): # Data Model for FastAPI
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
def create_article(article: ArticleUpdate): # Use class `ArticleUpdate` to limit request to the required parameters
    # Create a session to the DB
    session = Session(myblog_db)
    # Complete the article object by validating/mapping the input to the model tied to the DB
    db_article = Article.model_validate(article)
    # then add the article
    session.add(db_article)
    # Commit the session
    session.commit()
    # Refresh Session
    session.refresh(db_article)
    # Return restuls
    print("New article: ", db_article.id)
    return db_article

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
def create_comment(article_id: int, comment: CommentUpdate):
    session = Session(myblog_db)
    # Check if article exist
    if not session.get(Article, article_id):
        raise HTTPException(status_code=404, detail="Comment not possible. Article not found")
    # Complete the article object by validating/mapping the input to the model tied to the DB
    db_comment = Comment.model_validate(comment)
    db_comment.article_id = article_id
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    print("New comment: ", db_comment.id)
    return db_comment


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
