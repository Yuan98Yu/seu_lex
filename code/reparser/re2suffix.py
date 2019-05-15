from structs import Rule


class Re2suffix_parser:
    def re2suffix(self, rules):
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
                            if stack or not (stack[-1] in ['.', '|', '*']):
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
            # 清空栈
            while stack:
                queue.append(stack.pop())
            # 正确队列->字符串
            rule.pattern = ''.join(queue)
        return rules
