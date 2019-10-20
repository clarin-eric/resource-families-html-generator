import argparse
from clartable import Clartable
from reader import read_data, read_rules
import os

parser = argparse.ArgumentParser(description='Create html table from given data and rules')
parser.add_argument('-i', metavar='PATH', required=True, help='path to input csv file')
parser.add_argument('-r', metavar='PATH', required=True, help='path to json file with rules')
parser.add_argument('-o', metavar='PATH', required=True, help='path to file where output html table will be written')

args = parser.parse_args()


if __name__ == "__main__":
        csv_name = os.path.basename(args.i)
        csv_name = csv_name.replace('.csv', '')
        data = read_data(args.i)
        rules = read_rules(args.r)
        clartable = Clartable(rules)
        # generate table
        ret = clartable.generate(data)
        output = open(args.o, 'w')
        # add title
        ret = "<h3 id=\"table-title\">" + csv_name + "</h3>\n" + ret
        output.write(ret)
