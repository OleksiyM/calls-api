from sqlalchemy import String, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    ...


class Call(Base):
    __tablename__ = 'calls'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    emotional_tone: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)

    categories: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=[])

    @property
    def category_titles(self) -> list[str]:
        return self.categories if self.categories else []


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    points: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=[])

    @property
    def points_list(self) -> list[str]:
        return self.points if self.points else []
