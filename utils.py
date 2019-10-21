import csv
import json
import os
import pandas as pd

def read_rules(path_to_rules):
    with open(path_to_rules, 'r') as json_file:
        rules = json.load(json_file)
    return rules

def read_data(path_to_data):
    with open(path_to_data, 'r') as data_file:
        data = pd.read_csv(path_to_data, sep=',', engine='python', keep_default_na=False, na_values=[None])
    return data

def table_title(file_path):
    '''
    generates h3 tag with table title from .csv file name
    '''

    return "<h3 id\"table-title\">" + os.path.basename(file_path).replace('.csv', '') + "</h3>\n"

def section_title(file_path):
    '''
    generates h2 tag with section table from directory name
    '''

    return '<h2 id="' + '-'.join(os.path.basename(file_path).split(' ')) + '">' + os.path.basename(file_path) + '</h2>\n'
