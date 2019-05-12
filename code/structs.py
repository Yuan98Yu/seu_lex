from enum import IntEnum, unique
from copy import copy

class Rule:
    def __init__(self, pattern, action):
        self.pattern = pattern
        self.action = copy(action)


@unique
class LexfileState(IntEnum):
    """枚举类型：当前处理的.l文件中的模块"""
    BeforePart1 = 0
    Part1 = 1
    Part2 = 2
    Part3 = 3
    Part4 = 4