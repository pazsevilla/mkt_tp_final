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

    # DIMs
    dim_channel  = build_dim_channel(dfs["channel"])
    dim_address  = build_dim_address(dfs["address"], dfs["province"])
    dim_store    = build_dim_store(dfs["store"], dim_address)
    dim_product  = build_dim_product(dfs["product"], dfs["product_category"])
    dim_customer = build_dim_customer(dfs["customer"])
    dim_date     = build_dim_date(dfs)  # ahora con date_sk

    # Guardar DIMs
    save_dim(dim_channel,  "dim_channel")
    save_dim(dim_address,  "dim_address")
    save_dim(dim_store,    "dim_store")
    save_dim(dim_product,  "dim_product")
    save_dim(dim_customer, "dim_customer")
    save_dim(dim_date,     "dim_date")

    # FACT (usa date_sk en vez de date_key)
    fact_soi = build_fact_sales_order_item(
        dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address, dim_product
    )

    # chequeo rápido
    for col in ["customer_sk","channel_sk","product_sk","order_date_sk"]:
        assert fact_soi[col].notna().all(), f"FK nula detectada en {col}"

    save_fact(fact_soi, "fact_sales_order_item")
    print("✅ DW (star schema) generado en warehouse/dim y warehouse/fact")

if __name__ == "__main__":
    main()
