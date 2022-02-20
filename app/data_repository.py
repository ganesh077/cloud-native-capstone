from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import List

from .schemas import Order


class OrderRepository:
    """Thread-safe in-memory repository backed by a JSON seed file."""

    def __init__(self, data_path: Path) -> None:
        self._data_path = data_path
        self._lock = Lock()
        self._orders: List[Order] = self._load()

    def _load(self) -> List[Order]:
        if not self._data_path.exists():
            raise FileNotFoundError(f"Seed data missing at {self._data_path}")
        raw_payload = json.loads(self._data_path.read_text())
        return [Order.from_dict(item) for item in raw_payload]

    def list_orders(self) -> List[Order]:
        with self._lock:
            return list(self._orders)

    def add_order(self, order: Order) -> Order:
        with self._lock:
            self._orders.append(order)
            return order

    def refresh(self) -> None:
        with self._lock:
            self._orders = self._load()
