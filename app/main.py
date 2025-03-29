import time

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import Base, engine, get_db
from app.routes import activities, buildings, organizations


def wait_for_db():
    max_attempts = 60
    for attempt in range(max_attempts):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                break
        except Exception as e:
            if attempt == max_attempts - 1:
                raise e
            time.sleep(1)


wait_for_db()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API App Directory",
    description="REST API для справочника Организаций, Зданий и Деятельности",
    version="1.0.0",
    dependencies=[Depends(verify_api_key)],
)

app.include_router(
    organizations.router, prefix="/organizations", tags=["Organizations"]
)
app.include_router(buildings.router, prefix="/buildings", tags=["Buildings"])
app.include_router(
    activities.router, prefix="/activities", tags=["Activities"]
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the API App Directory!"}
