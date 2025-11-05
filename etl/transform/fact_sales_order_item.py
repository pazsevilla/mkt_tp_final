import pandas as pd

def build_fact_sales_order_item(dfs, dim_date, dim_customer, dim_channel,
                                dim_store, dim_address, dim_product):

    soi = dfs["sales_order_item"].copy()
    so  = dfs["sales_order"].copy()

    # ===== Fecha -> date_key (para lookup) =====
    so["order_date"]     = pd.to_datetime(so["order_date"], errors="coerce")
    so["order_date_key"] = so["order_date"].dt.strftime("%Y%m%d").fillna("0").astype(int)

    # ===== Lookups naturales -> SKs =====
    cust_lkp = dict(zip(dim_customer["customer_id"], dim_customer["customer_sk"]))
    chan_lkp = dict(zip(dim_channel["channel_id"],  dim_channel["channel_sk"]))
    store_lkp= dict(zip(dim_store["store_id"],     dim_store["store_sk"]))
    addr_lkp = dict(zip(dim_address["address_id"], dim_address["address_sk"]))
    prod_lkp = dict(zip(dim_product["product_id"], dim_product["product_sk"]))
    date_lkp = dict(zip(dim_date["date_key"],      dim_date["date_sk"]))

    # ===== Join cabecera de la orden =====
    fact = soi.merge(
        so[[
            "order_id","customer_id","channel_id","store_id",
            "shipping_address_id","billing_address_id","order_date_key",
            "status","currency_code","subtotal","tax_amount","shipping_fee","total_amount"
        ]],
        on="order_id", how="left", validate="m:1"
    )

    # ===== Surrogate key del fact =====
    fact = fact.reset_index(drop=True)
    fact["order_item_sk"] = (fact.index + 1).astype("Int64")

    # ===== Map natural keys -> surrogate keys (todas INT) =====
    fact["customer_sk"]   = fact["customer_id"].map(cust_lkp).astype("Int64")
    fact["channel_sk"]    = fact["channel_id"].map(chan_lkp).astype("Int64")
    fact["store_sk"]      = fact["store_id"].map(store_lkp).astype("Int64")
    fact["ship_addr_sk"]  = fact["shipping_address_id"].map(addr_lkp).astype("Int64")
    fact["bill_addr_sk"]  = fact["billing_address_id"].map(addr_lkp).astype("Int64")
    fact["product_sk"]    = fact["product_id"].map(prod_lkp).astype("Int64")
    fact["order_date_sk"] = fact["order_date_key"].map(date_lkp).astype("Int64")

    # Flag útil
    fact["is_paid_or_fulfilled"] = fact["status"].isin(["PAID", "FULFILLED"]).astype("Int64")

    # ===== Columnas finales (sin order_id, sin order_item_id natural) =====
    keep = [
        "order_item_sk",          # ✅ surrogate key
        "order_date_sk",          # ✅ Int64
        "customer_sk","channel_sk","store_sk",
        "bill_addr_sk",
        "product_sk",
        "quantity","unit_price","discount_amount","line_total"
    ]

    return fact[keep]
