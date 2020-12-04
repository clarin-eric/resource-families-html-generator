import csv
import json
import pandas as pd

def read_rules(path_to_rules):
    try:
        with open(path_to_rules, 'r') as json_file:
            rules = json.load(json_file)
    except:
        raise Exception("The rules file failed to open: " + path_to_rules)
    return rules

def read_data(path_to_data):
    try:
        with open(path_to_data, 'r') as data_file:
            data = pd.read_csv(path_to_data, sep=',', engine='python', keep_default_na=False, na_values=[None])
    except:
        raise Exception("The .csv file failed to open: " + path_to_data)
    return data
