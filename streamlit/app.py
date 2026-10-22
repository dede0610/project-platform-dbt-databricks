import os

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
st.header("Browse curated customer data")

app_name = os.getenv("DATABRICKS_APP_NAME", "")
if app_name.endswith("-dev") or app_name.endswith("-local"):
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
def load_customers(catalog: str, warehouse_id: str) -> pd.DataFrame:
    config = Config()
    if not config.host:
        raise RuntimeError("DATABRICKS_HOST is not configured.")

    with sql.connect(
        server_hostname=config.host.removeprefix("https://").rstrip("/"),
        http_path=f"/sql/1.0/warehouses/{warehouse_id}",
        credentials_provider=lambda: config.authenticate,
    ) as connection:
        with connection.cursor() as cursor:
            escaped_catalog = catalog.replace("`", "``")
            cursor.execute(f"SELECT * FROM `{escaped_catalog}`.`curated`.`customers`")
            columns = [column[0] for column in cursor.description]
            return pd.DataFrame(cursor.fetchall(), columns=columns)


st.subheader("Customers")
customers = load_customers(
    catalog=catalog,
    warehouse_id=os.getenv(
        "DATABRICKS_WAREHOUSE_ID", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    ),
)

total_customers = len(customers)
lifetime_revenue = (
    pd.to_numeric(customers["lifetime_spend"], errors="coerce").fillna(0).sum()
    if "lifetime_spend" in customers
    else 0
)
average_lifetime_spend = lifetime_revenue / total_customers if total_customers else 0
returning_customers = (
    customers["customer_type"].eq("returning").sum()
    if "customer_type" in customers
    else 0
)
returning_customer_rate = (
    returning_customers / total_customers * 100 if total_customers else 0
)

metric_columns = st.columns(4)
metric_columns[0].metric("Total customers", f"{total_customers:,}")
metric_columns[1].metric("Lifetime revenue", f"${lifetime_revenue:,.2f}")
metric_columns[2].metric("Avg. lifetime spend", f"${average_lifetime_spend:,.2f}")
metric_columns[3].metric(
    "Returning customers",
    f"{returning_customers:,}",
    f"{returning_customer_rate:.1f}%",
)

st.subheader("Customer details")
st.dataframe(customers, use_container_width=True, hide_index=True)
