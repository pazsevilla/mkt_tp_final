import pandas as pd

def build_fact_nps_response(dfs, dim_date, dim_customer, dim_channel):
    nps = dfs["nps_response"].copy()

    # 1) Convertir responded_at a datetime
    nps["responded_at"] = pd.to_datetime(nps["responded_at"], errors="coerce")

    # 2) Surrogate key
    nps["nps_sk"] = range(1, len(nps) + 1)

    # 3) Dividir fecha y hora
    nps["responded_at_date_key"] = nps["responded_at"].dt.strftime("%Y%m%d").astype(int)
    nps["responded_at_time"] = nps["responded_at"].dt.strftime("%H:%M:%S")

    # 4) Lookups
    date_lkp = dim_date.set_index("date_key")["date_sk"].to_dict()
    cust_lkp = dim_customer.set_index("customer_id")["customer_sk"].to_dict()
    chan_lkp = dim_channel.set_index("channel_id")["channel_sk"].to_dict()

    # 5) Map natural keys → surrogate keys
    nps["responded_at_date_id"] = nps["responded_at_date_key"].map(date_lkp).astype("Int64")
    nps["customer_sk"] = nps["customer_id"].map(cust_lkp).astype("Int64")
    nps["channel_sk"] = nps["channel_id"].map(chan_lkp).astype("Int64")

    # 6) Columnas finales
    keep = [
        "nps_sk",
        "score",
        "comment",
        "responded_at_date_id",
        "responded_at_time",
        "customer_sk",
        "channel_sk"
    ]

    return nps[keep]
