from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from typing import List

from backend.app.crud import users as users_crud
from backend.app.models.models import User
from backend.app.schemas import users as users_schemas
from backend.app.security.auth import get_current_user

# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db

# インスタンスをアノテーションに利用することでエンドポイントを定義できる
router = APIRouter()

# Userを登録
@router.post("/users/", response_model=users_schemas.UserCreate, status_code=201)
async def create_user(user: users_schemas.UserCreate, db: Session = Depends(get_db)):
    return users_crud.create_user(db=db, user=user)

# Userの全取得
@router.get("/users/", response_model=List[users_schemas.UserRead], status_code=200)
def read_users(db: Session = Depends(get_db)):
    return users_crud.read_users(db=db)

# トークン検証
# @router.get("/users/", response_model=List[users_schemas.UserRead], status_code=200)
# def read_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return users_crud.read_users(db=db)

# 単一のUserを取得
@router.get("/users/{user_id}", response_model=users_schemas.UserRead, status_code=200)
def read_user_id(user_id: int, db: Session = Depends(get_db)):
    user = users_crud.read_user_id(db=db, user_id=user_id)
    return user

# Userを更新
@router.put("/users/{user_id}", response_model=users_schemas.UserUpdate, status_code=200)
def update_user(user_id: int, user: users_schemas.UserUpdate, db: Session = Depends(get_db)):
    return users_crud.update_user(db=db, user=user, user_id=user_id)

# Userを削除
@router.delete("/users/{user_id}", response_model=users_schemas.UserDelete, status_code=200)
def delete_user_id(user_id: int, db: Session = Depends(get_db)):
    return users_crud.delete_user_id(db=db, user_id=user_id)

