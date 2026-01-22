from pathlib import Path
import socket

def get_repo_root():
    return Path(__file__).parent.parent.parent

def p(*parts):
    return get_repo_root().joinpath(*parts)

def plots_path(*parts):
    return p("plots", *parts)

def _get_hostname() -> str:
    return socket.gethostname()

def data_path(*parts):
    hostname = _get_hostname()

    if hostname == "hypernova":
        base = Path("/data2/ATLAS/WDs/")
    elif hostname.startswith("node"):
        base = Path("/orcd/data/kburdge/001/ATLAS/ATLAS_Lightcurves/")  
    else:
        raise RuntimeError(f"hostname '{hostname}' not recognized")

    return base.joinpath(*parts)

def bls_path(*parts):
    hostname = _get_hostname()

    if hostname == "hypernova":
        base = Path("/data/Bulk_BLS_ATLAS/")
    elif hostname.startswith("node"):
        base = Path("/orcd/data/kburdge/001/ATLAS/ATLAS_BLS/")
    else:
        raise RuntimeError(f"hostname '{hostname}' not recognized")

    return base.joinpath(*parts)

def lc_path(source_id):
    return data_path(str(source_id))
