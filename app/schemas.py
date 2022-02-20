from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Mapping


@dataclass(frozen=True)
class Order:
    order_id: str
    region: str
    category: str
    units: int
    revenue: float
    order_ts: datetime

    @staticmethod
    def from_dict(payload: Mapping[str, Any]) -> "Order":
        try:
            ts_raw = payload["order_ts"]
            timestamp = (
                datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                if isinstance(ts_raw, str)
                else datetime.utcfromtimestamp(ts_raw)
            )
            return Order(
                order_id=str(payload["order_id"]),
                region=str(payload["region"]),
                category=str(payload["category"]),
                units=int(payload["units"]),
                revenue=float(payload["revenue"]),
                order_ts=timestamp,
            )
        except KeyError as exc:  # pragma: no cover - defensive programming
            raise ValueError(f"Missing required field: {exc.args[0]}") from exc

    def to_dict(self) -> Dict[str, Any]:
        return {
            "order_id": self.order_id,
            "region": self.region,
            "category": self.category,
            "units": self.units,
            "revenue": self.revenue,
            "order_ts": self.order_ts.isoformat(),
        }
