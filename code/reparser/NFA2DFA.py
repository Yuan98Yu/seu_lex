from structs import *
import logging, os


class NFA2DFA_parser:
    def __init__(self, log_file_path='../tmp'):
        self.num_of_NFAstates = 0
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        logging.basicConfig(filename=log_file_path + '/debug_NFA2DFA.txt', filemode='w', level=logging.DEBUG)
        logging.FileHandler(log_file_path + '/debug_NFA2DFA.txt', 'w')

    def __epsilon_closure(self, initStates_set, NFAstates_dict):
        stack = []
        handled_flag_list = [False] * self.num_of_NFAstates

        for s in initStates_set:
            # logging.debug('s:%d' % s)
            stack.append(s)
            handled_flag_list[s] = True
        while stack:
            next_states = NFAstates_dict[stack.pop()].edges['@']  # @边指向的states
            for unhandled_state in next_states:
                if handled_flag_list[unhandled_state]:
                    continue
                else:
                    stack.append(unhandled_state)
                    initStates_set.add(unhandled_state)

    def __find_actions(self, NFAstates_in_DFAstate, endStates_in_NFA):
        endState_number = -1
        actions = -1
        find = False
        for NFA_state_number in NFAstates_in_DFAstate:
            if NFA_state_number in endStates_in_NFA.keys():
                if find:
                    if endState_number > NFA_state_number:
                        endState_number = NFA_state_number
                else:
                    endState_number = NFA_state_number
                    find = True
        if find:
            actions = endStates_in_NFA[endState_number]
        return actions

    def __subset_construct(self, origin_set, edge_char, NFAstates_dict):
        flag = False
        constructed_set = set()
        for state_number in origin_set:
            # logging.debug("state_number in origin_set: %d" % state_number)
            next_states = NFAstates_dict[state_number].edges[edge_char]  # edge_char边指向的states
            if len(next_states) == 0:
                continue
            for state_number in next_states:
                logging.debug("state_number in next_states: %d" % state_number)
                constructed_set.add(state_number)
            flag = True
        return flag, constructed_set

    def NFA2DFA(self, NFAin):
        DFAout = DFA()

        self.num_of_NFAstates = len(NFAin.states_dict)
        c = 1
        edgeSet = ALLSET
        unexamed_DFA_states_numbers = []
        counter = 0
        state = DFAstate(counter)
        counter += 1
        state.identify_set.add(NFAin.startState)
        self.__epsilon_closure(state.identify_set, NFAin.states_dict)
        DFAout.states_list.append(state)
        unexamed_DFA_states_numbers.append(state.number)
        while unexamed_DFA_states_numbers:
            nowState_num = unexamed_DFA_states_numbers.pop(0)
            for c in edgeSet:
                # logging.debug("in for")
                flag, tmpSet = self.__subset_construct(DFAout.states_list[nowState_num].identify_set, c, NFAin.states_dict)
                if flag:
                    logging.debug("in flag")
                    self.__epsilon_closure(tmpSet, NFAin.states_dict)
                    to_state_num = -1
                    has = False
                    for s in DFAout.states_list:
                        if s.identify_set == tmpSet:
                            to_state_num = s.number
                            has = True
                            break
                    if not has:
                        new_DFAstate = DFAstate(counter, tmpSet)
                        counter += 1
                        to_state_num = new_DFAstate.number
                        DFAout.states_list.append(new_DFAstate)
                        unexamed_DFA_states_numbers.append(to_state_num)
                        actions = self.__find_actions(new_DFAstate.identify_set, NFAin.endStates_dict)
                        if actions != -1:
                            DFAout.endStates_dict[new_DFAstate.number] = actions
                    DFAout.states_list[nowState_num].edges[c] = to_state_num
        return DFAout
