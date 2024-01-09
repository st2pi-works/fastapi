from pydantic import BaseModel
from typing import Optional
import datetime


# PydanticのBaseModelを継承して、Createエンドポイントで利用するデータの定義を行う
class ServerCreate(BaseModel):
    servername: str
    center_id: Optional[int]
    area_id: Optional[int]
    class Config:
        from_attributes = True # SQLAlchemyのモデルをPydanticのモデルに変換する設定
        orm_mode = True # SQLAlchemyのモデルをPydanticのモデルに変換する設定

# PydanticのBaseModelを継承して、Readエンドポイントで利用するデータの定義を行う
class ServerRead(ServerCreate):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
        orm_mode = True

# PydanticのBaseModelを継承して、Updateエンドポイントで利用するデータの定義を行う
class ServerUpdate(BaseModel):
    servername: Optional[str]
    center_id: Optional[int]
    area_id: Optional[int]
    #現時点の時刻を取得
    updated_at: datetime.datetime = datetime.datetime.now()

    class Config:
        from_attributes = True
        orm_mode = True

# PydanticのBaseModelを継承して、Deleteエンドポイントで利用するデータの定義を行う
class ServerDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True