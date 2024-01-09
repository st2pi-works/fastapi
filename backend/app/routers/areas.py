from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from typing import List

from backend.app.crud import areas as areas_crud
from backend.app.schemas import areas as areas_schemas

# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db

# インスタンスをアノテーションに利用することでエンドポイントを定義できる
router = APIRouter()

# Areaを登録
@router.post("/areas/", response_model=areas_schemas.AreaCreate, status_code=201)
def create_area(area: areas_schemas.AreaCreate, db: Session = Depends(get_db)):
    return areas_crud.create_area(db=db, area=area)

# Areaの全取得
@router.get("/areas/", response_model=List[areas_schemas.AreaRead], status_code=200)
def read_areas(db: Session = Depends(get_db)):
    return areas_crud.read_areas(db=db)

# AreaのIDを指定して取得
@router.get("/areas/{area_id}", response_model=areas_schemas.AreaRead, status_code=200)
def read_area_id(area_id: int, db: Session = Depends(get_db)):
    area = areas_crud.read_area_id(db=db, area_id=area_id)
    return area
