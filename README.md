# Microservices with Python and FastAPI

## Use case
A simple blogging system. It is a site that allows users to create, edit and delete their articles. The site allows to comment and rate articles, in addtion to authenticate users. 

## Service Architecture
 - **Article Class**
    * UpdateArticle 
    * CreateArticle 
    * DeleteArticle 
    * ReadArticle 

 - **User Class**
    * AuthenticateUser 
    * CreateUser 
    * UpdatePassword 
    * UpdateUser 

 - **Rating Class** 
    * LikeArticle 

 - **Comment Class**
    * CommentArticle 

## Execution
Run in the terminal: 
```Python
fastapi dev main.py
```
