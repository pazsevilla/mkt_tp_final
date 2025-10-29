from etl.extract.raw_loader import load_raw
from etl.load.save_csv import save_dim, save_fact

from etl.transform.dim_channel import build_dim_channel
from etl.transform.dim_province import build_dim_province
from etl.transform.dim_address import build_dim_address
from etl.transform.dim_store import build_dim_store
from etl.transform.dim_product_category import build_dim_product_category
from etl.transform.dim_product import build_dim_product
from etl.transform.dim_customer import build_dim_customer
from etl.transform.dim_date import build_dim_date
from etl.transform.fact_sales_order_item import build_fact_sales_order_item

def main():
    dfs = load_raw()

    # DIMs
    dim_channel   = build_dim_channel(dfs["channel"])
    dim_province  = build_dim_province(dfs["province"])
    dim_address   = build_dim_address(dfs["address"], dim_province)
    dim_store     = build_dim_store(dfs["store"], dim_address)
    dim_category  = build_dim_product_category(dfs["product_category"])
    dim_product   = build_dim_product(dfs["product"], dim_category)
    dim_customer  = build_dim_customer(dfs["customer"])
    dim_date      = build_dim_date(dfs)

    # Save DIMs
    save_dim(dim_channel, "dim_channel")
    save_dim(dim_province, "dim_province")
    save_dim(dim_address, "dim_address")
    save_dim(dim_store, "dim_store")
    save_dim(dim_category, "dim_product_category")
    save_dim(dim_product, "dim_product")
    save_dim(dim_customer, "dim_customer")
    save_dim(dim_date, "dim_date")

    # FACT
    fact_soi = build_fact_sales_order_item(
        dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address, dim_product
    )

    # chequeo simple de integridad
    for col in ["customer_sk","channel_sk","product_sk","order_date_key"]:
        assert fact_soi[col].notna().all(), f"FK nula detectada en {col}"

    save_fact(fact_soi, "fact_sales_order_item")
    print("✅ DW completo generado en warehouse/dim y warehouse/fact")

if __name__ == "__main__":
    main()
