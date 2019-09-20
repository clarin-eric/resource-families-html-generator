from clartable import Clartable
from reader import read_data, read_rules

if __name__ == "__main__":
        data = read_data('./literary-corpora.csv')
        rules = read_rules('./rules.json')
        print(rules)
        clartable = Clartable(rules)
        ret = clartable.generate(data)
        print(ret)
        output = open('./table.hmtl', 'w')
        output.write(ret)
