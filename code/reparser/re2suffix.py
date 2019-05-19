import os
import logging
from structs import Rule


class Re2suffix_parser:
    def __init__(self, log_file_path='../tmp'):
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        logging.basicConfig(filename=log_file_path+'/debug_re2suffix.txt', filemode='w', level=logging.DEBUG)
        logging.FileHandler(log_file_path + '/debug_re2suffix.txt', 'w')

    def re2suffix(self, rules):
        count = 0
        for rule in rules:
            logging.debug("re2suffix rule: %d" % count)
            count += 1
            # 仅处理pattern,即正则式
            pattern = rule.pattern
            stack = []
            queue = []

            i=0
            while i < len(pattern):
                now = pattern[i]
                # (优先级最低，压栈
                if now == '(':
                    stack.append(now)
                elif now == ')':
                    try:
                        while stack[-1] != '(':
                            queue.append(stack.pop())
                        stack.pop()
                    except Exception as err:
                        print(err, "while resolve standard_re: %s" % pattern)
                elif now == '|':
                    if not stack:
                        stack.append(now)
                    elif stack[-1] in ['.', '|', '*']:
                        # 遇到优先级高的
                        while True:
                            queue.append(stack.pop())
                            if not stack or (not stack[-1] in ['.', '|', '*']):
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
                            if not stack or not (stack[-1] in ['.', '*']):
                                break
                        stack.append(now)
                    else:
                        stack.append(now)
                elif now == '*':
                    queue.append(now)
                # 防止越界
                elif now == '`' and i + 1 == len(pattern):
                    queue.append(now)
                # 若是预定义的正则表达式中的转义序列，直接传给正确队列
                elif now == '`' and pattern[i + 1] in ['(', ')', '|', '.', '*']:
                    queue.append(now)
                    queue.append(pattern[i + 1])
                    i += 1
                elif now == '`' and pattern[i + 1] in ['?', '+', '{', '}', '[', ']']:
                    queue.append(pattern[i + 1])
                    i += 1
                else:
                    queue.append(now)
                i+=1
            # 清空栈
            while stack:
                queue.append(stack.pop())
            # 正确队列->字符串
            rule.pattern = ''.join(queue)
        return rules
