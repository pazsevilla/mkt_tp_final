import pandas as pd

def build_fact_shipment(dfs, dim_date, dim_customer, dim_channel, dim_store, dim_address):
    ship = dfs["shipment"].copy()

    # Join con sales_order para traer customer/channel/store/shipping_address
    so_cols = ["order_id", "customer_id", "channel_id", "store_id", "shipping_address_id"]
    so = dfs["sales_order"][so_cols].copy()
    ship = ship.merge(so, on="order_id", how="left", validate="m:1")

    # ===== Surrogate key de la fact =====
    ship = ship.reset_index(drop=True)
    ship["shipment_sk"] = (ship.index + 1).astype("Int64")

    # ===== Fechas -> date_key (YYYYMMDD) =====
    ship["shipped_at"]   = pd.to_datetime(ship.get("shipped_at"),   errors="coerce")
    ship["delivered_at"] = pd.to_datetime(ship.get("delivered_at"), errors="coerce")

    ship["shipped_date_key"] = (
        ship["shipped_at"].dt.strftime("%Y%m%d").fillna("0").astype(int)
    )
    ship["delivered_date_key"] = (
        ship["delivered_at"].dt.strftime("%Y%m%d").fillna("0").astype(int)
    )

    # ===== Lookups natural -> SK =====
    cust_lkp = dict(zip(dim_customer["customer_id"], dim_customer["customer_sk"]))
    chan_lkp = dict(zip(dim_channel["channel_id"],  dim_channel["channel_sk"]))
    store_lkp= dict(zip(dim_store["store_id"],     dim_store["store_sk"]))
    addr_lkp = dict(zip(dim_address["address_id"], dim_address["address_sk"]))
    date_lkp = dict(zip(dim_date["date_key"],      dim_date["date_sk"]))

    ship["customer_sk"] = ship["customer_id"].map(cust_lkp).astype("Int64")
    ship["channel_sk"]  = ship["channel_id"].map(chan_lkp).astype("Int64")
    ship["store_sk"]    = ship["store_id"].map(store_lkp).astype("Int64")

    # Si no vino shipping_address_id desde sales_order, usamos el de shipment si existe
    if "shipping_address_id" not in ship.columns and "address_id" in ship.columns:
        ship = ship.rename(columns={"address_id": "shipping_address_id"})
    ship["ship_addr_sk"] = ship["shipping_address_id"].map(addr_lkp).astype("Int64")

    ship["shipped_date_sk"]   = ship["shipped_date_key"].map(date_lkp).astype("Int64")
    ship["delivered_date_sk"] = ship["delivered_date_key"].map(date_lkp).astype("Int64")

    # ===== Columnas finales =====
    base_keep = [
        "shipment_sk",                 # <- surrogate key
        "shipped_date_sk", "delivered_date_sk",
        "customer_sk", "channel_sk", "store_sk", "ship_addr_sk",
    ]

    optional = [
        "status",
        "shipping_method",
        "carrier",
        "tracking_number",
        "shipping_cost",
    ]

    keep = base_keep + [c for c in optional if c in ship.columns]
    return ship[keep]
