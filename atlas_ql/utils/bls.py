from .paths import bls_path
import pandas as pd 

COLUMNS = ["gid", "pow", "snr", "wid", "per_day", "per_min", "q", "phi0", "dphi", "epo"]
_catalog = None

def load_catalog():
    result_files = sorted(bls_path().glob("*.result"))

    dfs = []
    for result_file in result_files:
        df = pd.read_csv(result_file, names=COLUMNS)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    # Recompute per_day from per_min for better precision
    df['per_day'] = df['per_min'] / 1440
    # Index by gid for fast lookups
    df.set_index('gid', inplace=True)

    return df

def get_catalog():
    global _catalog 
    if _catalog is None:
        _catalog = load_catalog()
    return _catalog

def get_bls_stats(source_id):
    df = get_catalog()

    if source_id in df.index:
        return df.loc[source_id]
    return None

def get_period(source_id):
    df = get_catalog()

    if source_id in df.index:
        return df.loc[source_id, 'per_min']
    return None