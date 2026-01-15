from pathlib import Path

def get_repo_root():
    return Path(__file__).parent.parent.parent

def p(*parts):
    return get_repo_root().joinpath(*parts)

def plots_path(*parts):
    return p("plots", *parts)

def data_path(*parts):
    import socket
    hostname = socket.gethostname()

    path_dict = {
        'hypernova': '/data2/ATLAS/WDs/'
    }

    if hostname in path_dict.keys():
        return Path(path_dict[hostname]).joinpath(*parts)
    else:
        print(f'hostname {hostname} not recognized')

def bls_path(*parts):
    import socket
    hostname = socket.gethostname()

    path_dict = {
        'hypernova': '/data/Bulk_BLS_ATLAS/'
    }

    if hostname in path_dict.keys():
        return Path(path_dict[hostname]).joinpath(*parts)
    else:
        print(f'hostname {hostname} not recognized')

def lc_path(source_id):
    return data_path(str(source_id))
