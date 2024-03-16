from datetime import datetime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from typing_extensions import List

from database import db
from sqlalchemy import Integer, func, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    posts: Mapped[List["Posts"]] = relationship(back_populates="user")


class Posts(Base):
    __tablename__ = "posts"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="posts")
