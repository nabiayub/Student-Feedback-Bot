from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CategoryBase(BaseModel):
    title: str

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    """
    Used when creating categories
    (initial seed or admin-only actions)
    """
    pass




