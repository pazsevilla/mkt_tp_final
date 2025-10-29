def build_dim_address(df_address, dim_province):
    dim = df_address.drop_duplicates(subset=["address_id"]).copy()
    dim = dim.merge(
        dim_province[["province_id","province_sk","name"]].rename(columns={"name":"province_name"}),
        on="province_id", how="left", validate="m:1"
    )
    dim["address_sk"] = range(1, len(dim)+1)
    keep = ["address_sk","address_id","line1","line2","city",
            "province_sk","province_id","province_name","postal_code","country_code","created_at"]
    return dim[keep]
