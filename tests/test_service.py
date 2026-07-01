"""Unit tests for the pure business logic in mini_inventory.service.

These tests exercise InventoryService directly (no CLI, no capsys, no
global/module state) to prove the logic is fully unit-testable in
isolation, per CLAUDE.md criterion 5 (I/O separated from logic).
"""

from mini_inventory.service import LOW_STOCK_THRESHOLD, InventoryService


def test_new_service_starts_empty():
    """A freshly constructed service has no items."""
    service = InventoryService()
    assert service.items == {}


def test_add_item_creates_new_entry():
    """Adding a new item stores its qty and price."""
    service = InventoryService()
    message = service.add_item("widget", 10, 2.5)
    assert message == "added widget"
    assert service.items["widget"].qty == 10
    assert service.items["widget"].price == 2.5


def test_add_item_accumulates_existing_entry():
    """Adding an existing item accumulates qty, keeping the original price."""
    service = InventoryService()
    service.add_item("widget", 10, 2.5)
    service.add_item("widget", 5, 999.0)
    assert service.items["widget"].qty == 15
    assert service.items["widget"].price == 2.5


def test_remove_item_with_enough_stock():
    """Removing available stock decrements qty and returns a confirmation."""
    service = InventoryService()
    service.add_item("widget", 10, 2.5)
    message = service.remove_item("widget", 4)
    assert message == "removed widget"
    assert service.items["widget"].qty == 6


def test_remove_item_not_enough_stock():
    """Removing more than available returns an error, leaving qty unchanged."""
    service = InventoryService()
    service.add_item("widget", 3, 2.5)
    message = service.remove_item("widget", 4)
    assert message == "error: not enough stock"
    assert service.items["widget"].qty == 3


def test_remove_item_unknown():
    """Removing a nonexistent item returns an error."""
    service = InventoryService()
    message = service.remove_item("ghost", 1)
    assert message == "error: no item"


def test_calc_total_empty_is_int_zero():
    """An empty inventory totals to int 0."""
    service = InventoryService()
    assert service.calc_total() == 0
    assert isinstance(service.calc_total(), int)


def test_calc_total_with_items_is_float_sum():
    """A nonempty inventory totals qty*price summed as a float."""
    service = InventoryService()
    service.add_item("a", 2, 3.5)
    service.add_item("b", 1, 10)
    assert service.calc_total() == 17.0


def test_find_low_stock_below_threshold():
    """Items below LOW_STOCK_THRESHOLD are returned."""
    service = InventoryService()
    service.add_item("a", 4, 1.0)
    service.add_item("b", 10, 1.0)
    assert service.find_low_stock() == [("a", 4)]


def test_find_low_stock_boundary_not_included():
    """An item at exactly LOW_STOCK_THRESHOLD is not considered low."""
    service = InventoryService()
    service.add_item("a", LOW_STOCK_THRESHOLD, 1.0)
    assert service.find_low_stock() == []


def test_list_items_returns_all_with_subtotal():
    """list_items returns (name, qty, price, subtotal) for every item."""
    service = InventoryService()
    service.add_item("a", 2, 3.5)
    assert service.list_items() == [("a", 2, 3.5, 7.0)]


def test_reset_clears_all_items():
    """reset() empties the inventory."""
    service = InventoryService()
    service.add_item("a", 2, 3.5)
    service.reset()
    assert service.items == {}
    assert service.calc_total() == 0
