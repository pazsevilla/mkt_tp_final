from etl.extract.raw_loader import load_raw
from etl.load.save_csv import save_dim, save_fact

# DIMs
from etl.transform.dim_channel import build_dim_channel
from etl.transform.dim_address import build_dim_address
from etl.transform.dim_store import build_dim_store
from etl.transform.dim_product import build_dim_product
from etl.transform.dim_customer import build_dim_customer
from etl.transform.dim_date import build_dim_date

# FACTS
from etl.transform.fact_sales_order_item import build_fact_sales_order_item
from etl.transform.fact_sales_order import build_fact_sales_order
from etl.transform.fact_payment import build_fact_payment
from etl.transform.fact_shipment import build_fact_shipment
from etl.transform.fact_web_session import build_fact_web_session
from etl.transform.fact_nps_response import build_fact_nps_response


def main():
    dfs = load_raw()

    # ======================
    # DIMENSIONS
    # ======================
    dim_channel = build_dim_channel(dfs["channel"])
    save_dim(dim_channel, "dim_channel")

    dim_address = build_dim_address(dfs["address"], dfs["province"])
    save_dim(dim_address, "dim_address")

    dim_store = build_dim_store(dfs["store"], dfs["address"], dfs["province"])
    save_dim(dim_store, "dim_store")

    dim_product = build_dim_product(dfs["product"], dfs["product_category"])
    save_dim(dim_product, "dim_product")

    dim_customer = build_dim_customer(dfs["customer"])
    save_dim(dim_customer, "dim_customer")

    dim_date = build_dim_date(dfs)
    save_dim(dim_date, "dim_date")

    # ======================
    # FACTS
    # ======================

    fact_soi = build_fact_sales_order_item(
        dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address, dim_product
    )
    save_fact(fact_soi, "fact_sales_order_item")

    fact_sales_order = build_fact_sales_order(
        dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address
    )
    save_fact(fact_sales_order, "fact_sales_order")

    fact_payment = build_fact_payment(
        dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address
    )
    save_fact(fact_payment, "fact_payment")

    fact_shipment = build_fact_shipment(
        dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address
    )
    save_fact(fact_shipment, "fact_shipment")

    fact_web_session = build_fact_web_session(
        dfs, dim_date, dim_customer, dim_channel
    )
    save_fact(fact_web_session, "fact_web_session")

    fact_nps = build_fact_nps_response(
        dfs, dim_date, dim_customer, dim_channel
    )
    save_fact(fact_nps, "fact_nps_response")

    print("✅ DW (STAR SCHEMA) generado: dimensiones y hechos exportados a warehouse/")


if __name__ == "__main__":
    main()

