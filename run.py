import argparse
from clartable import Clartable
from reader import read_data, read_rules

parser = argparse.ArgumentParser(description='Create html table from given data and rules')
parser.add_argument('-i', metavar='PATH', help='path to input csv file')
parser.add_argument('-r', metavar='PATH', help='path to json file with rules')
parser.add_argument('-o', metavar='PATH', help='path to file where output html table will be written')

args = parser.parse_args()


if __name__ == "__main__":
        data = read_data(args.i)
        rules = read_rules(args.r)
        clartable = Clartable(rules)
        ret = clartable.generate(data)
        output = open(args.o, 'w')
        output.write(ret)
