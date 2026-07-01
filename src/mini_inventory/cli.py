"""Command-line interface for the mini inventory system.

All ``print``/``input`` calls live in this module; business logic lives
in :mod:`mini_inventory.service` and only returns values.
"""

import sys

from mini_inventory.service import InventoryService

USAGE = "usage: inventory.py <command> [args...]"


def dispatch(service: InventoryService, cmd: str, args: list[str]) -> list[str]:
    """Run cmd against service and return the lines that should be printed.

    Args:
        service: the inventory service to operate on.
        cmd: the command name (add/remove/total/low/list, or anything else).
        args: positional arguments for the command.

    Returns:
        A list of output lines; the caller prints each on its own line.
    """
    if cmd == "add":
        return [service.add_item(args[0], int(args[1]), float(args[2]))]
    if cmd == "remove":
        return [service.remove_item(args[0], int(args[1]))]
    if cmd == "total":
        return [f"total value: {service.calc_total()}"]
    if cmd == "low":
        return [f"{name} is low ({qty})" for name, qty in service.find_low_stock()]
    if cmd == "list":
        return [
            f"{name}: qty={qty} price={price} subtotal={subtotal}"
            for name, qty, price, subtotal in service.list_items()
        ]
    return ["unknown command"]


def main(service: InventoryService | None = None) -> None:
    """Entry point: parse argv, run the command, and print its output.

    Args:
        service: inventory service to operate on. If omitted, a fresh
            empty service is constructed locally -- matching how a real
            CLI invocation starts with no prior state, since each
            process run is independent and nothing is shared globally.
    """
    if service is None:
        service = InventoryService()
    if len(sys.argv) < 2:
        print(USAGE)
        return
    cmd = sys.argv[1]
    args = sys.argv[2:]
    for line in dispatch(service, cmd, args):
        print(line)


if __name__ == "__main__":
    main()
