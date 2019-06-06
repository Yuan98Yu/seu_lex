# coding:utf-8
from lexfile_parser import LexFileParser
from re_parser import RE_parser
from C_Code_generator import CCodeGenerator
from tools import *
from structs import Mode
from argparse import ArgumentParser
import logging


arg_parse = ArgumentParser(prog="lex writen by Yuan Yu, 2019.5.12",
                           description="""
                          占位
                          """)
arg_parse.add_argument("inputFile", help="input file's url")
arg_parse.add_argument("--output", "-o", help="output file's url")
arg_parse.add_argument("--test", "-t", action="store_true")
args = arg_parse.parse_args()
if args.output is None:
    args.output = "output.l"

if __name__ == '__main__':
    import os
    import sys
    re_parser_path = os.path.abspath(os.path.join('./reparser'))
    sys.path.append(re_parser_path)

    lex_file_parser = LexFileParser()
    re_parser = RE_parser()
    c_code_generator = CCodeGenerator()

    maps, rules, p1, p4 = lex_file_parser.read_and_parse_lex(args.inputFile)
    print_result_of_lexfile_parser(maps, rules, p1, p4)


# ----------------------------------- test of reparser -----------------------------------------
    if args.test:
        print("raw_re".center(170, '-'))
        show_rules('tmp/raw_re.txt', rules)
        standard_rules = re_parser.REStandardization_parser.re_standardize(rules, maps)
        print("standard_re".center(170, '-'))
        show_rules('tmp/standard_re.txt', standard_rules)
        # mini_dfa, arrays, endVec = re_parser.parseRegexs(rules)
        # result = c_code_generator.generate_c_code(arrays, endVec, p1, p4, mini_dfa.startState, Mode.LEX_TEST)
        suffix_rules = re_parser.Re2suffix_parser.re2suffix(standard_rules)
        print("suffix_re".center(170, '-'))
        show_rules('tmp/suffix_re.txt', suffix_rules)
        nfa = re_parser.suffix2NFA_parser.suffix2NFA(suffix_rules[0:])
        show_nfa('tmp/nfa.txt', nfa)
        dfa = re_parser.NFA2DFA_parser.NFA2DFA(nfa)
        print('total number', dfa)
        show_dfa('tmp/dfa.txt', dfa)
        logging.FileHandler("tmp/debug_miniDFA.txt", 'w')
        mini_dfa = re_parser.DFA_minimization_parser.DFA_minimize(dfa)
        show_dfa('tmp/mini_dfa.txt', mini_dfa)


        arrays, endVec = re_parser.DFA2Array_parser.dfa2array(mini_dfa, suffix_rules)
        print("Code_generator start".center(100, '-'))
        mode = Mode.LEX_TEST
        c_code_generator.generate_c_code(arrays, endVec, p1, p4, mini_dfa.startState, mode, args.output)


# -------------------------------- end of test of reparser --------------------------------------
    else:
        arrays, endVec, mini_dfa= re_parser.parseRegexs(rules, maps)
        mode = Mode.LEX_TEST
        c_code_generator(arrays, endVec, p1, p4, mini_dfa.startState, mode, args.output)
