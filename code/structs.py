from enum import IntEnum, unique
from copy import copy
from collections import defaultdict


class Rule:
    def __init__(self, pattern, action):
        self.pattern = pattern
        self.action = copy(action)


class NFAstate:
    """
    结构体：一个NFA节点的索引数字，和该节点出边
    edges为一个多值映射的字典
    """
    def __init__(self, number=0, edges=None):
        if edges is None:
            edges = defaultdict(set)
        self.number = number
        self.edges = edges


class NFA:
    """
    结构体：一个完整的NFA，其开始节点（唯一），终止节点及对应动作（不唯一），以及所有节点（NFAstate类型）"""
    def __init__(self, startState=0, endStates_dict=None, states_dict=None):
        self.startState = startState
        self.endStates_dict = endStates_dict  # int: int, number: actionIndex
        self.states_dict = states_dict  # int: NFAstate, number: NFAstate


@unique
class LexfileState(IntEnum):
    """枚举类型：当前处理的.l文件中的模块"""
    BeforePart1 = 0
    Part1 = 1
    Part2 = 2
    Part3 = 3
    Part4 = 4