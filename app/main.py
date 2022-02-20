from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, request

from .analytics_service import SalesAnalyticsService
from .data_repository import OrderRepository


def create_app(test_config: Dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(test_config or {})

    data_path = Path(app.config.get("DATA_PATH", Path(__file__).parent / "data" / "sample_orders.json"))
    repository = OrderRepository(data_path=data_path)
    service = SalesAnalyticsService(repository)

    @app.route("/health", methods=["GET"])
    def health() -> Any:
        return jsonify({"status": "ok"}), 200

    @app.route("/orders", methods=["GET"])
    def list_orders() -> Any:
        return jsonify({"orders": service.list_orders()}), 200

    @app.route("/orders", methods=["POST"])
    def create_order() -> Any:
        payload = request.get_json(force=True, silent=True) or {}
        try:
            created = service.create_order(payload)
        except ValueError as err:
            return jsonify({"error": str(err)}), 400
        return jsonify(created), 201

    @app.route("/analytics/summary", methods=["GET"])
    def analytics_summary() -> Any:
        return jsonify(service.revenue_summary()), 200

    @app.route("/analytics/regions", methods=["GET"])
    def regions_breakdown() -> Any:
        return jsonify({"regions": service.revenue_by_region()}), 200

    @app.route("/analytics/forecast", methods=["GET"])
    def forecast() -> Any:
        return jsonify(service.forecast_next_order()), 200

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=8080)
