from typing import Optional, List

from pydantic import BaseModel

from schemas.categories import Category


class CallCreate(BaseModel):
    audio_url: str


class Call(BaseModel):
    id: int
    name: Optional[str] = None
    location: Optional[str] = None
    emotional_tone: str
    text: str
    url: str
    categories: List[Category]

    class Config:
        from_attributes = True
