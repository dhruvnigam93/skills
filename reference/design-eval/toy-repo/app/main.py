from fastapi import FastAPI, Depends
from app.auth import current_user, User
from app.db import Store

app = FastAPI()
store = Store()


@app.get("/items")
def list_items(user: User = Depends(current_user)):
    return store.list_items(user.id)


@app.post("/items")
def create_item(name: str, user: User = Depends(current_user)):
    return store.add_item(user.id, name)


@app.get("/items/{item_id}")
def get_item(item_id: str, user: User = Depends(current_user)):
    return store.get_item(user.id, item_id)
