def add_surrogate_key(df, new_col_name):
    df = df.copy()
    df[new_col_name] = range(1, len(df) + 1)
    return df
