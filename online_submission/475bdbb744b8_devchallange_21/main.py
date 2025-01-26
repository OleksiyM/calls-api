from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config.constants import MSG_DB_NOT_CONFIGURED, MSG_DB_CONNECT_ERROR, MSG_WELCOME
from db import get_db
from routes import categories, calls

app = FastAPI()

origins = ['http://localhost:8080', '*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router, prefix="/api")
app.include_router(calls.router, prefix="/api")


@app.get("/")
def index():
    """Returns a welcome message for the API"""
    return {"message": MSG_WELCOME}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """Checks the health of the database"""
    if db is None:
        raise HTTPException(status_code=500, detail=MSG_DB_NOT_CONFIGURED)

    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail=MSG_DB_NOT_CONFIGURED)
        return {"message": MSG_WELCOME}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{MSG_DB_CONNECT_ERROR}: {e}")
