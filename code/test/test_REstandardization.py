import os, sys
top_path = os.path.abspath(os.path.join('..'))
sys.path.append(top_path)
from structs import Rule
from reparser.REStandardization import REStandardization_parser

if __name__ == '__main__':
    print("test of REStandardization.py".center(80, '-'))
    re_standardization_parser = REStandardization_parser()
    rules = list()
    re_map = dict({'L': '[a-z]'})

    print("Test1: [a-z]".center(50, '*'))
    rules.append(Rule("{L}", "printf(aas)"))
    rules = re_standardization_parser.re_standardize(rules, re_map)
    i = 0
    for rule in rules:
        print('rule %d: %s, %s' % (i, rule.pattern, rule.action))
        i += 1
