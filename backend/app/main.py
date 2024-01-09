from fastapi import FastAPI
from starlette.requests import Request

from backend.app.database.database import SessionLocal, engine
from backend.app.models import models
from backend.app.routers import todos, users, servers, centers, areas
from backend.app.security import auth


# モデルの定義をDBに反映
models.Base.metadata.create_all(bind=engine)

# インスタンスをアノテーションに利用することでエンドポイントを定義できる
app = FastAPI()

# routers/配下を読み込む
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(servers.router)
app.include_router(centers.router)
app.include_router(areas.router)

# Token認証用のrouterを読み込む
app.include_router(auth.router)

# リクエストの度に呼ばれるミドルウェア DB接続用のセッションインスタンスを作成
# SQLAlchemyの接続プールを使用して、データベースへの接続を効率化する
@app.middleware("http")
def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = call_next(request)
    request.state.db.close()
    return response

# ルートディレクトリにアクセスした際の処理
@app.get("/")
def root():
    return {"Welcome!!"}