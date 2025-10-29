from .helpers import add_surrogate_key

def build_dim_customer(df_customer):
    dim = df_customer.drop_duplicates(subset=["customer_id"]).copy()
    if "email" in dim.columns:
        dim["email"] = dim["email"].astype(str).str.lower()
    dim = add_surrogate_key(dim, "customer_sk")
    keep = ["customer_sk","customer_id","email","first_name","last_name","phone","status","created_at"]
    return dim[keep]
