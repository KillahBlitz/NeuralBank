from contextlib import asynccontextmanager
import fastapi
from src.app.endpoints import pdf_upload
from src.app.endpoints import query_data
from services.db_conection import init_db, engine


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    init_db()
    yield
    engine.dispose()


app = fastapi.FastAPI(lifespan=lifespan)

app.include_router(pdf_upload.router, prefix="/pdf-upload")
app.include_router(query_data.router, prefix="/data")