from contextlib import asynccontextmanager
import fastapi
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from src.app.endpoints import pdf_upload
from src.app.endpoints import query_data
from services.db_conection import init_db, engine, remove_session


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        finally:
            remove_session()


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    init_db()
    yield
    engine.dispose()


app = fastapi.FastAPI(lifespan=lifespan)

app.add_middleware(DBSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_upload.router, prefix="/pdf-upload")
app.include_router(query_data.router, prefix="/data")