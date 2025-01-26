from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.constants import MSG_CATEGORY_NOT_FOUND, MSG_CATEGORY_DELETED, MSG_CATEGORY_TITLE_REQUIRED
from db import get_db
from repository.categories import get_categories, create_category, update_category, update_category_partial, delete_category
from schemas.categories import CategoryCreate, CategoryUpdate

router = APIRouter(prefix='/category', tags=['category'])


@router.get("/")
async def list_categories(limit: int = Query(10, ge=10, le=100),
                          offset: int = Query(0, ge=0),
                          db: AsyncSession = Depends(get_db)):
    """Retrieves a list of categories."""
    categories = await get_categories(limit, offset, db)
    if categories is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MSG_CATEGORY_NOT_FOUND)
    return categories


@router.post("/")
async def create_new_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new category."""
    if not category.title:
        raise HTTPException(status_code=400, detail=MSG_CATEGORY_TITLE_REQUIRED)
    new_category = await create_category(db, category)
    return new_category


@router.put("/{category_id}")
async def update_existing_category(category_id: int, category: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    """Updates an existing category by ID."""
    updated_category = await update_category_partial(db, category_id, category)
    if updated_category is None:
        raise HTTPException(status_code=404, detail=MSG_CATEGORY_NOT_FOUND)
    return updated_category


@router.delete("/{category_id}")
async def delete_existing_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Deletes an existing category by ID."""
    deleted_category = await delete_category(db, category_id)
    if deleted_category is None:
        raise HTTPException(status_code=404, detail=MSG_CATEGORY_NOT_FOUND)
    return {"detail": MSG_CATEGORY_DELETED}
