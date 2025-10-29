import pandas as pd

def build_dim_store(df_store, df_address, df_province):
    # 1) Store sin duplicados
    dim = df_store.drop_duplicates(subset=["store_id"]).copy()

    # 2) Merge store + address
    dim = dim.merge(
        df_address,
        on="address_id",
        how="left",
        validate="m:1"
    )

    # 3) Merge con province (address ya tiene province_id)
    dim = dim.merge(
        df_province.rename(columns={"name":"province_name","code":"province_code"}),
        on="province_id",
        how="left",
        validate="m:1"
    )

    # 4) Crear surrogate key
    dim["store_sk"] = range(1, len(dim) + 1)

    # 5) Seleccionar columnas finales (desnormalización completa)
    keep = [
        "store_sk","store_id","name",
        # address
        "line1","line2","city","postal_code","country_code",
        # province
        "province_name","province_code"
    ]

    return dim[keep]
