import pandas as pd

def build_fact_nps_response(dfs, dim_date, dim_customer, dim_channel):
    nps = dfs["nps_response"].copy()

    # fechas
    nps["responded_at"] = pd.to_datetime(nps.get("responded_at"), errors="coerce")
    nps["date_key"] = nps["responded_at"].dt.strftime("%Y%m%d").fillna("0").astype(int)

    # lookups
    cust_lkp = dict(zip(dim_customer["customer_id"], dim_customer["customer_sk"]))
    chan_lkp = dict(zip(dim_channel["channel_id"],  dim_channel["channel_sk"]))
    date_lkp = dict(zip(dim_date["date_key"],      dim_date["date_sk"]))

    nps["customer_sk"] = nps["customer_id"].map(cust_lkp) if "customer_id" in nps.columns else None
    nps["channel_sk"]  = nps["channel_id"].map(chan_lkp)  if "channel_id"  in nps.columns else None
    nps["date_sk"]     = nps["date_key"].map(date_lkp)

    keep = ["nps_id","customer_sk","channel_sk","date_sk","score","comment"]
    keep = [c for c in keep if c in nps.columns]  # tolerante

    return nps[keep]
