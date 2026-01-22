from enum import Enum
from pydantic import BaseModel
import uuid
from typing import List

class OrderStatus(str, Enum):
    DRAFT = "Draft"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    CANCELED = "Canceled"

class OrderItem(BaseModel):
    product_id: str
    price: float
    quantity: int

class Order:
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        self.items: List[OrderItem] = []
        self.status = OrderStatus.DRAFT

    def add_product(self, item: OrderItem):
        if self.status != OrderStatus.DRAFT:
            raise ValueError("Order must be only in Draft Status.")
        if item.quantity <= 0:
            raise ValueError("Product quantity must be equal or greater than zero")
        self.items.append(item)

    def confirm(self):
        if self.status != OrderStatus.DRAFT:
            raise ValueError("Order must be Draft before confirm.")
        self.status = OrderStatus.CONFIRMED

    def cancel(self):
        if self.status != OrderStatus.SHIPPED:
            raise ValueError("A shipped order cannot be canceled")
        self.status = OrderStatus.CANCELED

    def ship(self):
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError("Order must be confirmed befor shpping")
        self.status = OrderStatus.SHIPPED


"""
new_order = Order()
item = {
    product_id = "dsfsdrew32423",
    price = 25.00,
    quantity = -3
}
new_order = {
    id: "sdsdr234234",
    items: [
        {
            product_id = "dsfsdrew32423",
            price = 25.00,
            quantity = 3
        }
    ],
    status: "Draft"
}
"""