import pandas as pd

def build_dim_date(dfs: dict):
    cols = []
    so = dfs["sales_order"]
    cols.append(pd.to_datetime(so.get("order_date"), errors="coerce"))

    ship = dfs["shipment"]
    for c in ["shipped_at","delivered_at"]:
        if c in ship.columns:
            cols.append(pd.to_datetime(ship[c], errors="coerce"))

    pay = dfs["payment"]
    if "paid_at" in pay.columns:
        cols.append(pd.to_datetime(pay["paid_at"], errors="coerce"))

    ws = dfs["web_session"]
    if "started_at" in ws.columns:
        cols.append(pd.to_datetime(ws["started_at"], errors="coerce"))

    s = pd.concat(cols).dropna()
    if s.empty:
        s = pd.Series([pd.to_datetime("2020-01-01")])

    start = s.min().normalize()
    end   = s.max().normalize()

    dates = pd.date_range(start, end, freq="D")
    dim = pd.DataFrame({"date": dates})

    # natural key (YYYYMMDD)
    dim["date_key"] = dim["date"].dt.strftime("%Y%m%d").astype(int)

    # surrogate key incremental (PK sugerida en esta dim)
    dim["date_sk"] = range(1, len(dim)+1)

    dim["year"]       = dim["date"].dt.year
    dim["quarter"]    = dim["date"].dt.quarter
    dim["month"]      = dim["date"].dt.month
    dim["month_name"] = dim["date"].dt.strftime("%b")
    dim["day"]        = dim["date"].dt.day
    dim["dow"]        = dim["date"].dt.dayofweek
    dim["dow_name"]   = dim["date"].dt.strftime("%a")

    # dejamos date_key como atributo, pero el hecho referirá date_sk
    return dim[["date_sk","date_key","date","year","quarter","month","month_name","day","dow","dow_name"]]
