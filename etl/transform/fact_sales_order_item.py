import pandas as pd

def build_fact_sales_order_item(dfs, dim_date, dim_customer, dim_channel,
                                dim_store, dim_address, dim_product):
    soi = dfs["sales_order_item"].copy()
    so  = dfs["sales_order"].copy()

    so["order_date"] = pd.to_datetime(so["order_date"], errors="coerce")
    so["order_date_key"] = so["order_date"].dt.strftime("%Y%m%d").astype(int)

    # lookups naturales → SK
    cust_lkp = dict(zip(dim_customer["customer_id"], dim_customer["customer_sk"]))
    chan_lkp = dict(zip(dim_channel["channel_id"],  dim_channel["channel_sk"]))
    store_lkp= dict(zip(dim_store["store_id"],     dim_store["store_sk"]))
    addr_lkp = dict(zip(dim_address["address_id"], dim_address["address_sk"]))
    prod_lkp = dict(zip(dim_product["product_id"], dim_product["product_sk"]))

    fact = soi.merge(so, on="order_id", how="left", validate="m:1")

    fact["customer_sk"]  = fact["customer_id"].map(cust_lkp)
    fact["channel_sk"]   = fact["channel_id"].map(chan_lkp)
    fact["store_sk"]     = fact["store_id"].map(store_lkp)
    fact["ship_addr_sk"] = fact["shipping_address_id"].map(addr_lkp)
    fact["bill_addr_sk"] = fact["billing_address_id"].map(addr_lkp)
    fact["product_sk"]   = fact["product_id"].map(prod_lkp)
    fact["order_date_key"] = fact["order_date_key"]

    fact["is_paid_or_fulfilled"] = fact["status"].isin(["PAID","FULFILLED"]).astype(int)

    keep = [
        "order_item_id","order_id",
        "order_date_key",
        "customer_sk","channel_sk","store_sk",
        "bill_addr_sk","ship_addr_sk",
        "product_sk",
        "quantity","unit_price","discount_amount","line_total",
        "status","currency_code","subtotal","tax_amount","shipping_fee","total_amount",
        "is_paid_or_fulfilled"
    ]
    return fact[keep]
