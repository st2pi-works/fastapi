from pydantic import BaseModel
from typing import Optional
import datetime

# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
# PydanticのBaseModelを継承して、Createエンドポイントで利用するデータの定義を行う
class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True # SQLAlchemyのモデルをPydanticのモデルに変換する設定


# PydanticのBaseModelを継承して、Readエンドポイントで利用するデータの定義を行う
class UserRead(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


# PydanticのBaseModelを継承して、Updateエンドポイントで利用するデータの定義を行う
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


# PydanticのBaseModelを継承して、Deleteエンドポイントで利用するデータの定義を行う
class UserDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True


# PydanticのBaseModelを継承して、Loginエンドポイントで利用するデータの定義を行う
class UserLogin(BaseModel):
    username: str
    hashed_password: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    login_username: str
    login_password: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: Optional[str] = None

    class Config:
        from_attributes = True


