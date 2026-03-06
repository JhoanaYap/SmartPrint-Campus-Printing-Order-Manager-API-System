from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


StatusLiteral = Literal["pending", "completed", "cancelled"]
PaperType = Literal["black_white", "colored", "photo"]


class OrderCreate(BaseModel):
    client_name: str = Field(...)
    pages: int = Field(..., gt=0)
    paper_type: PaperType = Field(...)
    status: StatusLiteral = Field(default="pending")


class OrderOut(OrderCreate):
    id: int
    total_cost: float
    created_at: datetime


class OrdersSummary(BaseModel):
    total_orders: int
    total_revenue: float
    orders: list[OrderOut]
