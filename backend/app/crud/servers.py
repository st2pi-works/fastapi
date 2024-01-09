from sqlalchemy.orm import Session
from backend.app.models import models
from backend.app.schemas import servers
from fastapi import HTTPException

# Serverを登録
def create_server(db: Session, server: servers.ServerCreate):
    db_server = models.Server(
        servername=server.servername,
        area_id=server.area_id,
        center_id=server.center_id
    )

    # servernameが空の場合 エラーとdetailを返す
    if server.servername == "":
        raise HTTPException(status_code=400, detail="Servername is empty")

    # servernameがNoneの場合 エラーとdetailを返す
    elif server.servername is None:
        raise HTTPException(status_code=400, detail="Servername is None")

    # servernameが既に存在する場合 エラーとdetailを返す
    elif db.query(models.Server).filter(models.Server.servername == server.servername).first():
        raise HTTPException(status_code=400, detail="Servername already exists")

    # servernameの文字列の中に空白が含まれていた場合 detailを返す
    elif ' ' in server.servername:
        raise HTTPException(status_code=400, detail="Servername contains spaces")

    # servernameの文字列の中に全角文字が含まれていた場合 detailを返す
    elif len(server.servername) != len(server.servername.encode()):
        raise HTTPException(status_code=400, detail="Servername contains full-width characters")

    else:
        db.add(db_server)
        db.commit()
        db.refresh(db_server)
        return db_server

# serverの全取得
def read_servers(db: Session):
    return db.query(models.Server).all()

# servernameが部分一致したServerを取得、空であれば取得しない
def get_server_by_servername(db: Session, servername: str):
    db_server = db.query(models.Server).filter(models.Server.servername.like('%' + servername + '%')).all()
    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server

# serverIDが一致したServerを取得
def get_server_by_id(db: Session, server_id: int):
    db_server = db.query(models.Server).filter(models.Server.id == server_id).first()
    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server

# serverの更新、idを指定して更新する
def update_server(db: Session, server: servers.ServerUpdate, server_id: int):
    db_server = db.query(models.Server).filter(models.Server.id == server_id).first()

    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")

    # 更新されるフィールドだけを適用
    for var, value in vars(server).items():
        if value is not None:
            setattr(db_server, var, value)

    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server

# serverの削除、idを指定して削除する
def delete_server(db: Session, server_id: int):
    db_server = db.query(models.Server).filter(models.Server.id == server_id).first()
    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    db.delete(db_server)
    db.commit()
    return db_server