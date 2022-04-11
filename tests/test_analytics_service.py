from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.analytics_service import SalesAnalyticsService
from app.data_repository import OrderRepository


@pytest.fixture()
def service(tmp_path: Path) -> SalesAnalyticsService:
    seed = Path(__file__).resolve().parents[1] / "app" / "data" / "sample_orders.json"
    data = json.loads(seed.read_text())
    data_path = tmp_path / "orders.json"
    data_path.write_text(json.dumps(data))
    repository = OrderRepository(data_path)
    return SalesAnalyticsService(repository)


def test_revenue_summary(service: SalesAnalyticsService) -> None:
    summary = service.revenue_summary()
    assert summary["records"] == 10
    assert summary["total_revenue"] > 50000
    assert summary["top_region"]["name"] in {"us-east", "eu-central"}


def test_create_order_updates_forecast(service: SalesAnalyticsService) -> None:
    new_order = {
        "order_id": "A9999",
        "region": "eu-central",
        "category": "ai-platform",
        "units": 300,
        "revenue": 15000,
        "order_ts": "2024-02-10T10:00:00Z",
    }
    service.create_order(new_order)
    forecast = service.forecast_next_order()
    assert forecast["predicted_units"] >= 200
    assert forecast["predicted_revenue"] >= 9000
