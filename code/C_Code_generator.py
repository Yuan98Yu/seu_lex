from structs import Mode


class CCodeGenerator:
    def __print_array(self, name, size, value, file):
        array_buf = value
        file.write("static int	%s[%d]=\n" % (name, size))
        file.write("{ 0,\n")
        for i in range(1, size):
            file.write("%-4s" % array_buf[i])
            if i != size - 1:
                    file.write(",")
            if i % 10 == 0:
                file.write("\n")
        file.write("};\n")

    def generate_c_code(self, arrays, endVec, part1, part4, startState, mode, filepath):
        if len(arrays) != 4:
            return -1
        with open(filepath, 'w') as file:
            file.write("#define _CRT_SECURE_NO_WARNINGS\n")
            file.write("#include\"stdio.h\"\n")
            file.write("#include\"stdlib.h\"\n")
    
            file.write("#include<string.h>\n")
            file.write("#define START_STATE %d\n" % startState)
            # 依次输出P1和P4
            for s in part1:
                file.write(s + '\n')

            file.write("char* getCharPtr(char* fileName);\n")
            file.write("int findAction(int action);\n")  # 函数声明
            # file.write("void addToken(int token);\n") # 将token加入Token序列 * /
            file.write("void comment();\n") # comment函数，啥都不做 * /

            # 依次输出ec表, base表, next表, accept表
            array_name = ["yy_ec", "yy_base", "yy_next", "yy_accept"]
    
            for i in range(4):
                self.__print_array(array_name[i], arrays[i][1], arrays[i][0], file)
    
            # 定义若干变量
            file.write("int yy_current_state = START_STATE;\n")
            file.write("int yy_last_accepting_state = -1;\n")
            file.write("char *yy_cp = NULL;\n")
            file.write("char *yy_last_accepting_cpos = NULL;\n")
            file.write("int yy_act = 0;\n")
            file.write("int isEnd=0;\n")
            file.write("int yy_c=-1;\n")
            file.write("int correct=1;\n")
    
            # 一些初始化动作
            file.write("void lex_init(char* fileName)\n")
            file.write("{\n")
            # 调用char * getCharPtr(char * fileName)
            # 得到文件字符指针
            file.write("yy_cp=getCharPtr(fileName);\n")
            file.write("}\n")
    
            if mode == Mode.YACC_TEST:
                file.write("int yy_lex()\n")
                file.write("{\n")
            if mode == Mode.LEX_TEST:
                file.write("int main(int argc,char** argv)\n")
                file.write("{\n")
                file.write("if(argc==2)\n")
                file.write("{\n")
                file.write("lex_init(argv[1]);\n")
                file.write("}\n")
                file.write("else{\n")
                file.write("printf(\"ERROR: invalid argument!\\n\");\n")
                file.write("return -1;\n")
                file.write("}\n")

            file.write("if (isEnd&&correct)\n")
            file.write("{\n")
            file.write("\treturn -1;\n")
            file.write("}\n")
            file.write("else if (isEnd && !correct)\n")
            file.write("{\n")
            file.write("\treturn -2;\n")
            file.write("}\n")
            file.write("int result = 0;\n")
            file.write("while (*yy_cp != 0) {\n")
            file.write("\tyy_c = yy_ec[(int)*yy_cp];\n")
            file.write("\tif (yy_accept[yy_current_state])\n")
            file.write("\t{\n")
            file.write("\tyy_last_accepting_state = yy_current_state;\n")
            file.write("\tyy_last_accepting_cpos = yy_cp;\n")
            file.write("\t}\n")
            file.write("\tif (yy_next[yy_base[yy_current_state] + yy_c] == -1 && yy_last_accepting_state != -1)\n")
            file.write("\t{\n")
            file.write("\tyy_current_state = yy_last_accepting_state;\n")
            file.write("\tyy_cp = yy_last_accepting_cpos;\n")
            file.write("\tyy_act = yy_accept[yy_current_state];\n")
            file.write("\tresult = findAction(yy_act);\n")
            if mode == Mode.YACC_TEST:
                file.write("\tif (result != -1)\n")
                file.write("\t{\n")
                file.write("\tyy_current_state = START_STATE;\n")
                file.write("\tyy_last_accepting_state = -1;\n")
                file.write("\t++yy_cp;\n")
                file.write("\tyy_current_state = yy_next[yy_base[yy_current_state] + yy_c];\n")
                file.write("\tbreak;\n")
                file.write("\t}\n")
                file.write("\tif (result == -1)\n")
                file.write("\t{\n")
                file.write("\tyy_current_state = START_STATE;\n")
                file.write("\tyy_last_accepting_state = -1;\n")
                file.write("\t++yy_cp;\n")
                file.write("\tyy_current_state = yy_next[yy_base[yy_current_state] + yy_c];\n")
                file.write("\tcontinue;\n")
                file.write("\t}\n")

            elif mode == Mode.LEX_TEST:
                file.write("\tprintf(\" \");\n")
                file.write("\tyy_current_state = START_STATE;\n")
                file.write("\tyy_last_accepting_state = -1;\n")
                file.write("\t++yy_cp;\n")
                file.write("\tyy_current_state = yy_next[yy_base[yy_current_state] + yy_c];\n")
                file.write("\tcontinue;\n")
    
            file.write("\t}\n")
            file.write("\tif (yy_next[yy_base[yy_current_state] + yy_c] == -1 && yy_last_accepting_state == -1)\n")
            file.write("{\n")
            file.write("\tprintf(\"ERROR DETECTED IN INPUT FILE !\");\n")
            if mode == Mode.LEX_TEST:
                file.write("\treturn -1;\n")

            file.write("\t}\n")
            file.write("if (yy_next[yy_base[yy_current_state] + yy_c] != -1) \n")
            file.write("{\n")
            file.write("\t\tyy_current_state = yy_next[yy_base[yy_current_state] + yy_c];\n")
            file.write("\t++yy_cp;\n")
            file.write("\t}\n")
            file.write("}\n")
            file.write("if (*yy_cp == 0) {\n")
            file.write("isEnd = 1;\n")
            file.write("\tif (yy_accept[yy_current_state] && yy_cp == yy_last_accepting_cpos + 1)\n")
            file.write("{\n")
            file.write("\tyy_act = yy_accept[yy_current_state];\n")
            file.write("\tresult = findAction(yy_act);\n")
            file.write("}\n")
    
            file.write("else \n")
            file.write("{\n")
            file.write("\tprintf(\"ERROR DETECTED IN INPUT FILE !\");\n")
            file.write("\tcorrect = 0;\n")
            if mode == Mode.LEX_TEST:
                file.write("\treturn -1;\n")

            file.write("}\n")
            file.write("}\n")
            if mode == Mode.LEX_TEST:
                file.write("\treturn 0;\n")
            else:
                file.write("\treturn result;\n")

            file.write("}\n")  # lex_main函数结束
            # int findAction(int action)函数
            file.write("int findAction(int action)\n")
            file.write("{\n")
            file.write("switch (action) \n")  # 根据endVec打印switch语句
            file.write("{\n")
            file.write("case 0:\n")
            # ...此处省略了一些东西
            file.write("break;\n")
            for i in range(len(endVec)):
                p=i+1
                file.write("case %d:\n" % p)
                for j in range(len(endVec[i].action)):
                    file.write(endVec[i].action[j]+"\n")
                file.write("break;\n")

            file.write("default:\n")
            file.write("break;\n")
            file.write("}\n")
            # int findAction(int state）函数的下括号
            file.write("return -1;\n")
            file.write("}\n")
            # int findAction(int action)函数的下括号
            # char * getCharPtr(char * fileName)
            file.write("char* getCharPtr(char* fileName){\n")
            file.write("char* cp=NULL;\n")
            file.write("FILE *fp;\n")
            file.write("fp=fopen(fileName,\"r\");\n")
            file.write("if(fp==NULL)\n")
            file.write("{\n")
            file.write("printf(\"can't open file\");\n")
            file.write("exit(0);\n")
            file.write("}\n")
            file.write("fseek(fp,0,SEEK_END);\n")
            file.write("int flen = ftell(fp);\n")  # 得到文件大小
            file.write("cp = (char *)malloc(flen + 1);\n")  # 根据文件大小动态分配内存空间
            file.write("if (cp == NULL)\n")
            file.write("{\n")
            file.write("fclose(fp);\n")
            file.write("\treturn 0;\n")
            file.write("}\n")
            file.write("rewind(fp);\n") # 定位到文件开头
            file.write("memset(cp,0,flen+1);\n")
            file.write("fread(cp, sizeof(char), flen, fp);\n")  # 一次性读取全部文件内容
            file.write("cp[flen] = 0; \n")  # 字符串结束标志
            file.write("return cp;\n")
            file.write("}\n")
    
            for s in part4:
                file.write(s+"\n")
