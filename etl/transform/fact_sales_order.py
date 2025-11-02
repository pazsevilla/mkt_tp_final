import pandas as pd

def build_fact_sales_order(dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address):

    so = dfs["sales_order"].copy()

    # ===== Surrogate key =====
    so = so.reset_index(drop=True)
    so["order_sk"] = (so.index + 1).astype("Int64")  # ✅ surrogate key de la fact

    # ===== Convertir fecha =====
    so["order_date"] = pd.to_datetime(so["order_date"], errors="coerce")
    so["order_date_key"] = so["order_date"].dt.strftime("%Y%m%d").fillna("0").astype(int)

    # ===== Lookups naturales → SK =====
    cust_lkp = dict(zip(dim_customer["customer_id"], dim_customer["customer_sk"]))
    chan_lkp = dict(zip(dim_channel["channel_id"],  dim_channel["channel_sk"]))
    store_lkp= dict(zip(dim_store["store_id"],     dim_store["store_sk"]))
    addr_lkp = dict(zip(dim_address["address_id"], dim_address["address_sk"]))
    date_lkp = dict(zip(dim_date["date_key"],      dim_date["date_sk"]))

    # Map de FK → SK
    so["customer_sk"]  = so["customer_id"].map(cust_lkp).astype("Int64")
    so["channel_sk"]   = so["channel_id"].map(chan_lkp).astype("Int64")
    so["store_sk"]     = so["store_id"].map(store_lkp).astype("Int64")         # ✅ ahora int
    so["ship_addr_sk"] = so["shipping_address_id"].map(addr_lkp).astype("Int64")
    so["bill_addr_sk"] = so["billing_address_id"].map(addr_lkp).astype("Int64") # ✅ ahora int
    so["order_date_sk"]= so["order_date_key"].map(date_lkp).astype("Int64")

    # ===== Columnas finales =====
    keep = [
        "order_sk",             # ✅ surrogate key
        "order_date_sk",        # ✅ int
        "customer_sk","channel_sk","store_sk",
        "ship_addr_sk","bill_addr_sk",
        "status","currency_code",
        "subtotal","tax_amount","shipping_fee","total_amount"
    ]

    return so[keep]
