from os import environ

def single_proxy(proto, host, port):
    environ[f'{proto.upper()}_PROXY'] = f'{proto}://{host}:{port}'