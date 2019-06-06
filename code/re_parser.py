from reparser.REStandardization import REStandardization_parser
from reparser.re2suffix import Re2suffix_parser
from reparser.suffix2NFA import Suffix2NFA_parser
from reparser.NFA2DFA import NFA2DFA_parser
from reparser.DFAMinimization import DFA_Minimization_parser
from reparser.DFA2Array import DFA2Array_parser
from structs import Rule
from tools import *


class RE_parser:
    """
        给定一个词法单元定义列表Rules，一个Rule包含：词法单元名称(key)，(正则表达式，动作)(value)来创建一个RE_parser的实例
        提供public功能如下：
            Token(str) 对于一个输入的str，返回其对应的词法单元
    """
    def __init__(self):
        self.REStandardization_parser = REStandardization_parser()
        self.Re2suffix_parser = Re2suffix_parser()
        self.suffix2NFA_parser = Suffix2NFA_parser()
        self.NFA2DFA_parser = NFA2DFA_parser()
        self.DFA_minimization_parser = DFA_Minimization_parser()
        self.DFA2Array_parser = DFA2Array_parser()

    def parseRegexs(self, rules, maps):
        # re标准化
        standard_rules = self.REStandardization_parser.re_standardize(rules, maps)
        suffix_rules = self.Re2suffix_parser.re2suffix(standard_rules)
        nfa = self.suffix2NFA_parser.suffix2NFA(suffix_rules)
        dfa = self.NFA2DFA_parser.NFA2DFA(nfa)
        mini_dfa = self.DFA_minimization_parser.DFA_minimize(dfa)
        arrays, endVec = self.DFA2Array_parser.dfa2array(mini_dfa, suffix_rules)
        return arrays, endVec, mini_dfa


if __name__ == '__main__':
    import os, sys
    re_parser_path = os.path.abspath(os.path.join('./reparser'))
    sys.path.append(re_parser_path)
