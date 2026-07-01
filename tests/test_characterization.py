"""Characterization tests locking in the pre-refactor CLI behavior.

These tests drive the CLI through `main()` + `sys.argv` + stdout, the same
way a real user would invoke
`python -m mini_inventory.inventory <command> [args...]`.

Each test gets its own fresh `InventoryService` instance (via the
`service` fixture) and passes it explicitly into `main()`. This mirrors
real-world usage: every CLI process starts with empty state, since state
is never shared through module/global scope (CLAUDE.md criterion 8).
Calling `main()` multiple times in one test with the *same* `service`
instance simulates a sequence of commands sharing state explicitly, the
same way persistent state would be threaded through in a real
application.

Per CLAUDE.md, the usage text is explicitly exempt from the "identical
behavior" requirement; everything else here must remain byte-for-byte
identical before and after refactoring.
"""

import pytest

from mini_inventory import inventory
from mini_inventory.service import InventoryService


@pytest.fixture
def service() -> InventoryService:
    """Provide a fresh, empty InventoryService for each test."""
    return InventoryService()


def run_cli(service, monkeypatch, capsys, *argv):
    """Invoke ``main(service)`` with the given argv and return stdout.

    Args:
        service: the InventoryService instance to operate on.
        monkeypatch: pytest monkeypatch fixture.
        capsys: pytest capsys fixture.
        *argv: command + arguments (without the leading program name).

    Returns:
        The captured stdout text for this single invocation.
    """
    monkeypatch.setattr("sys.argv", ["inventory.py", *argv])
    inventory.main(service)
    return capsys.readouterr().out


def test_add_new_item(service, capsys, monkeypatch):
    """Adding a brand-new item prints 'added <name>'."""
    out = run_cli(service, monkeypatch, capsys, "add", "widget", "10", "2.5")
    assert out == "added widget\n"


def test_add_existing_item_accumulates_qty(service, capsys, monkeypatch):
    """Adding an existing item accumulates quantity; list reflects total."""
    run_cli(service, monkeypatch, capsys, "add", "widget", "10", "2.5")
    out = run_cli(service, monkeypatch, capsys, "add", "widget", "5", "9.99")
    assert out == "added widget\n"
    out = run_cli(service, monkeypatch, capsys, "list")
    assert out == "widget: qty=15 price=2.5 subtotal=37.5\n"


def test_remove_enough_stock(service, capsys, monkeypatch):
    """Removing stock when enough is available prints 'removed <name>'."""
    run_cli(service, monkeypatch, capsys, "add", "widget", "10", "2.5")
    out = run_cli(service, monkeypatch, capsys, "remove", "widget", "4")
    assert out == "removed widget\n"
    out = run_cli(service, monkeypatch, capsys, "list")
    assert out == "widget: qty=6 price=2.5 subtotal=15.0\n"


def test_remove_not_enough_stock(service, capsys, monkeypatch):
    """Removing more stock than available prints an error, qty unchanged."""
    run_cli(service, monkeypatch, capsys, "add", "widget", "3", "2.5")
    out = run_cli(service, monkeypatch, capsys, "remove", "widget", "4")
    assert out == "error: not enough stock\n"
    out = run_cli(service, monkeypatch, capsys, "list")
    assert out == "widget: qty=3 price=2.5 subtotal=7.5\n"


def test_remove_unknown_item(service, capsys, monkeypatch):
    """Removing an item that doesn't exist prints 'error: no item'."""
    out = run_cli(service, monkeypatch, capsys, "remove", "ghost", "1")
    assert out == "error: no item\n"


def test_total_with_items(service, capsys, monkeypatch):
    """Total prints the sum of qty*price across all items."""
    run_cli(service, monkeypatch, capsys, "add", "a", "2", "3.5")
    run_cli(service, monkeypatch, capsys, "add", "b", "1", "10")
    out = run_cli(service, monkeypatch, capsys, "total")
    assert out == "total value: 17.0\n"


def test_total_empty(service, capsys, monkeypatch):
    """Total with no items prints 0 (int, since sum starts at 0)."""
    out = run_cli(service, monkeypatch, capsys, "total")
    assert out == "total value: 0\n"


def test_low_stock_flags_below_threshold(service, capsys, monkeypatch):
    """Items with qty < 5 are flagged as low."""
    run_cli(service, monkeypatch, capsys, "add", "a", "4", "1.0")
    out = run_cli(service, monkeypatch, capsys, "low")
    assert out == "a is low (4)\n"


def test_low_stock_boundary_at_5_not_flagged(service, capsys, monkeypatch):
    """An item with exactly qty == 5 is NOT flagged (condition is strict <)."""
    run_cli(service, monkeypatch, capsys, "add", "a", "5", "1.0")
    out = run_cli(service, monkeypatch, capsys, "low")
    assert out == ""


def test_list_items_format(service, capsys, monkeypatch):
    """List prints 'name: qty=.. price=.. subtotal=..' per item."""
    run_cli(service, monkeypatch, capsys, "add", "a", "2", "3.5")
    out = run_cli(service, monkeypatch, capsys, "list")
    assert out == "a: qty=2 price=3.5 subtotal=7.0\n"


def test_unknown_command(service, capsys, monkeypatch):
    """An unrecognized command prints 'unknown command'."""
    out = run_cli(service, monkeypatch, capsys, "frobnicate")
    assert out == "unknown command\n"


def test_main_usage_when_too_few_args(service, capsys, monkeypatch):
    """main() with no command argv prints a usage message.

    Note: per CLAUDE.md the exact usage text is exempt from the
    "identical behavior" requirement and may change during refactor;
    this test only pins down current pre-refactor behavior for reference.
    """
    monkeypatch.setattr("sys.argv", ["inventory.py"])
    inventory.main(service)
    out = capsys.readouterr().out
    assert out == "usage: inventory.py <command> [args...]\n"


def test_main_constructs_service_when_omitted(capsys, monkeypatch):
    """main() with no service argument builds its own, matching a real run."""
    monkeypatch.setattr("sys.argv", ["inventory.py", "total"])
    inventory.main()
    out = capsys.readouterr().out
    assert out == "total value: 0\n"
