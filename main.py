# from repository import OrderRepository <- non importo la class ma l'istanza
from fastapi import FastAPI, HTTPException
from domain import Order, OrderItem
from repository import order_repo

app = FastAPI()

# Creare an Order (Draft)
@app.post("/orders", status_code=201)
def create_order():
    # crea un ordine vuoto
    new_order = Order()
    # inserisce l'ordine a db
    order_repo.save(new_order)
    # do conferma all'utente 
    return {
        "message": "Order created",
        "id": new_order.id
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
        return {
            "message": "Item added",
            "total": len(order.items)
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@app.post("/orders/{order_id}/confirm")
def confirm_order(order_id: str):
    order = order_repo.get_by_id(order_id)
    if not order:
            raise HTTPException(status_code=404, detail="Order not found")
    
    try:
        order.confirm()
        order_repo.save(order)
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
    return {
         "message": "Order found",
         "order": order
    }

@app.get("/orders")
def get_orders():
    orders = order_repo.get_all()
    return {
        "count": len(orders),
        "orders": orders
    }

#"/orders/{order_id}/confirm" 
#"/orders/{order_id}/cancel"
#"/orders/{order_id}/ship"