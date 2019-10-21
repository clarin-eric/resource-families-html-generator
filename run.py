import argparse
from clartable import Clartable
from reader import read_data, read_rules
import os

parser = argparse.ArgumentParser(description='Create html table from given data and rules')
parser.add_argument('-i', metavar='PATH', required=True, help='path to a .csv file or folder with .csv files')
parser.add_argument('-r', metavar='PATH', required=True, help='path to json file with rules')
parser.add_argument('-o', metavar='PATH', required=True, help='path to file where output html table will be written')

args = parser.parse_args()


def table_title(file_path):
    '''
    generates h3 tag with file name as table title
    '''

    return "<h3 id\"table-title\">" + os.path.basename(file_path).replace('.csv', '') + "</h3>\n"


if __name__ == "__main__":
    rules = read_rules(args.r)
    clartable = Clartable(rules)
    output = open(args.o, 'w')

    # input is a single file
    if os.path.isfile(args.i):
        data = open(args.i, 'r')
        title = table_title(args.i)
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
                        table = table_title(args.i)
                    else:
                        table = ''
                    table += clartable.generate(data)
                    output.write(table)
