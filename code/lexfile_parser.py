# coding:utf-8

from structs import Rule, LexfileState
import logging
import os





class LexFileParser:
    """.l文件的解析器"""
    def __init__(self, logFilePath='tmp'):
        if not os.path.exists(logFilePath):
            os.makedirs(logFilePath)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%S',
                            filename=logFilePath+"/LexFileParser.log",
                            filemode='w')

    def read_and_parse_lex(self, filePath):
        with open(filePath, 'rt') as file:
            lines = file.readlines()
        # local variables
        state = LexfileState.BeforePart1  # 当前处理的模块
        lineCount = 0  # 行号
        hasError = False
        findUpperPar = False
        action = []

        # return value
        part1_lines = []
        part4_lines = []
        maps = {}
        rules = []
        for line in lines:
            assert not hasError

            lineCount += 1
            line = line.strip()
            if line =="":
                continue

            if state == LexfileState.BeforePart1:
                if line == "%{":
                    state = LexfileState.Part1
                    logging.debug("Part1 Start")
                else:
                    hasError = True
                    logging.error("No entry sign %{")

            elif state == LexfileState.Part1:
                if line == "%}":
                    logging.debug("Part1 End, Part2 Start")
                    state = LexfileState.Part2
                else:
                    part1_lines.append(line)

            elif state == LexfileState.Part2:
                if line == "%%":
                    logging.debug("Part2 End, Part3 Start")
                    state = LexfileState.Part3
                else:
                    # 去除尾部注释
                    pass
                    vBuf = line.split()
                    if len(vBuf) == 2:
                        maps[vBuf[0]] = vBuf[1]
                    else:
                        logging.error("wrong input in line %d, Part 2:%s" % (lineCount, line))
                        hasError = True

            elif state == LexfileState.Part3:
                if line == "%%":
                    logging.debug("Part3 End, Part4 Start")
                    state = LexfileState.Part4
                else:
                    # 去掉尾部注释
                    pass
                    #去除首尾空格
                    line = line.strip()
                    # 如果在{}之间
                    if findUpperPar and line != "}":
                        logging.debug("add action, at line %d" % lineCount)
                        action.append(line)
                        findUpperPar = True
                    elif findUpperPar and line == "}":
                        logging.debug("find }, and add rule, at line %d" % lineCount)

                        rules.append(Rule(lhd, action))
                        logging.debug("pattern: " + rules[-1].pattern + "\t""action: " + str(rules[-1].action))
                        action.clear()
                        findUpperPar = False

                    # 如果不在{}之间
                    else:
                        # 对[和"开头的作特殊处理
                        if line[0] in ['[', '"', "'"]:
                            if line[0] == '[':
                                tag = ']'
                            else:
                                tag = line[0]
                            findUpperMark = True
                            i = 1
                            while i < len(line):
                                if line[i] == tag:
                                    findUpperMark = not findUpperMark
                                if i < len(line)-1 and (line[i+1].isspace() and findUpperMark is False):
                                    break
                                i += 1
                            lhd = line[0:i+1]
                            rhd = line[i+1:]
                            # trim(rhd)
                            rhd = rhd.strip()
                        else:
                            i = 0
                            while i < len(line):
                                if line[i].isspace():
                                    break
                                i += 1
                            lhd = line[0:i]
                            rhd = line[i:]
                            # trim(rhd)
                            rhd = rhd.strip()

                        if rhd != '{':
                            logging.debug("rhd is %s, at line %d" % (rhd, lineCount))
                            action.append(rhd)
                            rules.append(Rule(lhd, action))
                            action.clear()
                        else:
                            logging.debug("Find {! at line %d" % lineCount)
                            findUpperPar = True

            elif state == LexfileState.Part4:
                part4_lines.append(line)
        logging.debug("parser end")
        return maps, rules, part1_lines, part4_lines



