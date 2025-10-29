def build_dim_store(df_store, dim_address):
    dim = df_store.drop_duplicates(subset=["store_id"]).copy()
    dim = dim.merge(
        dim_address[["address_id","address_sk"]],
        on="address_id", how="left", validate="m:1"
    )
    dim["store_sk"] = range(1, len(dim)+1)
    return dim[["store_sk","store_id","name","address_sk","address_id"]]
