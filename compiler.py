#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from tokentype import *
from color_print import warning_print
import opcode
from objects import (FunObj, ModuleObj)
from parser import Parser
from objects import args_num
from vm import VM
from color_print import fatal_print


BP_NONE = 0
BP_LOWEST = 1
BP_ASSIGN = 2
BP_CONDITION = 3
BP_LOGIC_OR = 4 # or
BP_LOGIC_AND = 5 # and
BP_EQUAL = 6 # ==
BP_IS = 7 # is
BP_CMP = 8 # <=, >=, <, >
BP_BIT_OR = 9 # |
BP_BIT_AND = 10 # &
BP_BIT_SHIFT = 11 # >>, <<
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


# 标签函数定义区


def unused_rule():
    return Symbol()

def prefix_symbol(nud):
    sym = Symbol()
    sym.nud = nud
    return sym

def prefix_operator(id_, nud):
    sym = Symbol()
    sym.id = id_
    sym.nud = nud
    return sym

def infix_symbol(led, lbp):
    sym = Symbol()
    sym.lbp = lbp
    sym.led = led
    return sym

def infix_operator(id_, led, lbp):
    sym = Symbol()
    sym.id = id_
    sym.lbp = lbp
    sym.led = led
    return sym

def mix_operator(id_, led, nud, lbp):
    sym = Symbol()
    sym.led = led
    sym.nud = nud
    sym.lbp = lbp
    return sym

# int, float, str
def literal_nud(cu):
    cu.emit_load_constant(cu.cur_parser.pre_token.str)

# bool
def boolean_nud(cu):
    cu.write_opcode(opcode.PUSH_TRUE if cu.cur_parser.pre_token.type == TOKEN_TYPE_TRUE else opcode.PUSH_FALSE)

# (
def parentheses_nud(cu):
    expression(cu, BP_LOWEST)
    cu.cur_parser.error_if_cur_token_type_is_not(TOKEN_TYPE_RIGHT_PARENT, "parentheses doesn't match")

# .
def call_led(cu):
    cu.cur_parser.error_if_cur_token_type_is_not(TOKEN_TYPE_ID, "expect id after '.'")
    sign_name = cu.cur_parser.pre_token.str + '('
    # 处理调用实参
    arg_num = cu.handle_args()
    for i in range(arg_num):
        sign_name += '_,'
    if not arg_num:
        sign_name += ')'
    else:
        sign_name = sign_name[:-1] + ')'
    cu.emit_call(sign_name, arg_num)


# 数学运算符
def infix_operator_led(cu):
    rule = symbol_rules[cu.cur_parser.pre_token.type]
    expression(cu, rule.lbp)
    cu.emit_call(rule.id + '(_)', 1)

def nil_nud(cu):
    cu.write_opcode(opcode.PUSH_NIL)

def id_nud(cu):
    if cu.scope == SCOPE_MODULE:
        # global var 
        var = Var(cu.cur_parser.pre_token.str, cu.scope)
        if cu.cur_parser.to_next_token_if_cur_token_type_is(TOKEN_TYPE_ASSIGN):
            idx = cu.add_symbol(var)
            expression(cu, BP_LOWEST)
            cu.emit_store_module_variable(idx)
        else:
            cu.emit_load_module_variable(var)
    else:
        # local var
        var = Var(cu.cur_parser.pre_token.str, cu.scope)
        if cu.cur_parser.to_next_token_if_cur_token_type_is(TOKEN_TYPE_ASSIGN):
            idx = cu.add_symbol(var)
            expression(cu, BP_LOWEST)
            cu.emit_store_local_variable(idx)
        else:
            cu.emit_load_local_variable(var)

# list字面量[
def list_literal_nud(cu):
    # pre_token is [
    if cu.cur_parser.to_next_token_if_cur_token_type_is(TOKEN_TYPE_RIGHT_BRACKET):
        # empty
        cu.emit_load_module_variable()
        pass
    else:
        expression(cu, BP_LOWEST)
        while cu.cur_parser.to_next_token_if_cur_token_type_is(TOKEN_TYPE_COMMA):
            expression(cu, BP_LOWEST)
        pass
    pass

# 定义各种运算符的led与nud方法, 再绑定上去

