import os, sys
top_path = os.path.abspath(os.path.join('..'))
sys.path.append(top_path)
from structs import Rule
from reparser.suffix2NFA import Suffix2NFA_parser
from tools import *

if __name__ == '__main__':
    print("start test of suffix2NFA".center(170, '-'))
    suffix2nfa_parser = Suffix2NFA_parser()
    suffix_rules = []
    flag = True
    pattern = "."
    i = 1
    while pattern:
        pattern = input("pattern:")
        rule = Rule(pattern, "print %d" % i)
        suffix_rules.append(rule)
        i += 1

    final_nfa = suffix2nfa_parser.suffix2NFA(suffix_rules)
    print(final_nfa.startState)
    print(final_nfa.endStates_dict)
    print(final_nfa.states_dict)
    show_nfa('nfa.txt', final_nfa)
