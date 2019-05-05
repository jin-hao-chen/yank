#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from tokentype import *
from color_print import warning_print
import opcode


BP_LOWEST = 0
BP_HIGHEST = 100


MT_METHOD = 1
MT_SETTER = 2
MT_GETTER = 3
MT_SUB_SETTER = 4
MT_SUB_GETTER = 5


SCOPE_INVALID = 1
SCOPE_MODULE = 2
SCOPE_LOCAL = 3


class Var(object):


    def __init__(self, name, scope, idx=0):
        self.name = name
        self.scope = scope
        self.idx = idx

    def __eq__(self, other):
        return self.name == other.name


class MethodSign(object):


    def __init__(self, mt_type, string):
        self.type = mt_type
        # part not full
        self.str = string


class Symbol(object):


    def __init__(self):
        # 当前token的字符串
        self.id = ''
        self.led = None
        self.nud = None
        # 方法签名
        self.method_sign_fn = None
        self.lbp = 0


# 定义各种运算符的led与nud方法, 在绑定上去
# infix

symbol_rules = []


class CompileUnit(object):


    def __init__(self, parser, scope=0, module=None, fun=None):
        self.cur_parser = parser
        self.fun = fun
        self.scope = scope
        self.local_vars = []
        self.local_var_num = 0
        self.outter_cu = None
        self.cur_loop = None
    
    def add_symbol(self, var):
        for i in range(len(self.local_vars)): 
            if var == self.local_vars[i]:
                return i
        self.local_vars.append(var)
        self.local_var_num += 1
        return self.local_var_num - 1

    def write_opcode(self, opcode):
        self.fun.stream.append(opcode)

    def emit_load_constant(self, var, cons):
        self.write_opcode_operand(opcode.LOAD_CONST, )

    def write_opcode_operand(self, opcode, operand):
        pass
    
    def define_var(self, var):
        pass
    
    def discard_var(self, var):
        pass

    def compile(self):
        while True:
            self.parser.fetch_next_token()
            if self.parser.cur_token.type == TOKEN_TYPE_EOF:
                return
            print(self.parser.cur_token)
        pass

    def compile_statement(self):
        pass

    def compile_if_statement(self):
        pass

    def compile_while_statement(self):
        pass

    def compile_return_statement(self):
        pass

    def compile_import_statement(self):
        pass


class Loop(object):


    def __init__(self, scope=0):
        self.scope = scope
        self.condition_start = 0
        self.body_start = 0
        self.exit = 0
        self.outter_loop = None


def main(argv=None):
    pass


if __name__ == '__main__':
    main()

