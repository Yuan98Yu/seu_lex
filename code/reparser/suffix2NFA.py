from structs import Rule, NFAstate, NFA


class Suffix2NFA_parser:
    def __init__(self):
        self.number = 0
        self.NFA_stack = []
        self.tmp_action_int = -1
        pass

    def __case0(self):
        """if now == '|'"""
        upNFA = self.NFA_stack.pop()
        downNFA = self.NFA_stack.pop()
        startNode = NFAstate(self.number)
        self.number += 1
        endNode = NFAstate(self.number)
        self.number += 1
        # 将up、down的终态都连接到end
        upNFA.states_dict[list(upNFA.endStates_dict.keys())[0]].edges['@'] \
            .add(endNode.number)
        downNFA.states_dict[list(downNFA.endStates_dict.keys())[0]].edges['@'] \
            .add(endNode.number)
        # 将start 连接到up、down的初态
        startNode.edges['@'].add(upNFA.startState)
        startNode.edges['@'].add(downNFA.startState)
        # 连接关系定义好后，存入states_dict
        downNFA.states_dict[startNode.number] = startNode
        downNFA.states_dict[endNode.number] = endNode
        # 将upNFA的states_dict拷贝到downNFA
        downNFA.states_dict.update(upNFA.states_dict)
        #修改downNFA的初态
        downNFA.startState = startNode.number
        #修改downNFA的终态
        downNFA.endStates_dict.clear()
        downNFA.endStates_dict[endNode.number] = self.tmp_action_int
        self.NFA_stack.append(downNFA)

    def __case1(self):
        """if now == '*'"""
        # 取出最上面的NFA进行操作
        upNFA = self.NFA_stack.pop()
        # 新建两个状态
        startNode = NFAstate(self.number)
        self.number += 1
        endNode = NFAstate(self.number)
        self.number += 1
        # start与upNFA的初态连接
        startNode.edges['@'].add(upNFA.startState)
        # start与end连接
        startNode.edges['@'].add(endNode.number)
        # upNFA的终态与初态连接
        upNFA.states_dict[list(upNFA.endStates_dict.keys())[0]].edges['@'] \
            .add(upNFA.startState)
        upNFA.states_dict[list(upNFA.endStates_dict.keys())[0]].edges['@'] \
            .add(endNode.number)
        # 更改初态
        upNFA.startState = startNode.number
        # 存入states_dict
        upNFA.states_dict[startNode.number] = startNode
        upNFA.states_dict[endNode.number] = endNode
        # 更改终态
        upNFA.endStates_dict.clear()
        upNFA.endStates_dict[endNode.number] = self.tmp_action_int
        self.NFA_stack.append(upNFA)

    def __case2(self):
        """if now == '.'"""
        upNFA = self.NFA_stack.pop()
        downNFA = self.NFA_stack.pop()
        # downNFA的终态 与 upNFA的初态连接
        downNFA.states_dict[list(downNFA.endStates_dict.keys())[0]] \
            .edges['@'].add(upNFA.startState)
        # 更改终态
        downNFA.endStates_dict.clear()
        downNFA.endStates_dict.update(upNFA.endStates_dict)
        downNFA.states_dict.update(upNFA.states_dict)
        self.NFA_stack.append(downNFA)

    def __switch(self, now):
        return {'|': self.__case0, '*': self.__case1, '.': self.__case2}.get(now, None)

    def suffix2NFA(self, suffix_rules):
        self.number = 0
        self.NFA_stack = []
        for i in range(len(suffix_rules)):
            pattern = suffix_rules[i].pattern
            self.tmp_action_int = -1
            it = 0
            while it < len(pattern):
                now = pattern[it]
                if self.__switch(now) is not None:
                    self.__switch(now)()
                # default:
                else:
                    if now == '`':
                        it += 1
                        now = pattern[it]
                    # 遇到字符，新建一个起始状态和一个终止状态，构造一个NFA并压栈
                    startNode = NFAstate(self.number)
                    self.number += 1
                    endNode = NFAstate(self.number)
                    self.number += 1
                    pushNFA = NFA(startNode.number)
                    # 连接 起始状态和终止状态
                    startNode.edges[now].add(endNode.number)
                    # 存入states_dict
                    pushNFA.states_dict[startNode.number] = startNode
                    pushNFA.states_dict[endNode.number] = endNode
                    # 标识当前终态，因此先传入空vector
                    pushNFA.endStates_dict[endNode.number] = self.tmp_action_int
                    # 压栈
                    self.NFA_stack.append(pushNFA)
                it += 1
            # 将action 赋给栈顶的NFA的终态
            for endnumber in self.NFA_stack[-1].endStates_dict.keys():
                self.NFA_stack[-1].endStates_dict[endnumber] = i
        # 将得到的所有NFA合并
        final_NFA = self.NFA_stack.pop()
        while self.NFA_stack:
            # 将栈顶的NFA依次与final_NFA合并
            down_NFA = self.NFA_stack.pop()
            startNode = NFAstate(self.number)
            self.number += 1
            startNode.edges['@'].add(final_NFA.startState)
            startNode.edges['@'].add(down_NFA.startState)
            # 修改finalNFA的起始状态
            final_NFA.startState = startNode.number
            final_NFA.states_dict[startNode.number] = startNode
            # 添加finalNFA的终止状态
            final_NFA.endStates_dict.update(down_NFA.endStates_dict)
            # 把downNFA的状态拷贝到finalNFA中
            final_NFA.states_dict.update(down_NFA.states_dict)
        return final_NFA
