from pydantic import BaseModel
from typing import Optional

# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
# PydanticのBaseModelを継承して、Createエンドポイントで利用するデータの定義を行う
class TodoCreate(BaseModel):
    title: str
    done: Optional[bool] = False

    class Config:
        from_attributes = True # SQLAlchemyのモデルをPydanticのモデルに変換する設定

# PydanticのBaseModelを継承して、Readエンドポイントで利用するデータの定義を行う
class TodoRead(BaseModel):
    id: int
    title: str
    done: bool

    class Config:
        from_attributes = True

# PydanticのBaseModelを継承して、Updateエンドポイントで利用するデータの定義を行う
class TodoUpdate(BaseModel):
    title: Optional[str]
    done: Optional[bool]

    class Config:
        from_attributes = True

# PydanticのBaseModelを継承して、UpdateCompleteエンドポイントで利用するデータの定義を行う
class TodoComplete(BaseModel):
    id: int
    title: Optional[str]
    done: Optional[bool]

    class Config:
        from_attributes = True

# PydanticのBaseModelを継承して、Deleteエンドポイントで利用するデータの定義を行う
class TodoDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True