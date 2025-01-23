from fastapi import FastAPI, HTTPException,Depends,Path
import models
from  pydantic import BaseModel,Field
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from models import Todo
from starlette import status
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]

class TodoRequest(BaseModel):
    title: str=Field(min_length=3)
    description: str=Field(min_length=3,max_length=100)
    priority: int=Field(gt=0,lt=6)
    complete: bool
        
        
@app.get("/", status_code=status.HTTP_200_OK)
def read_all(db:db_dependency):
    return db.query(Todo).all()

@app.get("/todo/{id}",status_code=status.HTTP_200_OK)
def read_one(db:db_dependency,id:int= Path(gt=0)):
    todo_model= db.query(Todo).filter(Todo.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    else:
        return todo_model
    
    
@app.post("/todo",status_code=status.HTTP_201_CREATED)
def create_one(db:db_dependency, todo_request: TodoRequest):
    todo_model = Todo(**todo_request.dict())
    
    db.add(todo_model)
    db.commit()
    
@app.put("/todo/{id}", status_code=status.HTTP_200_OK)
def update_one(db: db_dependency, todo_request: TodoRequest, id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.commit()
        db.refresh(todo_model)  # Optional, to ensure the latest state is returned

    return {"message": "Todo updated successfully", "todo": todo_model}

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(db: db_dependency, id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo_model)
        db.commit()

    return {"message": "Todo deleted successfully"}
    