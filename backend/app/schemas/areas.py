from pydantic import BaseModel
from typing import Optional
import datetime


class AreaCreate(BaseModel):
    areaname: str

    class Config:
        from_attributes = True # SQLAlchemyのモデルをPydanticのモデルに変換する設定

class AreaRead(AreaCreate):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True