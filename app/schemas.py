from typing import Dict, Optional
from pydantic import BaseModel, Field


class ProductInput(BaseModel):
    name: str = Field(..., description="Название товара")
    manufacturer: str = Field(..., description="Производитель")
    specs: Dict[str, str] = Field(default_factory=dict, description="Характеристики")
    description: Optional[str] = Field(None, description="Текстовое описание или фрагмент паспорта")


class ProductOutput(BaseModel):
    seo_title: str
    seo_description: str
    key_features: list[str]
    search_queries: list[str]
    commercial_block: str
    missing_data: list[str]
