from pathlib import Path

def save_dim(df, name):
    out = Path("warehouse/dim")
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / f"{name}.csv", index=False)

def save_fact(df, name):
    out = Path("warehouse/fact")
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / f"{name}.csv", index=False)
