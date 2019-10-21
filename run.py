import argparse
from clartable import Clartable
from reader import read_data, read_rules
import os

parser = argparse.ArgumentParser(description='Create html table from given data and rules')
parser.add_argument('-i', metavar='PATH', required=True, help='path to corpora folder with csv file')
parser.add_argument('-r', metavar='PATH', required=True, help='path to json file with rules')
parser.add_argument('-o', metavar='PATH', required=True, help='path to file where output html table will be written')

args = parser.parse_args()


if __name__ == "__main__":
    rules = read_rules(args.r)
    clartable = Clartable(rules)
    output = open(args.o, 'w')

    # input is a single file
    if os.path.isfile(args.i):
        data = open(args.i, 'r')
        title = <h3 id=\"table-title\">" + os.path.basename(args.i).replace('.csv', '') + "</h3>\n"
        table = title + clartable.generate(data)
        output.write(table)
    # input is a folder
    else:
        for root, subdir, files in os.walk(args.i):
            subdir.sort()
            if len(files) > 0:
                if os.path.basename(root) != '':
                    title = '<h2 id="' + '-'.join(os.path.basename(root).split(' ')) + '">' + os.path.basename(root) + '</h2>\n'
                    output.write(title)
                for _file in files:
                    data = read_data(os.path.join(root, _file))
                    # generate table:
                    if _file != '':
                        table = "<h3 id=\"table-title\">" + _file.replace('.csv', '') + "</h3>\n"
                    else:
                        table = ''
                    table += clartable.generate(data)
                    output.write(table)
