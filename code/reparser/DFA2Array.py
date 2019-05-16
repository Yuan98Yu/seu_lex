from ..structs import arrays, ALLSET


class DFA2Array_parser:
    def __init__(self):
        pass

    def dfa2array(self, dfa, rules):
        arrays = []
        endVec = []
        set_size = len(ALLSET)

        # 1.ec表：索引char的ascii码，值是对应的列数
        ec = [0 for i in range(256)]
        for i in range(set_size):
            ec[ALLSET[i]] = i+1
        arrays.append((ec, 256))

        # 2.base表：索引是状态序列，值是行数*宽度。
        DFA_size = len(dfa.states_list)
        base = [0 for i in range(DFA_size)]

        # 3.next表：索引是base+ec。值是下一个跳转状态。大小是base*ec
        size_of_next = DFA_size * (set_size + 1)
        next = [-1 for i in range(size_of_next)]

        for i in range(DFA_size):
            base[dfa.states_list[i].number] = i * (set_size+1)
            for itFirst, itSecond in dfa.states_list[i].edges.items():
                next[base[dfa.states_list[i].number] + ec[itFirst]] = itSecond

        arrays.append((base, DFA_size))
        arrays.append((next, size_of_next))

        # 4.accept表：索引是终态状态号，值是对应的序列号
        accept = [0 for i in range(DFA_size)]

        num_of_end = 0
        for itFirst,itSecond in dfa.endStates_dict.items():
            num_of_end += 1
            accept[itFirst] = num_of_end
            endVec.append(rules[itSecond])

        arrays.append((accept, DFA_size))
