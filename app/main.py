from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from typing import Literal

from .schemas import OrderCreate, OrderOut, OrdersSummary
from .storage import OrderStorage
from .utils import get_pricing

app = FastAPI(title="SmartPrint: Campus Printing Order Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

storage = OrderStorage()


@app.post("/orders", response_model=OrderOut)
def create_order(order: OrderCreate):
    created = storage.create_order(order)
    return created


@app.get("/orders", response_model=OrdersSummary)
def list_orders():
    return storage.summary()


@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int):
    found = storage.get_order(order_id)
    if not found:
        raise HTTPException(status_code=404, detail="Order not found")
    return found


@app.get("/pricing")
def pricing():
    return get_pricing()


StatusLiteral = Literal["pending", "completed", "cancelled"]


@app.put("/orders/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: int, status: StatusLiteral = Body(..., embed=True)):
    updated = storage.update_status(order_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    ok = storage.delete_order(order_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"deleted": True}
