from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from typing import List

from backend.app.crud import servers as servers_crud
from backend.app.schemas import servers as servers_schemas

# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db

# インスタンスをアノテーションに利用することでエンドポイントを定義できる
router = APIRouter()

# Serverを登録
@router.post("/servers/", response_model=servers_schemas.ServerCreate, status_code=201)
def create_server(server: servers_schemas.ServerCreate, db: Session = Depends(get_db)):
    return servers_crud.create_server(db=db, server=server)

# Serverの全取得
@router.get("/servers/", response_model=List[servers_schemas.ServerRead], status_code=200)
def read_servers(db: Session = Depends(get_db)):
    return servers_crud.read_servers(db=db)

# servernameが部分一致したServerを取得
@router.get("/servers/{servername}", response_model=List[servers_schemas.ServerRead], status_code=200)
def get_server_by_servername(servername: str, db: Session = Depends(get_db)):
    return servers_crud.get_server_by_servername(db=db, servername=servername)

# serverのIDが一致したServerを取得
@router.get("/servers/id/{server_id}", response_model=servers_schemas.ServerRead, status_code=200)
def get_server_by_id(server_id: int, db: Session = Depends(get_db)):
    return servers_crud.get_server_by_id(db=db, server_id=server_id)

# serverを更新(IDで指定)
@router.put("/servers/{server_id}", response_model=servers_schemas.ServerUpdate, status_code=200)
def update_server(server_id: int, server: servers_schemas.ServerUpdate, db: Session = Depends(get_db)):
    return servers_crud.update_server(db=db, server=server, server_id=server_id)

# serverのidを指定してServerを削除
@router.delete("/servers/{server_id}", response_model=servers_schemas.ServerDelete, status_code=200)
def delete_server(server_id: int, db: Session = Depends(get_db)):
    return servers_crud.delete_server(db=db, server_id=server_id)
