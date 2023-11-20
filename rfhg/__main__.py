#!/usr/bin/env python3

import argparse
import os
import re

from .clartable import Clartable
from .reader import read_data, read_rules, resolve_static
from .utils import table_title, section_title

parser = argparse.ArgumentParser(description='Create html table from given data and rules. To use static resources as arguments use `static.<path_inside_rfhg/static>`')
parser.add_argument('-i', metavar='PATH', default='static.resource_families/', help='path to a .csv file or folder with .csv files. Note that nesting data files inside multiple directories will generated nested tables respective to directory nesting.')
parser.add_argument('-r', metavar='PATH', default='static.rules/rules.json', help='path to json file with rules')
parser.add_argument('-o', metavar='PATH', required=True, help='path to file where output html table will be written')

args = parser.parse_args()


if __name__ == "__main__":
    rules = read_rules(args.r)
    clartable = Clartable(rules)

    output_path = args.o
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if os.path.isdir(output_path):
        file_name = os.path.basename(os.path.normpath(output_path)) + '.html'
        output_path = os.path.join(output_path, file_name)
    output = open(output_path, 'w')

    # input is a single file
    input_path = resolve_static(args.i)
    if os.path.isfile(os.path.normpath(input_path)):
        print("Processing file: ", input_path)
        data = read_data(input_path)
        title = table_title(input_path)
        table = title + clartable.generate(data)
        output.write(table)
    # input is a folder
    else:
        print("Processing directory: ", input_path)
        for root, subdir, files in os.walk(input_path):
            subdir.sort()
            files.sort()
            if len(files) > 0:
                if os.path.basename(root) != '':
                    output.write(section_title(root))
                for _file in files:
                    print("Processing file: ", _file)
                    data = read_data(os.path.join(root, _file))
                    # generate table:
                    if _file != '':
                        table = table_title(_file)
                    else:
                        table = ''
                    table += clartable.generate(data)
                    output.write(table)
