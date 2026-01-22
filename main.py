# from repository import OrderRepository <- non importo la class ma l'istanza
from fastapi import FastAPI, HTTPException
from domain import Order, OrderItem
from repository import order_repo
from mangum import Mangum

app = FastAPI()

def serialize_order(order: Order):
    return {
        "id": order.id,
        "status": order.status,
        "items": [item.dict() for item in order.items],
    }

# Creare an Order (Draft)
@app.post("/orders", status_code=201)
def create_order():
    order = Order()
    order_repo.save(order)
    return {
        "message": "Order created",
        "order": serialize_order(order)
    }

# Inserire un order_item in un Order
# devo indicare a quale order_id inserire l'order_item
# products/{order_id}/items
@app.post("/orders/{order_id}/items")
def add_item(order_id: str, item: OrderItem):
    order = order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        order.add_product(item)
        order_repo.save(order)
        return serialize_order(order)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@app.post("/orders/{order_id}/confirm")
def confirm_order(order_id: str):
    order = order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        order.confirm()
        return serialize_order(order)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str):
    order = order_repo.get_by_id(order_id)
    if not order:
            raise HTTPException(status_code=404, detail="Order not found")
    
    try:
        order.cancel()
        order_repo.save(order)
    except ValueError as e:
         raise HTTPException(status_code=422, detail=str(e))
    
@app.post("/orders/{order_id}/ship")
def ship_order(order_id: str):
    order = order_repo.get_by_id(order_id)
    if not order:
            raise HTTPException(status_code=404, detail="Order not found")
    
    try:
        order.ship()
        order_repo.save(order)
    except ValueError as e:
         raise HTTPException(status_code=422, detail=str(e))
    
@app.get("/order/{order_id}")
def get_order(order_id: str):
    order = order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return serialize_order(order)

@app.get("/orders")
def get_orders():
    orders = order_repo.get_all()
    return {
        "count": len(orders),
        "orders": [serialize_order(o) for o in orders]
    }

handler = Mangum(app)