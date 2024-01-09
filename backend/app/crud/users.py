from sqlalchemy.orm import Session
from backend.app.models import models
from backend.app.schemas import users
from backend.app.security.security import get_password_hash
from fastapi import HTTPException

# Userを登録
def create_user(db: Session, user: users.UserCreate):
    # db_user = models.User(**user.dict()) dictは非推奨になったため以下に変更
    db_user = models.User(
        username=user.username,
        email=user.email,
        #hashed_password=bcrypt.hashpw(user.hashed_password.encode('utf-8'), bcrypt.gensalt()),
        hashed_password=get_password_hash(user.hashed_password)

    )
    # 同じusernameが存在するか確認する
    existing_username = db.query(models.User).filter(models.User.username == user.username).first()

    # db_userがNoneの場合 エラーを返す
    if db_user is None:
        raise HTTPException(status_code=400, detail="User already registered")
    elif existing_username is not None:
        raise HTTPException(status_code=400, detail="Same username")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Userの全取得
def read_users(db: Session):
    return db.query(models.User).all()

# 単一のUserを取得
def read_user_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# usernameが一致したUserを取得
def get_user_by_username(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Userを更新
def update_user(db: Session, user_id: int, user: users.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in vars(user).items():
        if value is not None:
            setattr(db_user, var, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Userを削除
def delete_user_id(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
