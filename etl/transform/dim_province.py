from .helpers import add_surrogate_key

def build_dim_province(df_province):
    dim = df_province.drop_duplicates(subset=["province_id"]).copy()
    dim = add_surrogate_key(dim, "province_sk")
    return dim[["province_sk","province_id","name","code"]]
