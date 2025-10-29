from .helpers import add_surrogate_key

def build_dim_product_category(df_cat):
    dim = df_cat.drop_duplicates(subset=["category_id"]).copy()
    dim = add_surrogate_key(dim, "category_sk")
    return dim[["category_sk","category_id","name","parent_id"]]

