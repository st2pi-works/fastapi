from sqlalchemy.orm import Session
from backend.app.models import models
from backend.app.schemas import centers
from fastapi import HTTPException

# Centerを登録
def create_center(db: Session, center: centers.CenterCreate):
    db_center = models.Center(
        centername=center.centername
    )

    # servernameが空の場合 エラーとdetailを返す
    if center.centername == "":
        raise HTTPException(status_code=400, detail="Areaname is empty")

    # servernameがNoneの場合 エラーとdetailを返す
    elif center.centername is None:
        raise HTTPException(status_code=400, detail="Areaname is None")

    # servernameが既に存在する場合 エラーとdetailを返す
    elif db.query(models.Center).filter(models.Center.centername == center.centername).first():
        raise HTTPException(status_code=400, detail="Areaname already exists")

    # servernameの文字列の中に空白が含まれていた場合 detailを返す
    elif ' ' in center.centername:
        raise HTTPException(status_code=400, detail="Areaname contains spaces")

    # servernameの文字列の中に全角文字が含まれていた場合 detailを返す
    elif len(center.centername) != len(center.centername.encode()):
        raise HTTPException(status_code=400, detail="Areaname contains full-width characters")

    else:
        db.add(db_center)
        db.commit()
        db.refresh(db_center)
        return db_center


# Centerの全取得
def read_centers(db: Session):
    return db.query(models.Center).all()

# CenterのIDを指定してcenternameを取得
def read_center_id(db: Session, center_id: int):
    db_center = db.query(models.Center).filter(models.Center.id == center_id).first()
    if db_center is None:
        raise HTTPException(status_code=404, detail="Center not found")
    return db_center