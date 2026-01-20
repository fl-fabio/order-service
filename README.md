classDiagram
direction LR

class Order {
    <<Aggregate Root>>
    id: str
    status: OrderStatus
    items: List[OrderItem]

    add_product()
    confirm()
    cancel()
    ship()
}

class OrderItem {
    product_id: str
    price: float
    quantity: int
}

class OrderStatus {
    <<enum>>
    DRAFT
    CONFIRMED
    SHIPPED
    CANCELED
}

class OrderRepository {
    <<Repository>>
    save()
    get_by_id()
}

Order "1" *-- "*" OrderItem
Order --> OrderStatus
OrderRepository --> Order
