import pandas as pd

def build_fact_web_session(dfs, dim_date, dim_customer, dim_channel):
    ws = dfs["web_session"].copy()

    # fechas
    ws["started_at"] = pd.to_datetime(ws.get("started_at"), errors="coerce")
    ws["date_key"] = ws["started_at"].dt.strftime("%Y%m%d").fillna("0").astype(int)

    # lookups
    cust_lkp = dict(zip(dim_customer["customer_id"], dim_customer["customer_sk"]))
    date_lkp = dict(zip(dim_date["date_key"],      dim_date["date_sk"]))

    # channel: mapear 'source' a channel por code o name (case-insensitive)
    chan_by_code = {str(c).strip().lower(): sk for c, sk in zip(dim_channel["code"],  dim_channel["channel_sk"])}
    chan_by_name = {str(n).strip().lower(): sk for n, sk in zip(dim_channel["name"],  dim_channel["channel_sk"])}

    def map_source_to_sk(val):
        if pd.isna(val):
            return None
        key = str(val).strip().lower()
        return chan_by_code.get(key, chan_by_name.get(key))

    ws["customer_sk"] = ws["customer_id"].map(cust_lkp) if "customer_id" in ws.columns else None
    ws["channel_sk"]  = ws["source"].map(map_source_to_sk) if "source" in ws.columns else None
    ws["date_sk"]     = ws["date_key"].map(date_lkp)

    base_keep = ["session_id","date_sk","customer_sk","channel_sk"]
    optional = ["started_at","ended_at","source","device"]
    keep = [c for c in base_keep if c in ws.columns] + [c for c in optional if c in ws.columns]

    # asegurar PK
    if "session_id" not in ws.columns:
        ws["session_id"] = range(1, len(ws)+1)

    return ws[keep]

