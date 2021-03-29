#!/usr/bin/env python3

import argparse
import os

from clartable import Clartable
from reader import read_data, read_rules
from utils import table_title, section_title

parser = argparse.ArgumentParser(description='Create html table from given data and rules')
parser.add_argument('-i', metavar='PATH', default='./resource_families/', required=True, help='path to a .csv file or folder with .csv files')
parser.add_argument('-r', metavar='PATH', default='./rules.json', required=True, help='path to json file with rules')
parser.add_argument('-o', metavar='PATH', required=True, help='path to file where output html table will be written')

args = parser.parse_args()

if __name__ == "__main__":
    rules = read_rules(args.r)
    clartable = Clartable(rules)
    if not os.path.exists('./tables/'):
        os.makedirs('./tables/')
    output = open(os.path.join('./tables/', os.path.basename(os.path.normpath(args.o)) + '.html'), 'w')

    # input is a single file
    input_path = os.path.expanduser(args.i)
    if os.path.isfile(os.path.normpath(input_path)):
        print("Processing file: ", input_path)
        data = read_data(input_path)
        print(data)
        title = table_title(input_path)
        table = title + clartable.generate(data)
        output.write(table)
    # input is a folder
    else:
        print("Processing directory: ", args.i)
        for root, subdir, files in os.walk(args.i):
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
