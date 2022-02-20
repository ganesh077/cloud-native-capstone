from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean
from typing import Any, Dict, List, Sequence

from .data_repository import OrderRepository
from .schemas import Order


class SalesAnalyticsService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def list_orders(self) -> List[Dict[str, Any]]:
        return [order.to_dict() for order in self._repository.list_orders()]

    def create_order(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        order = Order.from_dict(payload)
        created = self._repository.add_order(order)
        return created.to_dict()

    def revenue_summary(self) -> Dict[str, Any]:
        orders = self._repository.list_orders()
        total_revenue = sum(order.revenue for order in orders)
        total_units = sum(order.units for order in orders)
        average_order_value = total_revenue / len(orders) if orders else 0.0
        avg_units = total_units / len(orders) if orders else 0.0

        top_region = self._top_key(orders, key_attr="region", metric_attr="revenue")
        top_category = self._top_key(orders, key_attr="category", metric_attr="revenue")

        return {
            "records": len(orders),
            "total_revenue": round(total_revenue, 2),
            "total_units": total_units,
            "average_order_value": round(average_order_value, 2),
            "average_units_per_order": round(avg_units, 2),
            "top_region": top_region,
            "top_category": top_category,
        }

    def revenue_by_region(self) -> List[Dict[str, Any]]:
        aggregates: Dict[str, Dict[str, float]] = defaultdict(lambda: {"revenue": 0.0, "units": 0})
        for order in self._repository.list_orders():
            aggregates[order.region]["revenue"] += order.revenue
            aggregates[order.region]["units"] += order.units

        response: List[Dict[str, Any]] = []
        for region, metrics in aggregates.items():
            response.append(
                {
                    "region": region,
                    "revenue": round(metrics["revenue"], 2),
                    "units": metrics["units"],
                }
            )
        response.sort(key=lambda item: item["revenue"], reverse=True)
        return response

    def forecast_next_order(self) -> Dict[str, Any]:
        """Simple heuristic forecast that averages the last 3 orders."""
        orders = sorted(self._repository.list_orders(), key=lambda o: o.order_ts)
        tail = orders[-3:]
        if not tail:
            return {"predicted_units": 0, "predicted_revenue": 0.0}

        predicted_units = mean(order.units for order in tail)
        predicted_revenue = mean(order.revenue for order in tail)
        return {
            "predicted_units": round(predicted_units, 2),
            "predicted_revenue": round(predicted_revenue, 2),
        }

    def _top_key(
        self, orders: Sequence[Order], *, key_attr: str, metric_attr: str
    ) -> Dict[str, Any] | None:
        if not orders:
            return None
        counter = Counter()
        metrics: Dict[str, float] = defaultdict(float)
        for order in orders:
            key = getattr(order, key_attr)
            metric = getattr(order, metric_attr)
            counter[key] += 1
            metrics[key] += metric
        best_key = max(metrics, key=lambda item: metrics[item])
        return {
            "name": best_key,
            "orders": counter[best_key],
            metric_attr: round(metrics[best_key], 2),
        }
