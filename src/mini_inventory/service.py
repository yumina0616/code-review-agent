"""Pure business logic for the mini inventory system.

None of the functions/methods in this module perform I/O (no ``print``/
``input``); they only return values, so they can be unit-tested directly
without capturing stdout.
"""

from mini_inventory.models import Inventory, Item

LOW_STOCK_THRESHOLD = 5


class InventoryService:
    """Holds inventory state and exposes stock operations.

    State lives on the instance (not as module-level global mutable
    state), so multiple independent instances can be created and tested
    in isolation.
    """

    def __init__(self) -> None:
        """Create a service with an empty inventory."""
        self._items: Inventory = {}

    @property
    def items(self) -> Inventory:
        """Return the underlying name-to-item mapping."""
        return self._items

    def reset(self) -> None:
        """Clear all items, returning the inventory to an empty state."""
        self._items.clear()

    def add_item(self, name: str, qty: int, price: float) -> str:
        """Add qty of name at price, creating or accumulating as needed.

        Args:
            name: item name.
            qty: quantity to add.
            price: unit price, used only when creating a new item.

        Returns:
            A confirmation message.
        """
        if name in self._items:
            self._items[name].qty = self._items[name].qty + qty
        else:
            self._items[name] = Item(qty=qty, price=price)
        return f"added {name}"

    def remove_item(self, name: str, qty: int) -> str:
        """Remove qty of name if enough stock is available.

        Args:
            name: item name.
            qty: quantity to remove.

        Returns:
            A confirmation message, or an error message if the item is
            unknown or there isn't enough stock.
        """
        if name not in self._items:
            return "error: no item"
        if self._items[name].qty - qty < 0:
            return "error: not enough stock"
        self._items[name].qty = self._items[name].qty - qty
        return f"removed {name}"

    def calc_total(self) -> float | int:
        """Compute the total inventory value (sum of qty * price).

        Returns:
            0 when the inventory is empty, otherwise a float sum.
        """
        total: float | int = 0
        for item in self._items.values():
            total = total + item.qty * item.price
        return total

    def find_low_stock(self) -> list[tuple[str, int]]:
        """List items whose quantity is below LOW_STOCK_THRESHOLD.

        Returns:
            A list of (name, qty) pairs, in insertion order.
        """
        return [
            (name, item.qty)
            for name, item in self._items.items()
            if item.qty < LOW_STOCK_THRESHOLD
        ]

    def list_items(self) -> list[tuple[str, int, float, float]]:
        """List all items together with their subtotal (qty * price).

        Returns:
            A list of (name, qty, price, subtotal) tuples, in insertion
            order.
        """
        return [
            (name, item.qty, item.price, item.qty * item.price)
            for name, item in self._items.items()
        ]
