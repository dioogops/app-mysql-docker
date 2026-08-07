from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas no banco ao iniciar (use Alembic em produção)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FastAPI + MySQL",
    description="API de exemplo com FastAPI e MySQL",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
