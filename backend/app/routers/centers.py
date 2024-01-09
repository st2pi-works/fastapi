from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from typing import List

from backend.app.crud import centers as centers_crud
from backend.app.schemas import centers as centers_schemas

# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db

# インスタンスをアノテーションに利用することでエンドポイントを定義できる
router = APIRouter()

# Centerを登録
@router.post("/centers/", response_model=centers_schemas.CenterCreate, status_code=201)
def create_server(center: centers_schemas.CenterCreate, db: Session = Depends(get_db)):
    return centers_crud.create_center(db=db, center=center)

# Centerの全取得
@router.get("/centers/", response_model=List[centers_schemas.CenterRead], status_code=200)
def read_centers(db: Session = Depends(get_db)):
    return centers_crud.read_centers(db=db)

# CenterのIDを指定してcentername取得
@router.get("/centers/{center_id}", response_model=centers_schemas.CenterRead, status_code=200)
def read_center_id(center_id: int, db: Session = Depends(get_db)):
    center = centers_crud.read_center_id(db=db, center_id=center_id)
    return center
