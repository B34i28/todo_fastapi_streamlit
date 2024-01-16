# main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Todo
from pydantic import BaseModel

class CreateTodo(BaseModel):
    id:int
    title:str
    description:str

class ResponseTodo(BaseModel):
    id:int
    title:str
    description:str

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos/")
def create_todo(todo_create: CreateTodo, db: Session = Depends(get_db)):
    todo = Todo(**todo_create.__dict__)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return ResponseTodo(**todo.__dict__)

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: CreateTodo, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updated_todo.__dict__.items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}