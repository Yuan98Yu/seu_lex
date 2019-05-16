def print_result_of_lexfile_parser(maps, rules, p1, p4):
    print("regular expressions".center(30, '*'))
    for item in maps.items():
        print(item)
    print("rules".center(30, '*'))
    for rule in rules:
        print("pattern:",rule.pattern, "action:"+str(rule.action), end="\n-----\n")
    print("part1".center(30, '*'))
    for line in p1:
        print(line)
    print("part4".center(30, '*'))
    for line in p4:
        print(line)
