from threading import Lock
from datetime import datetime, timezone
from typing import List, Optional
from .schemas import OrderCreate, OrderOut, OrdersSummary
from .utils import compute_cost


class OrderStorage:
    def __init__(self):
        self._lock = Lock()
        self._orders: List[OrderOut] = []
        self._next_id = 1

    def create_order(self, order: OrderCreate) -> OrderOut:
        total = compute_cost(order.pages, order.paper_type)
        with self._lock:
            oid = self._next_id
            self._next_id += 1
            out = OrderOut(
                id=oid,
                client_name=order.client_name,
                pages=order.pages,
                paper_type=order.paper_type,
                status=order.status,
                total_cost=total,
                created_at=datetime.now(timezone.utc),
            )
            self._orders.append(out)
            return out

    def list_orders(self) -> List[OrderOut]:
        # Return a shallow copy of orders list
        return list(self._orders)

    def summary(self) -> OrdersSummary:
        orders = list(self._orders)
        total_orders = len(orders)
        total_revenue = round(sum(o.total_cost for o in orders), 2)
        return OrdersSummary(total_orders=total_orders, total_revenue=total_revenue, orders=orders)

    def get_order(self, order_id: int) -> Optional[OrderOut]:
        for o in self._orders:
            if o.id == order_id:
                return o
        return None

    def update_status(self, order_id: int, status: str) -> Optional[OrderOut]:
        with self._lock:
            for idx, o in enumerate(self._orders):
                if o.id == order_id:
                    updated = o.model_copy()
                    updated.status = status
                    self._orders[idx] = OrderOut(**updated.model_dump())
                    return self._orders[idx]
        return None

    def delete_order(self, order_id: int) -> bool:
        with self._lock:
            for idx, o in enumerate(self._orders):
                if o.id == order_id:
                    del self._orders[idx]
                    return True
        return False

