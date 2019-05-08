#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from tokentype import *
from color_print import warning_print
import opcode
from objects import FunObj
from parser import Parser
from objects import args_num
from vm import VM
from color_print import fatal_print


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


SIGN_METHOD = 1 
SIGN_SETTER = 2
SIGN_GETTER = 3
SIGN_SUB_SETTER = 4
SIGN_SUB_GETTER = 5


SCOPE_INVALID = 1
SCOPE_LOCAL = 2
SCOPE_MODULE = 3


class Var(object):


    def __init__(self, name, scope, idx=0):
        self.name = name
        self.scope = scope
        self.idx = idx

    def __eq__(self, other):
        return self.name == other.name


class MethodSign(object):


    def __init__(self, sign_type, name):
        self.sign_type = sign_type
        self.name = name
        self.arg_num = 0


class Symbol(object):


    def __init__(self):
        # 当前token的字符串
        self.id = None
        self.led = None
        self.nud = None
        # 用于语法和语义分析
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
def literal_nud(cu):
    cu.emit_load_constant()

# 标签函数定义区


def unused_rule():
    return Symbol()

def prefix_symbol(nud):
    sym = Symbol()
    sym.nud = nud
    return sym

def prefix_operator(id_, nud, sign_fn):
    sym = Symbol()
    sym.id = id_
    sym.nud = nud
    sym.sign_fn = sign_fn 
    return sym

def infix_symbol(led):
    sym = Symbol()
    sym.led = led
    return sym

def infix_operator(id_, led, sign_fn, lbp):
    sym = Symbol()
    sym.id = id_
    sym.led = sign_fn
    sym.lbp = lbp

def mix_operator(id_, led, nud, sign_fn, lbp):
    sym = Symbol()
    sym.led = led
    sym.nud = nud
    sym.sign_fn = sign_fn
    sym.lbp = lbp
    return sym


# 定义各种运算符的led与nud方法, 再绑定上去

symbol_rules = [unused_rule(), # if
                unused_rule(), # elif
                unused_rule(), # else
                unused_rule(), # for,
                unused_rule(), # in
                unused_rule(), # while
                unused_rule(), # break
                prefix_symbol(nud), # not
               ] 


def expression(cu, rbp):
    nud_fun = symbol_rules[cu.cur_parser.cur_token.type].nud
    cu.cur_parser.fetch_next_token()
    nud_fun(cu) 
    while rbp < symbol_rules[cu.cur_parser.cur_token.type].lbp:
        led_fun = symbol_rules[cu.cur_parser.cur_token.type].led
        cu.cur_parser.fetch_next_token()
        led_fun(cu)


class CompileUnit(object):


    def __init__(self, parser, vm, fun_name='CORE', scope=SCOPE_MODULE):
        self.cur_parser = parser
        self.vm = vm
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

    def sign_to_str(self, sign):
        # 此时的sign已经完整
        if sign.sign_type == SIGN_GETTER:
            return sign.name
        elif sign.sign_type == SIGN_SETTER:
            return sign.name + '=(_)'
        elif sign.sign_type == SIGN_METHOD:
            s = '('
            for i in range(sign.arg_num):
                s += '_,'
            return sign.name + s[:-1] + ')'
        # sub_getter也有参数
        elif sign.sign_type == SIGN_SUB_GETTER:
            s = '['
            for i in range(sign.arg_num):
                s += '_,'
            return sign.name + s[:-1] + ']'
        
        elif sign.sign_type == SIGN_SUB_SETTER:
            s = '['
            for i in range(sign.arg_num - 1):
                s += '_,'
            return sign.name + s[:-1] + ']=(_)'
    
    # 字符串和数据字面量比较特别, 与其他变量相比, 他们是常量, 要放到常量表中
    def emit_load_constant(self, value):
        idx = self.fun.add_constant(value)
        self.write_opcode_operand(opcode.LOAD_CONST, idx)
    
    def emit_load_local_variable(self):
        pass

    def emit_load_module_variable(self):
        pass
    
    def emit_store_local_variable(self):
        pass

    def emit_store_module_variable(self):
        pass

    def emit_store_constant(self):
        pass
    
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

    def define_local_variable(self, var):
        pass
    
    def define_module_variable(self, var):
        pass
    
    def discard_var(self, var):
        pass

    def compile_module(self):
        """
        compile_module -> compile_program -> compile_statement
        """
        pass

    def end_compile(self):
        pass

    def enter_scope(self):
        self.scope += 1

    def leave_scope(self):
        pass
    
    def handle_args(self):
        pass

    def handle_parameters(self):
        pass
    
    def compile_block(self):
        pass

    def compile_program(self):
        pass

    def compile_statement(self):
        pass

    def compile_if_statement(self):
        pass

    def compile_while_statement(self):
        pass

    def compile_return_statement(self):
        pass

    def compile_import(self):
        pass

    def compile_break_statement(self):
        pass
    
    def compile_continue_statement(self):
        pass

    def emit_call(self, name, arg_num):
        idx = self.vm.fine_method_name(name)
        if idx == -1:
            fatal_print('%s is not defined' % name)
            sys.exit(1)
        self.write_opcode_operand(opcode.CALL0 + arg_num, idx)

    def emit_call_by_sign(self, sign):
        sign_name = self.sign_to_str(sign)
        self.emit_call(sign_name, sign.arg_num)
    


class Loop(object):


    def __init__(self, scope=0):
        self.scope = scope
        self.condition_start = 0
        self.body_start = 0
        self.exit = 0
        self.outter_loop = None


def main(argv=None):
    vm = VM()
    cu = CompileUnit(Parser('./example.y'), vm)
    sign = MethodSign(SIGN_SUB_SETTER, 'my_method')
    sign.arg_num = 2
    print(cu.sign_to_str(sign))
    print(cu.emit_call(cu.sign_to_str(sign), 2))


if __name__ == '__main__':
    main()

