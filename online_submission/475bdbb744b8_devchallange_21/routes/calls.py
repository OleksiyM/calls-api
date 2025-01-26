from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.constants import MSG_CALL_NOT_FOUND, MSG_URL_REQUIRED
from db import get_db
from repository.calls import get_call_by_id, create_call
from schemas.calls import CallCreate

router = APIRouter(prefix='/call', tags=['call'])


@router.get("/{id}")
async def get_call(id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a call by its ID."""
    call = await get_call_by_id(db, id)
    if not call:
        raise HTTPException(status_code=404, detail=MSG_CALL_NOT_FOUND)
    return call


@router.post("/")
async def create_new_call(call: CallCreate, db: AsyncSession = Depends(get_db)):
    """Create a new call."""
    if not call.audio_url:
        raise HTTPException(status_code=400, detail=MSG_URL_REQUIRED)
    new_call = await create_call(db, call)
    return {"id": new_call.id}
