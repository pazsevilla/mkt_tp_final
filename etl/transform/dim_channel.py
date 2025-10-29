from .helpers import add_surrogate_key

def build_dim_channel(df_channel):
    # 1) quitamos duplicados por id natural
    dim = df_channel.drop_duplicates(subset=["channel_id"]).copy()
    # 2) agregamos surrogate key
    dim = add_surrogate_key(dim, "channel_sk")
    # 3) columnas finales ordenadas
    return dim[["channel_sk", "channel_id", "code", "name"]]
