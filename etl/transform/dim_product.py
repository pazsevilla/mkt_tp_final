def build_dim_product(df_product, df_category):
    dim = df_product.drop_duplicates(subset=["product_id"]).copy()

    # self-join para resolver parent
    cat = df_category[["category_id","name","parent_id"]].rename(columns={"name":"category_name"})
    cat_parent = df_category[["category_id","name"]].rename(columns={"category_id":"parent_id","name":"category_parent_name"})

    cat_full = cat.merge(cat_parent, on="parent_id", how="left")

    # producto + categoría + nombre del parent (sin parent_id)
    dim = dim.merge(
        cat_full[["category_id","category_name","category_parent_name"]],
        on="category_id", how="left", validate="m:1"
    )

    dim["product_sk"] = range(1, len(dim)+1)

    keep = [
        "product_sk","product_id","sku","name",
        "category_id","category_name","category_parent_name",
        "list_price","status","created_at"
    ]
    return dim[keep]
