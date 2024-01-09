from sqlalchemy.orm import Session
from backend.app.models import models
from backend.app.schemas import areas
from fastapi import HTTPException

# Areaを登録
def create_area(db: Session, area: areas.AreaCreate):
    db_area = models.Area(
        areaname=area.areaname
    )

    # servernameが空の場合 エラーとdetailを返す
    if area.areaname == "":
        raise HTTPException(status_code=400, detail="Areaname is empty")

    # servernameがNoneの場合 エラーとdetailを返す
    elif area.areaname is None:
        raise HTTPException(status_code=400, detail="Areaname is None")

    # servernameが既に存在する場合 エラーとdetailを返す
    elif db.query(models.Area).filter(models.Area.areaname == area.areaname).first():
        raise HTTPException(status_code=400, detail="Areaname already exists")

    # servernameの文字列の中に空白が含まれていた場合 detailを返す
    elif ' ' in area.areaname:
        raise HTTPException(status_code=400, detail="Areaname contains spaces")

    # servernameの文字列の中に全角文字が含まれていた場合 detailを返す
    elif len(area.areaname) != len(area.areaname.encode()):
        raise HTTPException(status_code=400, detail="Areaname contains full-width characters")

    else:
        db.add(db_area)
        db.commit()
        db.refresh(db_area)
        return db_area



# Areaの全取得
def read_areas(db: Session):
    return db.query(models.Area).all()

# AreaのIDを指定してareanameを取得
def read_area_id(db: Session, area_id: int):
    db_area = db.query(models.Area).filter(models.Area.id == area_id).first()
    if db_area is None:
        raise HTTPException(status_code=404, detail="Area not found")
    return db_area
