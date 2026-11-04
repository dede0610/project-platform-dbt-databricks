from pathlib import Path
from types import SimpleNamespace
from typing import Self

from streamlit.testing.v1 import AppTest


class FakeCursor:
    def __init__(self) -> None:
        self.description: list[tuple[str]] | None = None
        self._rows: list[tuple[object, ...]] = []
        self.queries: list[str] = []

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def execute(self, query: str) -> None:
        self.queries.append(query)
        if query.endswith("`.`orders`"):
            self.description = [
                ("order_id",),
                ("customer_id",),
                ("order_total",),
                ("customer_order_number",),
            ]
            self._rows = [(1, 1, 10.0, 1), (2, 1, 20.0, 2), (3, 2, 30.0, 1)]
        elif query.endswith("`.`order_items`"):
            self.description = [
                ("product_name",),
                ("product_price",),
                ("is_food_item",),
                ("is_drink_item",),
            ]
            self._rows = [("Coffee", 5.0, False, True), ("Bagel", 3.0, True, False)]
        else:
            self.description = [
                ("customer_id",),
                ("customer_name",),
                ("count_lifetime_orders",),
                ("first_order_date",),
                ("last_order_date",),
                ("lifetime_spend",),
                ("customer_type",),
            ]
            self._rows = [(1, "Alice", 2, None, None, 30.0, "returning")]

    def fetchall(self) -> list[tuple[object, ...]]:
        return self._rows


class FakeConnection:
    def __init__(self, cursor: FakeCursor) -> None:
        self._cursor = cursor

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def cursor(self) -> FakeCursor:
        return self._cursor


def test_app_renders_metrics_using_environment_catalog(monkeypatch) -> None:
    import databricks.sdk.core
    import databricks.sql

    cursor = FakeCursor()
    monkeypatch.setattr(
        databricks.sdk.core,
        "Config",
        lambda: SimpleNamespace(host="https://workspace.example.com/"),
    )
    monkeypatch.setattr(
        databricks.sql,
        "connect",
        lambda **_: FakeConnection(cursor),
    )
    monkeypatch.setenv("DATABRICKS_APP_NAME", "store-dev")

    app_path = Path(__file__).parents[1] / "app.py"
    app = AppTest.from_file(str(app_path)).run()

    assert not app.exception
    assert {metric.label: metric.value for metric in app.metric} == {
        "Total sales": "$60.00",
        "Orders": "3",
        "Average order value": "$20.00",
        "Repeat buyer rate": "50.0%",
    }
    assert {query.rsplit(" FROM ", maxsplit=1)[-1] for query in cursor.queries} == {
        "`dev_dbt`.`curated`.`orders`",
        "`dev_dbt`.`curated`.`order_items`",
        "`dev_dbt`.`curated`.`customers`",
    }
