def build_dim_address(df_address, df_province):
    # address + province (sin snowflake)
    dim = df_address.drop_duplicates(subset=["address_id"]).copy()

    dim = dim.merge(
        df_province[["province_id","name","code"]]
          .rename(columns={"name":"province_name","code":"province_code"}),
        on="province_id", how="left", validate="m:1"
    )

    # surrogate key
    dim["address_sk"] = range(1, len(dim)+1)

    # columnas finales (SIN province_sk ni nada en cadena)
    keep = [
        "address_sk","address_id",
        "line1","line2","city",
        "province_name","province_code",
        "postal_code","country_code","created_at"
    ]
    return dim[keep]

