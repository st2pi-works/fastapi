from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.requests import Request

from backend.app.crud.users import get_user_by_username
from backend.app.schemas.users import TokenData, Token, UserRead, UserLogin, LoginRequest
from backend.app.security.security import verify_password


# JWTの暗号化に利用する文字列
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2のBearer Tokenを利用するための設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# エンドポイントを定義するためのインスタンスを作成
router = APIRouter()


# 各エンドポイントの関数に渡すDB接続のセッションを定義
def get_db(request: Request):
    return request.state.db


# アクセストークンの生成
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # アクセストークンの期限を設定する
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# リフレッシュトークンの生成
def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # リフレッシュトークンの期限を設定する
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# リフレッシュトークンのデコードと検証
def decode_refresh_token(token: str):
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception


# アクセストークンのデコードと検証
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db_user = get_user_by_username(db=db,username=token_data.username)
    if db_user is None:
        raise credentials_exception
    return db_user


# ユーザー名とパスワードを受け取り、ユーザーが存在するかどうかを確認
def authenticate_user(input_username: str, input_password: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db=db, username=input_username)
    # ユーザーが存在する場合はユーザーを返し、存在しない場合はNoneを返す
    if user is None:
        return None
    # パスワードの検証
    if verify_password(plain_password=input_password, hashed_password=user.hashed_password):
        return user
    return None


# ログイン認証　ログイン後にアクセストークンとリフレッシュトークンを生成して返す
@router.post("/login/", response_model=Token, status_code=200)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # ユーザーの検証
    user = authenticate_user(request.login_username, request.login_password, db)
    if user is None:
        raise credentials_exception

    # アクセストークンの生成
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # リフレッシュトークンの生成
    refresh_token_expires = timedelta(days=7) # 7日後に期限切れ
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# ログインユーザーの取得
@router.get("/users/me/", response_model=UserRead, status_code=200)
async def read_users_me(current_user: str = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=404, detail="Inactive user")
    return current_user


# リフレッシュトークンのエンドポイント　期限が切れていない場合はアクセストークンを生成して返す
@router.post("/token/refresh/", response_model=Token, status_code=200)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    # リフレッシュトークンのデコードと検証
    payload = decode_refresh_token(refresh_token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # ユーザーの検証
    user = get_user_by_username(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    # 新しいアクセストークンの生成
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.name}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


# ログアウト
@router.post("/logout/", status_code=200)
async def logout():
    return {"message": "Logout successful"}


