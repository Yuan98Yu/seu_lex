# coding:utf-8
from lexfile_parser import LexFileParser
from argparse import ArgumentParser
argparse = ArgumentParser(prog="lex writen by Yuan Yu, 2019.5.12",
                          description="""
                          占位
                          """)
argparse.add_argument("inputFile", help="input file's url")
argparse.add_argument("--output", "-o", help="output file's url")
args = argparse.parse_args()
if args.output is None:
    args.output = "output.l"

if __name__ == '__main__':
    lex_parser = LexFileParser()
    maps, rules, p1, p4 = lex_parser.read_and_parse_lex(args.inputFile)
    print("regular expressions".center(30, '*'))
    for item in maps.items():
        print(item)
    print("rules".center(30, '*'))
    for rule in rules:
        print("pattern:",rule.pattern, "action:"+str(rule.action), end="\n-----\n")
    print("part1".center(30, '*'))
    for line in p1:
        print(line)
    print("part4".center(30, '*'))
    for line in p4:
        print(line)
