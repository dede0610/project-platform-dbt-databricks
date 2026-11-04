import os
from typing import Literal

import pandas as pd
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config

st.set_page_config(page_title="Curated Data Browser", layout="wide")
app_name = os.getenv("DATABRICKS_APP_NAME", "streamlit-app-local")
st.markdown(
    f"<h1 style='color:#A80876;'>{app_name}</h1>",
    unsafe_allow_html=True,
)
st.header("Jaffle Shop performance")

app_name = os.getenv("DATABRICKS_APP_NAME", "")
if app_name.endswith(("-dev", "-local")):
    catalog = "dev_dbt"
elif app_name.endswith("-tst"):
    catalog = "tst_dbt"
elif app_name.endswith("-prd"):
    catalog = "prd_dbt"
else:
    raise ValueError(f"Unsupported or missing DATABRICKS_APP_NAME: {app_name!r}")

st.write("Catalog used:", catalog)
st.write("Schema used:", "curated")


@st.cache_data(ttl=60)
def load_mart(
    catalog: str,
    warehouse_id: str,
    mart: Literal["orders", "order_items", "customers"],
) -> pd.DataFrame:
    selected_columns = {
        "orders": "order_id, customer_id, order_date, order_total, customer_order_number",
        "order_items": ("product_name, product_price, is_food_item, is_drink_item"),
        "customers": (
            "customer_id, customer_name, count_lifetime_orders, first_order_date, "
            "last_order_date, lifetime_spend, customer_type"
        ),
    }
    config = Config()
    if not config.host:
        raise RuntimeError("DATABRICKS_HOST is not configured.")

    with (
        sql.connect(
            server_hostname=config.host.removeprefix("https://").rstrip("/"),
            http_path=f"/sql/1.0/warehouses/{warehouse_id}",
            credentials_provider=lambda: config.authenticate,
        ) as connection,
        connection.cursor() as cursor,
    ):
        escaped_catalog = catalog.replace("`", "``")
        cursor.execute(
            f"SELECT {selected_columns[mart]} "
            f"FROM `{escaped_catalog}`.`curated`.`{mart}`"
        )
        description = cursor.description
        if description is None:
            raise RuntimeError(f"{mart} query did not return a result set.")

        result_columns = [str(column[0]) for column in description]
        return pd.DataFrame(cursor.fetchall(), columns=pd.Index(result_columns))


warehouse_id = os.getenv(
    "DATABRICKS_WAREHOUSE_ID", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
)
orders = load_mart(
    catalog=catalog,
    warehouse_id=warehouse_id,
    mart="orders",
)
order_items = load_mart(catalog=catalog, warehouse_id=warehouse_id, mart="order_items")

orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
orders["order_total"] = pd.to_numeric(orders["order_total"], errors="coerce")
order_items["product_price"] = pd.to_numeric(
    order_items["product_price"], errors="coerce"
)
order_items["product_category"] = "Other"
order_items.loc[order_items["is_food_item"].fillna(False), "product_category"] = "Food"
order_items.loc[order_items["is_drink_item"].fillna(False), "product_category"] = (
    "Drink"
)

total_orders = len(orders)
total_sales = orders["order_total"].sum()
average_order_value = total_sales / total_orders if total_orders else 0
repeat_buyers = orders.loc[orders["customer_order_number"] > 1, "customer_id"].nunique()
total_buyers = orders["customer_id"].nunique()
repeat_buyer_rate = repeat_buyers / total_buyers * 100 if total_buyers else 0

st.subheader("Sales at a glance")
metric_columns = st.columns(4)
metric_columns[0].metric("Total sales", f"${total_sales:,.2f}")
metric_columns[1].metric("Orders", f"{total_orders:,}")
metric_columns[2].metric("Average order value", f"${average_order_value:,.2f}")
metric_columns[3].metric("Repeat buyer rate", f"{repeat_buyer_rate:.1f}%")

st.subheader("Sales over time")
monthly_sales = (
    orders.dropna(subset=["order_date"])
    .assign(month=lambda frame: frame["order_date"].dt.to_period("M").astype(str))
    .groupby("month", as_index=True)["order_total"]
    .sum()
    .rename("Sales")
)
if monthly_sales.empty:
    st.info("No dated orders are available to chart.")
else:
    st.line_chart(monthly_sales)

st.subheader("What customers are ordering")
item_column, product_column = st.columns(2)
sales_by_type = (
    order_items.groupby("product_category")["product_price"]
    .sum()
    .sort_values(ascending=False)
    .rename("Item sales (before tax)")
)
item_column.bar_chart(sales_by_type)

top_products = (
    order_items.groupby("product_name")["product_price"]
    .sum()
    .nlargest(10)
    .sort_values()
    .rename("Item sales (before tax)")
)
product_column.bar_chart(top_products)

with st.expander("Customer details"):
    customers = load_mart(catalog=catalog, warehouse_id=warehouse_id, mart="customers")
    st.dataframe(customers, use_container_width=True, hide_index=True)
