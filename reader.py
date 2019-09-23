import csv
import json
import pandas as pd

def read_rules(path_to_rules):
    with open(path_to_rules, 'r') as json_file:
        rules = json.load(json_file)
    return rules

def read_data(path_to_data):
    with open(path_to_data, 'r') as data_file:
        data = pd.read_csv(path_to_data, sep=',', engine='python', keep_default_na=False, na_values=[None])
    return data
