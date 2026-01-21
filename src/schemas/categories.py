from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Category(BaseModel):
    title: str

class CategoryCreate(BaseModel):
    """
    Used when creating categories
    (initial seed or admin-only actions)
    """
    pass

class CategoryRead(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


