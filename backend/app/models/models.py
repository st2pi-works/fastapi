from backend.app.database.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
import datetime

# Todoテーブルの定義
class Todo(Base):
    __tablename__ = 'todos'
    id = Column('id', Integer, primary_key = True)
    title = Column('title', String(200))
    done = Column('done', Boolean, default=False)

# Userテーブルの定義
class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key = True)
    username = Column('name', String(100), unique=True)
    email = Column('email', String(100), unique=True)
    hashed_password = Column('hashed_password', String(100))
    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

# Areaテーブルの定義
class Area(Base):
    __tablename__ = 'areas'
    id = Column('id', Integer, primary_key = True)
    areaname = Column('areaname', String(100), unique=True)
    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

# Centerテーブルの定義
class Center(Base):
    __tablename__ = 'centers'
    id = Column('id', Integer, primary_key = True)
    centername = Column('centername', String(100), unique=True)
    area_id = Column('area_id', Integer, ForeignKey('areas.id'))
    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

# Serverテーブルの定義
class Server(Base):
    __tablename__ = 'servers'
    id = Column('id', Integer, primary_key = True)
    servername = Column('servername', String(100), unique=True)
    center_id = Column('center_id', Integer, ForeignKey('centers.id'))
    area_id = Column('area_id', Integer, ForeignKey('areas.id'))
    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

