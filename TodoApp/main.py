from fastapi import FastAPI, HTTPException,Depends,Path
import models
from  pydantic import BaseModel,Field
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from models import Todo
from starlette import status
from routers import auth,todos
app=FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)

