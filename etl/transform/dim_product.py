def build_dim_product(df_product, dim_category):
    dim = df_product.drop_duplicates(subset=["product_id"]).copy()
    dim = dim.merge(
        dim_category[["category_id","category_sk","name"]].rename(columns={"name":"category_name"}),
        on="category_id", how="left", validate="m:1"
    )
    dim["product_sk"] = range(1, len(dim)+1)
    keep = ["product_sk","product_id","sku","name",
            "category_sk","category_id","category_name",
            "list_price","status","created_at"]
    return dim[keep]
