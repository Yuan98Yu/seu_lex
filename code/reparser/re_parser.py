from ..structs import Rule, NFAstate, NFA, DFA
from .re2suffix import Re2suffix_parser
from .suffix2NFA import Suffix2NFA_parser
from .NFA2DFA import NFA2DFA_parser
from .DFAMinimization import DFA_Minimization_parser
from .DFA2Array import DFA2Array_parser
import types
import re


class RE_parser:
    """
        给定一个词法单元定义列表Rules，一个Rule包含：词法单元名称(key)，(正则表达式，动作)(value)来创建一个RE_parser的实例
        提供public功能如下：
            Token(str) 对于一个输入的str，返回其对应的词法单元
    """
    def __init__(self, rules):
        self.rules = rules
        self.Re2suffix_parser = Re2suffix_parser()
        self.suffix2NFA_parser = Suffix2NFA_parser()
        self.NFA2DFA_parser = NFA2DFA_parser()
        self.DFA_minimization_parser = DFA_Minimization_parser()
        self.DFA2Array_parser = DFA2Array_parser()

    def parseRegexs(self):
        # re标准化
        pass
        suffix_rules = self.Re2suffix_parser.re2suffix(self.rules)
        nfa = self.suffix2NFA_parser.suffix2NFA(suffix_rules)
        dfa = self.NFA2DFA_parser.NFA2DFA(nfa)
        dfa = self.DFA_minimization_parser.DFA_minimize(dfa)
        arrays, endVec = self.DFA2Array_parser.dfa2array(dfa, suffix_rules)

    def _form_master_re(self, regex_list, reflags, ldict, toknames):
        if not regex_list:
            return []
        regex = '|'.join(regex_list)
        try:
            lex_re_pattern = re.compile(regex, reflags)

            # Build the index to function map for the matching engine
            lex_index_func = [None] * (max(lex_re_pattern.groupindex.values()) + 1)
            lex_index_names = lex_index_func[:]

            for f, i in lex_re_pattern.groupindex.items():
                handle = ldict.get(f, None)
                if type(handle) in (types.FunctionType, types.MethodType):
                    lex_index_func[i] = (handle, toknames[f])
                    lex_index_names[i] = f
                elif handle is not None:
                    lex_index_names[i] = f
                    if f.find('ignore_') > 0:
                        lex_index_func[i] = (None, None)
                    else:
                        lex_index_func[i] = (None, toknames[f])

            return [(lex_re_pattern, lex_index_func)], [regex], [lex_index_names]
        except Exception:
            m = int(len(regex_list) / 2)
            if m == 0:
                m = 1
            llist, lre, lnames = _form_master_re(regex_list[:m], reflags, ldict, toknames)
            rlist, rre, rnames = _form_master_re(regex_list[m:], reflags, ldict, toknames)
            return (llist + rlist), (lre + rre), (lnames + rnames)

