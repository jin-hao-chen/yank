#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from tokentype import *
from color_print import warning_print
import opcode
from objects import FunObj


BP_NONE = 0
BP_LOWEST = 1
BP_CONDITION = 2
BP_LOGIC_OR = 3 # or
BP_LOGIC_AND = 4 # and
BP_EQUAL = 5 # ==
BP_IS = 6 # is
BP_CMP = 7 # <=, >=, <, >
BP_BIT_OR = 8 # |
BP_BIT_AND = 9 # &
BP_BIT_SHIFT = 10 # >>, <<
BP_BIT_TERM = 12 # +, -
BP_BIT_FACTOR = 13 # *, /
BP_BIT_UNARY = 14 # not, -, ~
BP_BIT_CALL = 15 # ., (), []
BP_HIGHEST = 16


SIGN_METHOD = 1 SIGN_SETTER = 2
SIGN_GETTER = 3
SIGN_SUB_SETTER = 4
SIGN_SUB_GETTER = 5


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
        self.id = None
        self.led = None
        self.nud = None
        # 方法签名
        self.sign_fn = None
        self.lbp = BP_NONE

"""
符号分为两种, 运算符与符号
运算符(operator): 有id, led, nud, sign_bp, lbp
符号(symbol): 无id和sign_bp, 有led, nud, lbp
它们主要的区别是运算符可以重载, 符号不可以重载

prefix_symbol
prefix_operator

infix_symbol
infix_operator

mix_operator

"""

# nud和led定义区

# 数字和字符串的nud
def literal(cu):
    cu.emit_load_constant()

# 标签函数定义区


def unused_rule():
    return Symbol()

def prefix_symbol(nud):
    pass

def prefix_operator(id_, nud, sign_fn):
    pass

def infix_symbol(led):
    pass

def infix_operator(id_, led, sign_fn, lbp):
    pass

def mix_operator(id_, led, nud, sign_fn, lbp):
    pass


# 定义各种运算符的led与nud方法, 再绑定上去

symbol_rules = []


def expression(cu, rbp):
    nud_fun = symbol_rules[cu.cur_parser.cur_token.type].nud
    cu.cur_parser.fetch_next_token()
    nud_fun(cu) 
    while rbp < symbol_rules[cu.cur_parser.cur_token.type].lbp:
        led_fun = symbol_rules[cu.cur_parser.cur_token.type].led
        cu.cur_parser.fetch_next_token()
        led_fun(cu)


class CompileUnit(object):


    def __init__(self, parser, fun_name='CORE', scope=0):
        self.cur_parser = parser
        parser.cur_cu = self
        self.scope = scope
        self.fun = FunObj(fun_name)
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
    
    # 字符串和数据字面量比较特别, 与其他变量相比, 他们是常量, 要放到常量表中
    def emit_load_constant(self, value):
        idx = self.fun.add_constant(value)
        self.write_opcode_operand(opcode.LOAD_CONST, idx)
    
    # 这种一般operand就是写在指令流中
    def write_opcode_operand(self, op, operand):
        self.fun.stream.append(op)
        self.fun.stream.append(operand)
        self.fun.stream_num += 1
        # 返回opcode所在的下标
        return self.fun.stream_num - 2
    
    # 这种一般operand在栈中
    def write_opcode(self, opcode):
        self.fun.stream.append(op)
        self.fun.stream_num += 1
        return self.fun.stream_num - 1

    def define_var(self, var):
        pass
    
    def discard_var(self, var):
        pass

    def compile(self):
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

