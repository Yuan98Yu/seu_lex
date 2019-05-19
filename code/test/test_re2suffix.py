import os, sys
top_path = os.path.abspath(os.path.join('..'))
sys.path.append(top_path)
from structs import Rule
from reparser.re2suffix import Re2suffix_parser

if __name__ == '__main__':
    rules = [Rule('(a)|b', 'print(a|b)'), Rule('".`)."', 'print(".`).")')]
    re2suffix_parser = Re2suffix_parser()
    rules = re2suffix_parser.re2suffix(rules)
    for rule in rules:
        print(rule.pattern, rule.action)
