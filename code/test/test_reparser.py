import os, sys
top_path = os.path.abspath(os.path.join('..'))
sys.path.append(top_path)
from structs import Rule
from re_parser import RE_parser

if __name__ == '__main__':
    re_parser = RE_parser()
    print("start test of re_parser".center(150, '-'))
    rules = list()
    re_map = dict({'L': '[a-z]'})
    rules.append(Rule("{L}", "printf(aas)"))
    rules = re_parser.parseRegexs(rules, re_map)
