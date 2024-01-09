from pydantic import BaseModel
from typing import Optional
import datetime


class CenterCreate(BaseModel):
    centername: str

    class Config:
        from_attributes = True # SQLAlchemyのモデルをPydanticのモデルに変換する設定

class CenterRead(CenterCreate):
    id: int
    area_id: Optional[int]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True