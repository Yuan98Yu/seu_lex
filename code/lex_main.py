# coding:utf-8
from lexfile_parser import LexFileParser
from reparser.re_parser import RE_parser
from C_Code_generator import CCodeGenerator
from argparse import ArgumentParser
from structs import Mode
from tools import *

arg_parse = ArgumentParser(prog="lex writen by Yuan Yu, 2019.5.12",
                           description="""
                          占位
                          """)
arg_parse.add_argument("inputFile", help="input file's url")
arg_parse.add_argument("--output", "-o", help="output file's url")
args = arg_parse.parse_args()
if args.output is None:
    args.output = "output.l"

if __name__ == '__main__':
    lex_file_parser = LexFileParser()
    re_parser = RE_parser()
    c_code_generator = CCodeGenerator()

    maps, rules, p1, p4 = lex_file_parser.read_and_parse_lex(args.inputFile)
    print_result_of_lexfile_parser(maps, rules, p1, p4)
    mini_dfa, arrays, endVec = RE_parser.parseRegexs(rules)
    result = c_code_generator.generate_c_code(arrays, endVec, p1, p4, mini_dfa.startState, Mode.LEX_TEST)
