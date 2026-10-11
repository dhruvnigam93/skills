# In-memory store standing in for a real database. Single point where items are persisted.
from dataclasses import dataclass, field
import uuid


@dataclass
class Store:
    _items: dict = field(default_factory=dict)

    def list_items(self, user_id: str):
        return [i for i in self._items.values() if i["user_id"] == user_id]

    def add_item(self, user_id: str, name: str):
        iid = str(uuid.uuid4())
        self._items[iid] = {"id": iid, "user_id": user_id, "name": name}
        return self._items[iid]

    def get_item(self, user_id: str, item_id: str):
        item = self._items.get(item_id)
        if item and item["user_id"] == user_id:
            return item
        return None
