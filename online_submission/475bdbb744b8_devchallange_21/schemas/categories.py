from datetime import date

from pydantic import BaseModel, Field
from typing import List, Optional


class CategoryBase(BaseModel):
    title: Optional[str] = None
    points: Optional[List[str]] = []

class CategoryCreate(CategoryBase):
    title: str

class CategoryUpdate(CategoryBase):
    title: Optional[str]

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

