from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from entity.models import Category
from schemas.categories import CategoryCreate, CategoryUpdate


async def get_categories(limit: int, offset: int, db: AsyncSession):
    """
    Function to retrieve a list of categories with pagination support.
    :param limit: Maximum number of categories to retrieve.
    :param offset: Number of categories to skip.
    :param db: AsyncSession object for database operations.
    :return: List of Category objects.
    """

    stmt = select(Category).offset(offset).limit(limit)
    categories = await db.execute(stmt)
    return categories.scalars().all()


async def get_category_by_id(db: AsyncSession, category_id: int):
    """
    Function to retrieve a category by its ID.
    :param db: AsyncSession object for database operations.
    :param category_id: ID of the category to retrieve.
    :return: Category object.
    """

    stmt = select(Category).filter(Category.id == category_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_category(db: AsyncSession, category: CategoryCreate):
    """
    Function to create a new category.
    :param db: AsyncSession object for database operations.
    :param category: CategoryCreate object containing the category details.
    :return: The created category object.
    """

    db_category = Category(title=category.title, points=category.points)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def update_category(db: AsyncSession, category_id: int, category_update: CategoryUpdate):
    """
    Function to update an existing category.
    :param db: AsyncSession object for database operations.
    :param category_id: ID of the category to update.
    :param category_update: CategoryUpdate object containing the updated category details.
    :return: The updated category object.
    """

    db_category = await get_category_by_id(db, category_id)
    if db_category:
        db_category.title = category_update.title
        db_category.points = category_update.points
        await db.commit()
        await db.refresh(db_category)
    return db_category


async def update_category_partial(db: AsyncSession, category_id: int, category_update: CategoryUpdate):
    """
    Function to update an existing category with partial data.
    :param db: AsyncSession object for database operations.
    :param category_id: ID of the category to update.
    :param category_update: CategoryUpdate object containing the updated category details.
    :return: The updated category object.
    """
    
    db_category = await get_category_by_id(db, category_id)
    
    if db_category:
        # Update the title only if it is provided and not an empty string
        if category_update.title is not None and category_update.title.strip():
            db_category.title = category_update.title
        
        # Update points if provided
        if category_update.points is not None:
            db_category.points = category_update.points
        
        await db.commit()
        await db.refresh(db_category)
    
    return db_category


async def delete_category(db: AsyncSession, category_id: int):
    """
    Function to delete an existing category.
    :param db: AsyncSession object for database operations.
    :param category_id: ID of the category to delete.
    :return: The deleted category object.
    """

    db_category = await get_category_by_id(db, category_id)
    if db_category:
        await db.delete(db_category)
        await db.commit()
    return db_category
