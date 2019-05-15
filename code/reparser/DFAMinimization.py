from structs import ALLSET, DFAstate, DFA
from random import choice


class DFA_Minimization_parser:
    def __init__(self):
        self.statesSetsVec = []
        self.statesSetsMap = {}
        self.count = 0
        pass

    def DFA_minimize(self, origin_dfa):
        new_dfa = DFA()
        self.__split_to_sets(origin_dfa)
        new_dfa.startState = self.statesSetsMap[origin_dfa.startState]
        for p in origin_dfa.endStates_dict.keys():
            new_dfa.endStates_dict[self.statesSetsMap[p]] = origin_dfa.endStates_dict[p]
        for k in range(len(self.statesSetsVec)):
            pivot_state = origin_dfa.states_list[choice(self.statesSetsVec[k])]
            new_state = DFAstate(k)
            for key, value in pivot_state.edges.items():
                new_state.edges[key] = self.statesSetsMap[value]
            new_dfa.states_list.append(new_state)
        return new_dfa

    def __scan(self, DFAstate_list):
        new_set = set()
        flag = False
        split_set_number = 0
        # 找到一个需要处理的集合
        for k in range(DFAstate_list):
            s = self.statesSetsVec[k]
            if len(s) == 1:
                continue
            else:
                stantard = DFAstate_list[choice(s)]
                for c in ALLSET:
                    for i in s:
                        state = DFAstate_list[i]
                        findStateIt = state.edges.get(c, -1)
                        findStandardIt = stantard.edges.get(c, -1)
                        if (findStateIt != -1 and findStandardIt == -1) or (findStateIt == -1 and findStandardIt != -1) \
                                or (findStateIt != -1 and findStandardIt != -1 \
                                    and self.statesSetsMap.get(findStandardIt) != self.statesSetsMap.get(findStateIt)):
                            flag = True
                            new_set.add(i)
                    if flag:
                        break
                if flag:
                    split_set_number = k
                    break
        for s in new_set:
            self.statesSetsVec[split_set_number].discard(s)
            self.statesSetsMap[s] = self.count

        self.statesSetsVec.append(new_set)
        self.count += 1

        return flag

    def __split_to_sets(self, dfa):
        endStates_dict = dfa.endStates_dict
        states_list = dfa.states_list
        for p in endStates_dict.keys():
            self.statesSetsVec.append({p})
            self.statesSetsMap[p] = self.count
            self.count += 1
        tmpset = set()
        for e in states_list:
            if e.number not in endStates_dict.keys():
                tmpset.add(e.number)
                self.statesSetsMap[e.number] = self.count
        self.statesSetsVec.append(tmpset)
        self.count += 1

        while self.__scan(states_list):
            pass
