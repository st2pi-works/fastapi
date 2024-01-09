from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from typing import List

from backend.app.crud import todos as todos_crud
from backend.app.models.models import Todo
from backend.app.schemas import todos as todos_schemas

# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db

# インスタンスをアノテーションに利用することでエンドポイントを定義できる
router = APIRouter()

# Todoを登録
@router.post("/todos/", response_model=todos_schemas.TodoCreate, status_code=201)
def create_todo(todo: todos_schemas.TodoCreate, db: Session = Depends(get_db)):
    return todos_crud.create_todo(db=db, todo=todo)

# Todoの全取得
@router.get("/todos/", response_model=List[todos_schemas.TodoRead], status_code=200)
def read_todos(db: Session = Depends(get_db)):
    return todos_crud.read_todos(db=db)

# 未完了(done=False)のTodoを取得
@router.get("/todos/not_done", response_model=List[todos_schemas.TodoRead], status_code=200)
def read_todos_not_done(db: Session = Depends(get_db)):
    return todos_crud.read_todos_not_done(db=db)

# 単一のTodoを取得
@router.get("/todos/{todo_id}", response_model=todos_schemas.TodoRead, status_code=200)
def read_todo_id(todo_id: int, db: Session = Depends(get_db)):
    todo = todos_crud.read_todo_id(db=db, todo_id=todo_id)
    return todo

# Todoを更新(IDで指定)
@router.put("/todos/{todo_id}", response_model=todos_schemas.TodoUpdate, status_code=200)
def update_todo(todo_id: int, todo: todos_schemas.TodoUpdate, db: Session = Depends(get_db)):
    return todos_crud.update_todo(db=db, todo=todo, todo_id=todo_id)

# Todoを完了済みに更新
@router.put("/todos/{todo_id}/complete", response_model=todos_schemas.TodoComplete, status_code=200)
def update_todo_complete(todo_id: int, db: Session = Depends(get_db)):
    return todos_crud.update_todo_complete(db=db, todo_id=todo_id)

# Todoを削除
@router.delete("/todos/{todo_id}", response_model=todos_schemas.TodoDelete, status_code=200)
def delete_todo_id(todo_id: int, db: Session = Depends(get_db)):
    return todos_crud.delete_todo_id(db=db, todo_id=todo_id)