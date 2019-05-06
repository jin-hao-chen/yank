#!/usr/bin/env python
# -*- coding: utf-8 -*-


LOAD_CONST = 0
STORE_CONST = 1
LOAD_LOCAL = 2
STORE_LOCAL = 3
LOAD_GLOBAL = 4
STORE_GLOBAL = 5
RETURN_VALUE = 6 # 回收frame并返回返回值到老的栈顶
PUSH_NIL = 7
POP = 8
JUMP_IF_FALSE = 9
JUMP = 10
PUSH_TRUE = 11
PUSH_FALSE = 12
LOOP = 13


CALL0 = 18
CALL1 = 19
CALL2 = 20
CALL3 = 21
CALL4 = 22
CALL5 = 23
CALL6 = 24
CALL7 = 25
CALL8 = 26
CALL9 = 27
CALL10 = 28
CALL11 = 29
CALL12 = 30
CALL13 = 31
CALL14 = 32
CALL15 = 33
CALL16 = 34
CALL17 = 35
CALL18 = 36
CALL19 = 37
CALL20 = 38


AND = 50
OR = 51
NOT = 52
END = 100


def opcode_print(stream):
    ptr = 0
    stream_len = len(stream)
    while ptr < stream_len:
        op = stream[ptr]
        s = ''
        if op == LOAD_CONST:
            s += 'LOAD_CONST '
            ptr += 1
            operand = stream[ptr]
            s += str(operand)
        ptr += 1
        print(s)
