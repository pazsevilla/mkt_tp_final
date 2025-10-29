def build_dim_store(df_store, dim_address):
    dim = df_store.drop_duplicates(subset=["store_id"]).copy()

    # store + address (address ya tiene province_name/province_code)
    dim = dim.merge(
        dim_address[[
            "address_id","address_sk",
            "line1","line2","city",
            "province_id","province_name","province_code",
            "postal_code","country_code"
        ]],
        on="address_id", how="left", validate="m:1"
    )

    dim["store_sk"] = range(1, len(dim)+1)

    # dejamos address_sk como FK directa a la dim_address (igual es star: fact no se cuelga de address)
    keep = [
        "store_sk","store_id","name",
        "address_sk","address_id",
        "line1","line2","city","province_name","province_code","postal_code","country_code"
    ]
    return dim[keep]
