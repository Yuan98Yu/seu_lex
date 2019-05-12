from structs import Rule
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

    def _re_to_suffix(self, rules):
        for rule in rules:
            # 仅处理pattern,即正则式
            pattern = rule.pattern
            stack = []
            queue = []

            for i in range(len(pattern)):
                now = pattern[i]
                # (优先级最低，压栈
                if now == '(':
                    stack.append(now)
                elif now == ')':
                    while stack[-1] != '(':
                        queue.append(stack.pop())
                    stack.pop()
                elif now == '|':
                    if not stack:
                        stack.append(now)
                    elif stack[-1] in ['.', '|', '*']:
                        # 遇到优先级高的
                        while True:
                            queue.append(stack.pop())
                            if stack or not(stack[-1] in ['.', '|', '*']):
                                break
                        stack.append(now)
                    else:
                        stack.append(now)
                elif now == '.':
                    if not stack:
                        stack.append(now)
                    elif stack[-1] in ['.', '*']:
                        # 遇到优先级高的
                        while True:
                            queue.append(stack.pop())
                            if stack or not (stack[-1] in ['.', '*']):
                                break
                        stack.append(now)
                    else:
                        stack.append(now)
                elif now == '*':
                    queue.append(now)
                # 防止越界
                elif now == '`' and i+1 == len(pattern):
                    queue.append(now)
                # 若是预定义的正则表达式中的转义序列，直接传给正确队列
                elif now == '`' and pattern[i+1] in ['(', ')', '|', '.', '*']:
                    queue.append(now)
                    queue.append(pattern[i+1])
                    i += 1
                elif now == '`' and pattern[i+1] in ['?', '+', '{', '}', '[', ']']:
                    queue.append(pattern[i+1])
                    i += 1
                else:
                    queue.append(now)
            # 清空栈
            while stack:
                queue.append(stack.pop())
            # 正确队列->字符串
            rule.pattern = ''.join(queue)

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

