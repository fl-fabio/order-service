from domain import Order
from typing import Dict, Optional

class OrderRepository:
    def __init__(self):
        self.storage: Dict[str, Order] = {}

    def save(self, order: Order):
        self.storage[order.id] = Order

    def get_by_id(self, order_id) -> Optional[Order]:
        return self.storage.get(order_id)
    
    def get_all(self):
        return list(self.storage)


order_repo = OrderRepository()
