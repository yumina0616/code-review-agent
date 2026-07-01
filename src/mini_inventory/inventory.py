"""Backward-compatible CLI entry point for the mini inventory system.

The actual implementation now lives in :mod:`mini_inventory.models`
(data structures), :mod:`mini_inventory.service` (business logic), and
:mod:`mini_inventory.cli` (I/O). This module re-exports ``main`` so that
``python -m mini_inventory.inventory`` keeps working unchanged.
"""

from mini_inventory.cli import main

__all__ = ["main"]

if __name__ == "__main__":
    main()
