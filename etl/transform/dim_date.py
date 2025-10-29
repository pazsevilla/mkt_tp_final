import pandas as pd

def build_dim_date(dfs: dict):
    cols = []
    so = dfs["sales_order"]
    cols.append(pd.to_datetime(so["order_date"], errors="coerce"))

    ship = dfs["shipment"]
    for c in ["shipped_at","delivered_at"]:
        cols.append(pd.to_datetime(ship[c], errors="coerce"))

    pay = dfs["payment"]
    cols.append(pd.to_datetime(pay["paid_at"], errors="coerce"))

    ws = dfs["web_session"]
    cols.append(pd.to_datetime(ws["started_at"], errors="coerce"))

    s = pd.concat(cols).dropna()
    start = s.min().normalize()
    end   = s.max().normalize()

    dates = pd.date_range(start, end, freq="D")
    dim = pd.DataFrame({"date": dates})
    dim["date_key"]   = dim["date"].dt.strftime("%Y%m%d").astype(int)
    dim["year"]       = dim["date"].dt.year
    dim["quarter"]    = dim["date"].dt.quarter
    dim["month"]      = dim["date"].dt.month
    dim["month_name"] = dim["date"].dt.strftime("%b")
    dim["day"]        = dim["date"].dt.day
    dim["dow"]        = dim["date"].dt.dayofweek
    dim["dow_name"]   = dim["date"].dt.strftime("%a")
    return dim[["date_key","date","year","quarter","month","month_name","day","dow","dow_name"]]
