from etl.extract.raw_loader import load_raw
from etl.load.save_csv import save_dim, save_fact

from etl.transform.dim_channel import build_dim_channel
from etl.transform.dim_address import build_dim_address
from etl.transform.dim_store import build_dim_store
from etl.transform.dim_product import build_dim_product
from etl.transform.dim_customer import build_dim_customer
from etl.transform.dim_date import build_dim_date
from etl.transform.fact_sales_order_item import build_fact_sales_order_item


def main():
    dfs = load_raw()

    # ✅ DIM CHANNEL
    dim_channel = build_dim_channel(dfs["channel"])
    save_dim(dim_channel, "dim_channel")

    # ✅ DIM ADDRESS (address + province)
    dim_address = build_dim_address(
        dfs["address"],
        dfs["province"]
    )
    save_dim(dim_address, "dim_address")

    # ✅ DIM STORE (store + address + province) — SOLO CRUDOS
    dim_store = build_dim_store(
        dfs["store"],
        dfs["address"],
        dfs["province"]
    )
    save_dim(dim_store, "dim_store")

    # ✅ DIM PRODUCT (producto + categoría + parent categoría)
    dim_product = build_dim_product(
        dfs["product"],
        dfs["product_category"]
    )
    save_dim(dim_product, "dim_product")

    # ✅ DIM CUSTOMER
    dim_customer = build_dim_customer(dfs["customer"])
    save_dim(dim_customer, "dim_customer")

    # ✅ DIM DATE con surrogate key (date_sk)
    dim_date = build_dim_date(dfs)
    save_dim(dim_date, "dim_date")

    # ✅ FACT (usa store_sk, address_sk, product_sk, customer_sk y date_sk)
    fact_soi = build_fact_sales_order_item(
        dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address, dim_product
    )
    save_fact(fact_soi, "fact_sales_order_item")

    print("✅ DW actualizado (STAR SCHEMA) generado en warehouse/dim y warehouse/fact")


if __name__ == "__main__":
    main()
