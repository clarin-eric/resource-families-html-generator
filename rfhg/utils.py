import csv
import json
import os
import pandas as pd
from typing import Set


def read_rules(path_to_rules):
    with open(path_to_rules, 'r') as json_file:
        rules = json.load(json_file)
    return rules


def read_data(path_to_data):
    with open(path_to_data, 'r') as data_file:
        data = pd.read_csv(path_to_data, sep=';', engine='python', keep_default_na=False, na_values=[None])
    return data


def get_title(file_path):
    clean_title = ''
    if(os.path.basename(file_path)[:1].isdigit()):
        clean_title = ' '.join(os.path.basename(file_path).split('-')[1:]).replace('.csv', '')
    else:
        clean_title = os.path.basename(file_path)
    return clean_title


def table_title(file_path):
    '''
    generates h3 tag with table title from .csv file name
    '''

    return "<h3 id\"table-title\">" + get_title(file_path) + "</h3>\n"


def section_title(file_path):
    '''
    generates h2 tag with section table from directory name
    '''

    return '<h2 id="' + '-'.join(os.path.basename(file_path).split(' ')) + '">' + get_title(file_path) + '</h2>\n'


class EmptyColumnError(Exception):
    """
    Exception thrown when field value is empty without fallback rule for corresponding set of columns

    :ivar column_set: set of column names for which field values are empty
    :type column_set: Set[str]
    """
    def __init__(self, column_set: Set[str]):
        self.message = f"These non-optional columns: {column_set} are empty without fallback <ifempty> rule defined."
        super().__init__(self.message)