symbol_rules = [unused_rule(), # if 0
                unused_rule(), # elif 1
                unused_rule(), # else 2
                unused_rule(), # for 3
                unused_rule(), # in 4
                unused_rule(), # while 5
                unused_rule(), # break 6
                unused_rule(), # not ? 7
                unused_rule(), # and ? 8
                unused_rule(), # or ? 9
                unused_rule(), # return ? 10
                unused_rule(), # import ? 11
                unused_rule(), # fun ? 12
                unused_rule(), # class ? 13
                unused_rule(), # let 14
                unused_rule(), # global 15
                prefix_symbol(boolean_nud), # true 16
                prefix_symbol(boolean_nud), # false 17
                unused_rule(), # continue 18
                unused_rule(), # del 19
                infix_operator('+', infix_operator_led, BP_BIT_TERM), # + 20
                infix_operator('-', infix_operator_led, BP_BIT_TERM), # - 21
                infix_operator('*', infix_operator_led, BP_BIT_FACTOR), # * 22
                infix_operator('/', infix_operator_led, BP_BIT_FACTOR), # / 23
                infix_operator('%', infix_operator_led, BP_BIT_FACTOR), # % 24
                unused_rule(), # ** ? 25
                unused_rule(), # ==? 26
                unused_rule(), # != ? 27
                unused_rule(), # >? 28
                unused_rule(), # <? 29
                unused_rule(), # >=? 30
                unused_rule(), # <=? 31
                unused_rule(), # = 32
                unused_rule(), # &? 33
                unused_rule(), # |? 34
                unused_rule(), # ^? 35
                unused_rule(), # ~? 36
                unused_rule(), # <<? 37
                unused_rule(), # >>? 38
                prefix_symbol(literal_nud), # num 39
                prefix_symbol(literal_nud), # str 40
                unused_rule(), # , 41
                infix_symbol(call_led, BP_BIT_CALL), # .方法调用 42
                unused_rule(), # : 43
                unused_rule(), # ; 44
                prefix_symbol(parentheses_nud), # ( 45
                unused_rule(), # ) 46
                unused_rule(), # [? 47
                unused_rule(), # ]? 48
                unused_rule(), # {? 49
                unused_rule(), # }? 50
                unused_rule(), # "? 51
                unused_rule(), # '? 52
                unused_rule(), # EOF 53
                unused_rule(), # unknow 54
                prefix_symbol(nil_nud), # 55
                prefix_symbol(id_nud), # 56
                prefix_symbol(literal_nud), # `
                unused_rule(), # lines 
                unused_rule(), # self
               ] 

def expression(cu, rbp):
    nud_fun = symbol_rules[cu.cur_parser.cur_token.type].nud
    cu.cur_parser.fetch_next_token()
    if not nud_fun:
        fatal_print('nud is None for token type ' + str(cu.cur_parser.pre_token.type))
        sys.exit(1)
    nud_fun(cu)
    while rbp < symbol_rules[cu.cur_parser.cur_token.type].lbp:
        led_fun = symbol_rules[cu.cur_parser.cur_token.type].led
        cu.cur_parser.fetch_next_token()
        led_fun(cu)


class CompileUnit(object):


    def __init__(self, parser, vm, fun_name='CORE', module=None, scope=SCOPE_MODULE):
        self.cur_parser = parser
        self.vm = vm
        parser.cur_cu = self
        self.scope = scope
        self.fun = FunObj(fun_name)
        # 运行时栈局部变量索引与local_vars符号表的索引一致
        self.local_vars = []
        self.local_var_num = 0
        self.outter_cu = None
        self.cur_loop = None
        self.module = ModuleObj('CORE')
    
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
    def emit_load_constant(self, var):
        idx = self.fun.add_constant(var)
        self.write_opcode_operand(opcode.LOAD_CONST, idx)
    
    # 对于变量来说, 现有store, 再有load, store在没有变量的时候在栈中创建对象, 在有变量的时候赋值
    def emit_load_local_variable(self, var):
        idx = self.add_symbol(var)
        self.write_opcode_operand(opcode.LOAD_LOCAL, idx)
        var.idx = idx

    def emit_load_module_variable(self, var):
        idx = self.module.add_module_var(var)
        self.write_opcode_operand(opcode.LOAD_GLOBAL, idx)
        var.idx = idx
    
    def emit_store_local_variable(self, idx):
        self.write_opcode_operand(opcode.STORE_LOCAL, idx) 

    def emit_store_module_variable(self, idx):
        self.write_opcode_operand(opcode.STORE_GLOBAL, idx)

    def emit_store_constant(self, idx):
        self.write_opcode_operand(opcode.STORE_CONST, idx)
    
    # 这种一般operand就是写在指令流中
    def write_opcode_operand(self, op, operand):
        self.fun.stream.append(op)
        self.fun.stream.append(operand)
        self.fun.stream_num += 1
        # 返回opcode所在的下标
        return self.fun.stream_num - 2
    
    # 这种一般operand在栈中
    def write_opcode(self, op):
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
        self.cur_parser.error_if_cur_token_type_is_not(TOKEN_TYPE_LEFT_PARENT, "expect '(' after method name")
        arg_num = 0
        if not self.cur_parser.cur_token.type == TOKEN_TYPE_RIGHT_PARENT:
            arg_num += 1
            # has args
            expression(self, BP_LOWEST)
            while self.cur_parser.to_next_token_if_cur_token_type_is(TOKEN_TYPE_COMMA):
                arg_num += 1
                expression(self, BP_LOWEST)
        self.cur_parser.error_if_cur_token_type_is_not(TOKEN_TYPE_RIGHT_PARENT, "parentheses doesn't match") 
        return arg_num

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
        # name is method name
        # s格式为nil0|bool2|str1, 在运行时再根据类型找方法来调用
        s = ''
        for cls in self.vm.builtin_clses:
            try: 
                idx = cls.method_names.index(name)
                s += cls.name + str(idx) + '|'
            except ValueError:
                pass
        if not s:
            fatal_print('%s is not defined' % name)
            sys.exit(1)
        self.write_opcode_operand(opcode.CALL0 + arg_num, s[:-1])

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
    cu = CompileUnit(Parser('./demo.y'), vm)
    cu.scope = SCOPE_LOCAL
    cu.cur_parser.fetch_next_token()
    while True:
        if cu.cur_parser.cur_token.type == TOKEN_TYPE_EOF:
            break
        expression(cu, BP_LOWEST)
    opcode.opcode_print(cu.fun.stream)


if __name__ == '__main__':
    main()

