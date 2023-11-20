import csv
from importlib import resources
import json
import pandas as pd
import pathlib
import re

from . import static


def _static_loc(path):
    return (resources.files(static) / path)


def resolve_static(arg):
    args = arg.split('.')
    if re.search("^static$", args[0]):
        return _static_loc('.'.join(args[1:]))
    else:
        return arg


def _open_handle(path):
    if isinstance(path, pathlib.PosixPath):
        return path.open("rt")
    else:
        return open(path, "r")


def read_rules(path_to_rules):
    path_to_rules = resolve_static(path_to_rules)
    rules_handle = _open_handle(path_to_rules)
    rules = json.load(rules_handle)
    rules_handle.close()
    return rules

def read_data(path_to_data):
    path_to_data = resolve_static(path_to_data)
    data_handle = _open_handle(path_to_data)
    data = pd.read_csv(data_handle, sep=';', engine='python', keep_default_na=False)
    data_handle.close()
    return data

