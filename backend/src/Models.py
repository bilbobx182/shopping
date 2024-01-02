"""
Model for grocery store products
"""
from __future__ import annotations

from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, Relationship
from typing import Optional


class Category(SQLModel):
    """
    Model for Category
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Company(SQLModel):
    """
    Model for shops
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Food(SQLModel):
    """
    Food class Model for everything a food item is associated with.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    product: str
    is_promotion: bool
    price: float
    unit_price: float
    url: Optional[str]
    date: datetime = datetime.now()

    company_id: Optional[int] = Field(default=None, foreign_key="company.id")
    company: Optional[Company] = Relationship(back_populates="food")

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="food")

