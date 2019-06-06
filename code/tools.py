from struct import *
def print_result_of_lexfile_parser(maps, rules, p1, p4):
    print("regular expressions".center(30, '*'))
    i = 0
    for item in maps.items():
        print('item %d' % i, item)
        i += 1
    print("rules".center(30, '*'))
    i = 0
    for rule in rules:
        print("pattern %d:" % i, rule.pattern, "action:"+str(rule.action))
        i += 1
    print("part1".center(30, '*'))
    for line in p1:
        print(line)
    print("part4".center(30, '*'))
    for line in p4:
        print(line)


def show_rules(filePath, rules):
    with open(filePath, 'w') as f:
        i = 0
        for rule in rules:
            print('rule %d: pattern:%s , action:%s' % (i, rule.pattern, rule.action))
            f.write('rule %d: pattern:%s , action:%s\n' % (i, rule.pattern, rule.action))
            i += 1


def show_nfa(filePath, nfa):
    with open(filePath, 'w') as f:
        f.write('the total nfa state number is %d\n'% len(nfa.states_dict.values()))
        f.write('the total nfa final state number is %d\n'%len(nfa.endStates_dict))
        for nfa_state in nfa.states_dict.values():
            print('number:%d\nedges:\t' % nfa_state.number)
            f.write('number:%d\nedges:\t' % nfa_state.number)
            for edge, nextStates in nfa_state.edges.items():
                print("edge: %s\tnext_states:" % edge)
                f.write("edge: %s\tnext_states:" % edge)
                for next_state in nextStates:
                    print(next_state, end=' ')
                    f.write("%d\t" % next_state)
                print()
                f.write("\n")


def show_dfa(filePath, dfa):
    with open(filePath, 'w') as f:
        f.write('the total dfa state number is %d\n' % len(dfa.states_list))
        f.write('the total dfa final state number is %d\n'%len(dfa.endStates_dict))
        for dfa_state in dfa.states_list:
            print('dfaNode_number:%d\nedges:\t' % dfa_state.number)
            f.write('number:%d\nedges:\t' % dfa_state.number)
            for edge, nextState in dfa_state.edges.items():
                print("edge: %s\tnext_state:%d\n" % (edge, nextState))
                f.write("edge: %s\tnext_state:%d\n" % (edge, nextState))

