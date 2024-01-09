from sqlalchemy.orm import Session
from backend.app.models import models
from backend.app.schemas import todos
from fastapi import HTTPException

# Todoを登録
def create_todo(db: Session, todo: todos.TodoCreate):
    db_todo = models.Todo(title=todo.title, done=False)
    if todo.title is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Todoの全取得
def read_todos(db: Session):
    return db.query(models.Todo).all()

# 単一のTodoを取得
def read_todo_id(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# 未完了(done=False)のTodoを取得
def read_todos_not_done(db: Session):
    todos_not_done = db.query(models.Todo).filter(models.Todo.done == False).all()
    if todos_not_done is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_not_done

# Todoを更新
def update_todo(db: Session, todo_id: int, todo: todos.TodoUpdate):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for var, value in vars(todo).items():
        if value is not None:
            setattr(db_todo, var, value)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Todoを完了済みに更新
def update_todo_complete(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.done = True
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Todoを削除
def delete_todo_id(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return db_todo
