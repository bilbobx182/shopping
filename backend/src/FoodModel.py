"""
Model for grocery store products
"""
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, validator
from pydantic.typing import Optional


class Food(BaseModel):
    """
    Food class Model for everything a food item is associated with.
    """
    company: str
    category: str
    product: str
    price: float
    unit_price: float
    url: Optional[str]
    date: datetime = datetime.now()

    def csv(self):
        """
        Return the model in a CSV format.
        """
        resp = ""
        for key in self.dict():
            resp += f"{key},"
        return resp
