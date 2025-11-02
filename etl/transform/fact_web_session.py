import pandas as pd

def build_fact_web_session(dfs, dim_date, dim_customer, dim_channel):

    ws = dfs["web_session"].copy()

    # ===== SURROGATE KEY FACT =====
    ws = ws.reset_index(drop=True)
    ws["session_sk"] = (ws.index + 1).astype("Int64")

    # ===== FECHAS =====
    ws["started_at"] = pd.to_datetime(ws.get("started_at"), errors="coerce")
    ws["ended_at"]   = pd.to_datetime(ws.get("ended_at"),   errors="coerce")

    # Fecha natural YYYYMMDD
    ws["started_date_key"] = ws["started_at"].dt.strftime("%Y%m%d").fillna("0").astype(int)
    ws["ended_date_key"]   = ws["ended_at"].dt.strftime("%Y%m%d").fillna("0").astype(int)

    # Hora HH:MM:SS
    ws["started_time"] = ws["started_at"].dt.strftime("%H:%M:%S")
    ws["ended_time"]   = ws["ended_at"].dt.strftime("%H:%M:%S")

    # ===== LOOKUPS DATE → SK =====
    date_lkp = dict(zip(dim_date["date_key"], dim_date["date_sk"]))

    ws["started_date_id"] = ws["started_date_key"].map(date_lkp).astype("Int64")
    ws["ended_date_id"]   = ws["ended_date_key"].map(date_lkp).astype("Int64")

    # ===== LOOKUP CUSTOMER → SK =====
    if "customer_id" in ws.columns:
        cust_lkp = dict(zip(dim_customer["customer_id"], dim_customer["customer_sk"]))
        ws["customer_sk"] = ws["customer_id"].map(cust_lkp).astype("Int64")
    else:
        ws["customer_sk"] = pd.NA

    # ===== LOOKUP CHANNEL (según source) =====
    chan_by_code = {str(c).strip().lower(): sk for c, sk in zip(dim_channel["code"],  dim_channel["channel_sk"])}
    chan_by_name = {str(n).strip().lower(): sk for n, sk in zip(dim_channel["name"],  dim_channel["channel_sk"])}

    def map_source_to_sk(val):
        if pd.isna(val): 
            return None
        key = str(val).strip().lower()
        return chan_by_code.get(key, chan_by_name.get(key))

    ws["channel_sk"] = ws["source"].map(map_source_to_sk).astype("Int64")

    # ===== COLUMNAS FINALES =====
    keep = [
        "session_sk",          # ✅ surrogate key final
        "started_date_id",     # ✅ surrogate key dim_date
        "ended_date_id",       # ✅ surrogate key dim_date
        "started_time",
        "ended_time",
        "customer_sk",
        "channel_sk",
        "device"
    ]

    return ws[keep]
