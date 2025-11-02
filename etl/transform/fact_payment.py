import pandas as pd

def build_fact_payment(dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address):

    pay = dfs["payment"].copy()

    # Traer datos del order (customer, channel, store, billing_address)
    so = dfs["sales_order"][["order_id","customer_id","channel_id","store_id","billing_address_id"]].copy()
    pay = pay.merge(so, on="order_id", how="left", validate="m:1")

    # Fecha → date_key manejando nulos
    pay["paid_at"] = pd.to_datetime(pay["paid_at"], errors="coerce")
    pay["paid_date_key"] = (
        pay["paid_at"]
            .dt.strftime("%Y%m%d")
            .fillna("0")
            .astype(int)
    )

    # Lookups para surrogate keys
    cust_lkp = dict(zip(dim_customer["customer_id"], dim_customer["customer_sk"]))
    chan_lkp = dict(zip(dim_channel["channel_id"],  dim_channel["channel_sk"]))
    store_lkp= dict(zip(dim_store["store_id"],     dim_store["store_sk"]))
    addr_lkp = dict(zip(dim_address["address_id"], dim_address["address_sk"]))
    date_lkp = dict(zip(dim_date["date_key"], dim_date["date_sk"]))

    pay["customer_sk"] = pay["customer_id"].map(cust_lkp)
    pay["channel_sk"]  = pay["channel_id"].map(chan_lkp)
    pay["store_sk"]    = pay["store_id"].map(store_lkp)
    pay["bill_addr_sk"]= pay["billing_address_id"].map(addr_lkp)
    pay["paid_date_sk"]= pay["paid_date_key"].map(date_lkp)

    # Columnas finales
    keep = [
        "payment_id","order_id",
        "paid_date_sk",
        "customer_sk","channel_sk","store_sk","bill_addr_sk",
        "amount","status","method","transaction_ref"
    ]

    return pay[keep]
