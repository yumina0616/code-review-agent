"""Data structures for the mini inventory system."""

from dataclasses import dataclass


@dataclass
class Item:
    """A single inventory line: quantity on hand and unit price.

    Args:
        qty: current quantity on hand.
        price: unit price.
    """

    qty: int
    price: float


Inventory = dict[str, Item]
