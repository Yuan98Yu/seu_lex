from structs import ALLSET, ESCAPEDCHARS, Rule
import logging
import os

class REStandardization_parser:
    def __init__(self, log_file_path='../tmp'):
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        logging.basicConfig(filename=log_file_path+'/debug_REStandardization.txt', filemode='w', level=logging.DEBUG)
        logging.FileHandler(log_file_path+'/debug_REStandardization.txt', 'w')
    def __handle_escape(self, exp, isin):
        logging.debug('start handle_escape, exp: %s' % exp)
        stemp = ''
        flag = False
        for c in exp:
            if isin:  # 转义[]内的所有可能字符
                if flag:
                    if c == 'n':
                        stemp += '\n'
                    elif c == 't':
                        stemp += '\t'
                    elif c == 'v':
                        stemp += '\v'
                    elif c == 'f':
                        stemp += '\f'
                    elif c == '\\':
                        stemp += '\\'
                    flag = False
                    continue
                if c == '\\':
                    flag = True
                    continue
            else:
                if flag:
                    flag = False
                    if c == '\"' or c == '\\':
                        stemp = stemp[0:-1]
                elif c == '\\':
                    flag = True
            stemp += c
        exp = stemp
        logging.debug('result exp: %s' % exp)
        logging.debug('len of exp: %d'% len(exp))
        return exp

    def __handle_quote(self, exp):
        in_quote = False
        sexp_it = 0
        char_vec = []
        for exp_it in range(len(exp)):
            if exp[exp_it] == '\"' and ((exp_it != sexp_it and exp[exp_it-1] != '\\') or exp_it == sexp_it):
                if not in_quote:
                    in_quote = True
                    continue
                else:
                    in_quote = False
                    continue
            elif in_quote and exp[exp_it] in ESCAPEDCHARS:
                char_vec.append('`')
            char_vec.append(exp[exp_it])
        exp = "".join(char_vec)
        return exp

    def __add_dot(self, exp):
        old_exp = exp
        doted_exp = ''
        for old_exp_it in range(len(old_exp)):
            doted_exp += old_exp[old_exp_it]
            if old_exp[old_exp_it] == '`':
                continue
            if (old_exp[old_exp_it] in ['(', '|']) \
                    and (old_exp[old_exp_it] == old_exp[0] or old_exp[old_exp_it-1] != '`'):
                continue
            if old_exp_it + 1 == len(old_exp):
                continue
            if old_exp[old_exp_it+1] in ['|', '*', ')']:
                continue
            doted_exp += '.'
        return doted_exp

    def __construct_char_set(self, content, n):
        s = set()  # output
        logging.debug("start construct_char_set, content=%s" % content)
        stemp = content
        stemp = self.__handle_escape(stemp, True)
        # 处理[a-z]
        tmp_set = set()
        for it in range(len(stemp)):
            logging.debug('it in construct_char_set: %d,\t'
                          'stemp[it]:%s' % (it, stemp[it]))
            if stemp[it] == '-' and it != 0 and it+1 != len(stemp)\
                    and stemp[it-1].isalnum() and stemp[it+1].isalnum():
                sit = ALLSET.find(stemp[it-1]) + 1
                eit = ALLSET.find(stemp[it+1])
                logging.debug('sit:%d, eit:%d' % (sit, eit))
                if eit <= sit:
                    raise Exception("UNDONE: 报错：[]内部格式不对")
                while sit != eit:
                    tmp_set.add(ALLSET[sit])
                    sit += 1
            else:
                tmp_set.add(stemp[it])

        if n:
            #logging.debug('tmp_set is %s'% tmp_set)
            for c in ALLSET:
                if c not in tmp_set:
                    s.add(c)
        else:
            s = tmp_set
        logging.debug('result s: %s' % "".join(s))
        return s

    def __replace_brace(self, exp, reMap):
        rename = ""
        char_vec = []
        inBrace = False
        for exp_it in range(len(exp)):
            if exp[exp_it] == '{' and (exp_it == 0 or exp[exp_it-1] != '`'):
                inBrace = True
                rename = ""
            elif inBrace and (exp[exp_it] == '}' and (exp_it == 0 or exp[exp_it-1] != '`')):
                inBrace = False
                findIt = reMap.get(rename, None)
                logging.debug('rule.pattern:%s' % rename)
                logging.debug('reMap:')
                logging.debug(reMap)
                logging.debug('findIt:%s' % findIt)
                if findIt is not None:
                    for c in findIt:
                        char_vec.append(c)
                else:
                    raise Exception("UNDONE: 报错，找不到前面的name")
            elif inBrace:
                rename += exp[exp_it]
            else:
                char_vec.append(exp[exp_it])

        exp = "".join(char_vec)
        return exp

    def __replace_square_brace(self, exp):
        sbcontent = ""
        char_vec = []
        inSquareBrackes = False
        for exp_it in range(len(exp)):
            if exp[exp_it] == '[' and (exp_it == 0 or exp[exp_it-1] != '`'):
                inSquareBrackes = True
                sbcontent = ""
            elif exp[exp_it] == ']' and inSquareBrackes and (exp_it == 0 or exp[exp_it-1] != '`'):
                #logging.debug("find the ]")
                inSquareBrackes = False
                char_vec.append('(')
                s = set()
                if sbcontent[0] == '^':
                    s = self.__construct_char_set(sbcontent[1:], True)
                else:
                    s = self.__construct_char_set(sbcontent, False)
                for c in s:
                    if c in ESCAPEDCHARS:
                        char_vec.append('`')
                    char_vec.append(c)
                    char_vec.append('|')
                char_vec.pop()
                char_vec.append(')')
            elif inSquareBrackes:
                sbcontent += exp[exp_it]
            else:
                char_vec.append(exp[exp_it])

        exp = "".join(char_vec)
        return exp

    def __replace_dot(self, exp):
        char_vec = []
        for exp_it in range(len(exp)):
            if exp[exp_it] == '.' and (exp_it == 0 or (exp_it != len(exp)-1 and exp[exp_it-1] != '`')):
                char_vec.append('(')
                s = self.__construct_char_set('\n', True)
                for c in s:
                    if c in ESCAPEDCHARS:
                        char_vec.append('`')
                    char_vec.append(c)
                    char_vec.append('|')
                char_vec.pop()
                char_vec.append(')')
            else:
                char_vec.append(exp[exp_it])

        exp = "".join(char_vec)
        return exp

    def __replace_question_and_add(self, exp):
        char_vec = []
        exp_it = 0
        while exp_it < len(exp):
            if exp[exp_it] in ['+', '?'] and (exp_it == 0 or (exp_it != 0 and exp[exp_it-1] != '`')):
                counter = 0
                if (exp_it != 0 and exp[exp_it-1] == ')') and ((exp_it-1 != 0 and exp[exp_it-2] != '`') or exp_it-1 == 0):
                    pre_exp_it = exp_it
                    exp_it -= 1
                    char_vec.pop()
                    counter += 1
                    while counter > 0:
                        char_vec.pop()
                        exp_it -= 1
                        if exp[exp_it] == '(' and ((exp_it != 0 and exp[exp_it-1] != '`') or exp_it == 0):
                            counter -= 1
                        elif exp[exp_it] == ')' and ((exp_it != 0 and exp[exp_it - 1] != '`') or exp_it == 0):
                            counter += 1
                    if exp[pre_exp_it] == '?':
                        char_vec.append('(')
                        char_vec.append('@')
                        char_vec.append('|')
                        while exp_it != pre_exp_it:
                            char_vec.append(exp[exp_it])
                            exp_it += 1
                        char_vec.append(')')
                    else:
                        start_it = exp_it
                        for i in range(2):
                            exp_it = start_it
                            while exp_it != pre_exp_it:
                                char_vec.append(exp[exp_it])
                                exp_it += 1
                        char_vec.append('*')
                else:
                    c = char_vec[-1]
                    if exp[exp_it] == '?':
                        char_vec.pop()
                        char_vec.append('(')
                        char_vec.append('@')
                        char_vec.append('|')
                        char_vec.append(c)
                        char_vec.append(')')
                    else:
                        char_vec.append(c)
                        char_vec.append('*')
                exp_it += 1
                while exp_it != len(exp):
                    char_vec.append((exp[exp_it]))
                    exp_it += 1
                exp = "".join(char_vec)
                char_vec.clear()
                exp_it = 0
                continue
            char_vec.append(exp[exp_it])
            exp_it += 1

        exp = "".join(char_vec)
        return exp

    def re_standardize(self, rules, reMap):
        for p1, p in reMap.items():
            p = self.__handle_quote(p)
            reMap[p1] = self.__replace_brace(p, reMap)
            logging.debug('p: %s'% p)
            logging.debug('p1:%s' % p1)
            logging.debug('reMap[p1]:%s' % reMap[p1])

        for rule in rules:
            rule.pattern = self.__handle_quote(rule.pattern)
            logging.debug('handle_quote:%s' % rule.pattern)
            rule.pattern = self.__replace_brace(rule.pattern, reMap)
            logging.debug('replace_brace:%s' % rule.pattern)
            rule.pattern = self.__replace_square_brace(rule.pattern)
            logging.debug('replace_square_brace:%s' % rule.pattern)
            rule.pattern = self.__replace_dot(rule.pattern)
            logging.debug('replace_dot:%s' % rule.pattern)
            rule.pattern = self.__replace_question_and_add(rule.pattern)
            logging.debug('replace_question_and_add:%s' % rule.pattern)
            rule.pattern = self.__handle_escape(rule.pattern, False)
            logging.debug('handle_escape:%s' % rule.pattern)
            rule.pattern = self.__add_dot(rule.pattern)
            logging.debug('add_dot:%s' % rule.pattern)

        return rules
