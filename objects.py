#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from color_print import *


def call(obj, method_name):
    return obj.obj_header.cls_obj.methods[method_name]


def type_to_pystr(obj):
    if obj.obj_header.obj_type == 'int':
        return int_to_str(obj).str
    elif obj.obj_header.obj_type == 'float':
        return float_to_str(obj).str
    elif obj.obj_header.obj_type == 'str':
        return str_to_str(obj).str
    elif obj.obj_header.obj_type == 'list':
        return list_to_str(obj).str
    elif obj.obj_header.obj_type == 'map':
        return map_to_str(obj).str
    elif obj.obj_header.obj_type == 'nil':
        return nil_to_str(obj).str
    elif obj.obj_header.obj_type == 'bool':
        return bool_to_str(obj).str

def is_type(obj, name):
    return obj.obj_header.obj_type == name

def args_num(pystr):
    left = pystr.find('(')
    right = pystr.rfind(')')
    args_str = s[left + 1: right]
    return len(args_str.split(','))


class ObjHeader(object):
    

    def __init__(self, obj_type, cls_obj, obj):
        self.obj_type = obj_type 
        self.cls_obj = cls_obj
        self.obj = obj


class ClsObj(object):


    def __init__(self, name):
        self.name = name
        self.methods = {}


class VM(object):


    def __init__(self):
        self.fun_cls = fun_cls
        self.nil_cls = nil_cls
        self.bool_cls = bool_cls
        self.str_cls = str_cls
        self.int_cls = int_cls
        self.float_cls = float_cls
        self.list_cls = list_cls
        self.map_cls = map_cls


"""
还有module, fun
map对象比较特别, 在yank中就是对象, map的remove, put, get在内部的方式是@remove, @put, @get, 因为yank中通过map实现对象的, 模仿一下js
"""

fun_cls = ClsObj('fun_cls')
nil_cls = ClsObj('nil_cls')
bool_cls = ClsObj('bool_cls')
str_cls = ClsObj('str_cls')
int_cls = ClsObj('int_cls')
float_cls = ClsObj('float_cls')
list_cls = ClsObj('list_cls')
map_cls = ClsObj('map_cls')

vm = VM()

########################### fun methods ###########################
# for function object, not for methods of bool, str, int and so on.
# 参数被封装成了yank_list
# 出现say(_,_)这种形式时

def fun_call(obj, args):
    # obj为fun object
    # 执行的是指令流
    pass

############################ nil methods ###########################

def nil_to_str(obj):
    return StrObj(str(obj.nil))

def nil_equ(obj1, obj2):
    if obj2.obj_header.obj_type != 'nil':
        return BoolObj(False)
    return BoolObj(True)

def nil_bind_methods():
    nil_cls.methods['tostr(_)'] = nil_to_str
    nil_cls.methods['==(_,_)'] = nil_equ

############################# bool methods ###################

def bool_to_str(obj):
    return StrObj(str(obj.bool))

def bool_equ(obj1, obj2):
    return BoolObj(obj1.bool == obj2.bool)

def bool_hash(obj):
    return IntObj(hash(obj.bool))

def bool_bind_methods():
    bool_cls.methods['tostr(_)'] = bool_to_str
    bool_cls.methods['==(_,_)'] = bool_equ
    bool_cls.methods['hash(_)'] = bool_hash

############################ str methods #######################

def str_to_str(obj):
    return obj

def str_equ(obj1, obj2):
    return BoolObj(obj1.str == obj2.str)

def str_hash(obj):
    return IntObj(hash(obj.str))

def str_add(obj1, obj2):
    if obj2.obj_header.obj_type != 'str':
        fatal_print('Run error, arg2 must be string')
        sys.exit(1)
    return StrObj(obj1.str + obj2.str)

def str_at(obj1, obj2):
    if obj2.obj_header.obj_type != 'int':
        fatal_print('Run error, index must be int')
        sys.exit(1)
    return StrObj(obj1.str[obj2.int])

def str_len(obj):
    return IntObj(len(obj.str))

def str_emtpy(obj):
    return BoolObj(len(obj.str) == 0)

def str_bind_methods():
    str_cls.methods['tostr(_)'] = str_to_str
    str_cls.methods['==(_,_)'] = str_equ
    str_cls.methods['hash(_)'] = str_hash
    str_cls.methods['+(_,_)'] = str_add
    str_cls.methods['at(_,_)'] = str_at
    str_cls.methods['len(_)'] = str_len
    str_cls.methods['empty(_)'] = str_emtpy


# 数字类型在运行时进行了类型检验
############################## int methods ####################

def int_to_str(obj):
    return StrObj(str(obj.int))

def int_equ(obj1, obj2):
    return BoolObj(obj1.int == obj2.int)

def int_hash(obj):
    return IntObj(hash(obj.int))

def int_to_float(obj):
    return FloatObj(float(obj.int))

def int_add(obj1, obj2):
    if obj2.obj_header.obj_type == 'float':
        obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == 'float':
        return FloatObj(obj1.float + obj2.float)

    if obj1.obj_header.obj_type == 'int':
        return IntObj(obj1.int + obj2.int)

def int_sub(obj1, obj2):
    if obj2.obj_header.obj_type == 'float':
        obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == 'float':
        return FloatObj(obj1.float - obj2.float)

    if obj1.obj_header.obj_type == 'int':
        return IntObj(obj1.int - obj2.int)

def int_mul(obj1, obj2):
    if obj2.obj_header.obj_type == 'float':
        obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == 'float':
        return FloatObj(obj1.float * obj2.float)

    if obj1.obj_header.obj_type == 'int':
        return IntObj(obj1.int * obj2.int)

def int_div(obj1, obj2):
    if obj2.obj_header.obj_type == 'float':
        obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == 'float':
        if obj2.float == 0.0:
            fatal_print('Run error, arg2 cannot be 0')
            sys.exit(1)
        return FloatObj(obj1.float / obj2.float)

    if obj1.obj_header.obj_type == 'int':
        if obj2.int == 0:
            fatal_print('Run error, arg2 cannot be 0')
            sys.exit(1)
        return IntObj(obj1.int / obj2.int)

def int_mod(obj1, obj2):
    if obj2.obj_header.obj_type != 'int':
        fatal_print('Run error, arg2 must be int')
        sys.exit(1)
    
    if obj2.int == 0:
        fatal_print('Run error, arg2 cannot be 0')
        sys.exit(1)
    return IntObj(obj1.int % obj2.int)

def int_gt(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    obj1 = int_to_float(obj1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    return BoolObj(obj1.float > obj2.float)

def int_ge(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, args is not a number')
        sys.exit(1)
    obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    return BoolObj(obj1.float >= obj2.float)

def int_lt(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, args is not a number')
        sys.exit(1)
    obj1 = int_to_float(obj1)

    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    return BoolObj(obj1.float < obj2.float)

def int_le(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    obj1 = int_to_float(obj1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    return BoolObj(obj1.float <= obj2.float)


def int_bind_methods():
    int_cls.methods['tostr(_)'] = int_to_str
    int_cls.methods['==(_,_)'] = int_equ
    int_cls.methods['hash(_)'] = int_hash
    int_cls.methods['tofloat(_)'] = int_to_float
    int_cls.methods['+(_,_)'] = int_add
    int_cls.methods['-(_,_)'] = int_sub
    int_cls.methods['*(_,_)'] = int_mul
    int_cls.methods['/(_,_)'] = int_div
    int_cls.methods['%(_,_)'] = int_mod
    int_cls.methods['>(_,_)'] = int_gt
    int_cls.methods['>=(_,_)'] = int_ge
    int_cls.methods['<(_,_)'] = int_lt
    int_cls.methods['<=(_,_)'] = int_le
    

############################# float methods #######################

def float_to_str(obj):
    return StrObj(str(obj.float))

def float_equ(obj1, obj2):
    return BoolObj(obj1.float == obj2.float)

def float_hash(obj):
    return IntObj(hash(obj.float))

def float_to_int(obj1):
    return IntObj(int(obj1.float))

def float_add(obj1, obj2):
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    
    return FloatObj(obj1.float + obj2.float)

def float_sub(obj1, obj2):
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    return FloatObj(obj1.float - obj2.float)

def float_mul(obj1, obj2):
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    return FloatObj(obj1.float * obj2.float)

def float_div(obj1, obj2):
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    if obj2.float == 0:
        fatal_print('Run error, arg2 cannot be 0')
    return FloatObj(obj1.float / obj2.float)

def float_gt(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2) 
    return BoolObj(obj1.float > obj2.float)

def float_ge(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2) 
    return BoolObj(obj1.float >= obj2.float)

def float_lt(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2) 
    return BoolObj(obj1.float < obj2.float)

def float_le(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        fatal_print('Run error, arg2 is not a number')
        sys.exit(1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2) 
    return BoolObj(obj1.float <= obj2.float)

def float_bind_methods():
    float_cls.methods['tostr(_)'] = float_to_str
    float_cls.methods['==(_,_)'] = float_equ
    float_cls.methods['hash(_)'] = float_hash
    float_cls.methods['toint(_)'] = float_to_int
    float_cls.methods['+(_,_)'] = float_add
    float_cls.methods['-(_,_)'] = float_sub
    float_cls.methods['*(_,_)'] = float_mul
    float_cls.methods['/(_,_)'] = float_div
    float_cls.methods['>(_,_)'] = float_gt
    float_cls.methods['>=(_,_)'] = float_ge
    float_cls.methods['<(_,_)'] = float_lt
    float_cls.methods['<=(_,_)'] = float_le

################################ list methods ########################

def list_len(obj):
    return IntObj(len(obj.list))

def list_to_str(obj):
    s = '['
    for item in obj.list:
        s += type_to_pystr(item) + ','
    s = s[:-1] + ']'
    return StrObj(s)

def list_at(obj1, obj2):
    if obj2.obj_header.obj_type != 'int':
        fatal_print('Run error, arg2 must be int')
        sys.exit(1)
    return obj1.list[obj2.int]

def list_insert(obj1, obj2, obj3):
    """obj2: 下标
    """
    if obj2.obj_header.obj_type != 'int':
        fatal_print('Run error, index must be int')
        sys.exit(1)
    obj1.list.insert(obj2.int, obj3)
    
def list_append(obj1, obj2):
    obj1.list.append(obj2)

def list_remove(obj1, obj2):
    """obj2: 下标
    """
    if obj2.obj_header.obj_type != 'int':
        fatal_print('Run error, index must be int')
        sys.exit(1)
    length = list_len(obj1) 
    if obj2.int >= length or obj2.int < 0:
        fatal_print('Run error, index out of rang')
        sys.exit(1)
    del obj1.list[obj2.int]


def list_bind_methods():
    list_cls.methods['len(_)'] = list_len
    list_cls.methods['tostr(_)'] = list_to_str
    list_cls.methods['insert(_,_,_)'] = list_insert
    list_cls.methods['at(_,_)'] = list_at
    list_cls.methods['remove(_,_)'] = list_remove
    list_cls.methods['append(_,_)'] = list_append


def map_put(obj, key, val):
    if key.obj_header.obj_type in ['map', 'list']:
        fatal_print('Run error, map or list cannot be hashed')
        sys.exit(1)
    obj.map[key] = val

def map_get(obj, key):
    if key.obj_header.obj_type == 'nil':
        fatal_print('Run error, key cannot be nil')
        sys.exit(1)
    if key.obj_header.obj_type in ['map', 'list']:
        fatal_print('Run error, map or list cannot be hashed')
        sys.exit(1)
    if key not in obj.map:
        return NilObj()
    return obj.map[key]

def map_remove(obj, key):
    if key.obj_header.obj_type == 'nil':
        fatal_print('Run error, key cannot be nil')
        sys.exit(1)
    if key.obj_header.obj_type in ['map', 'list']:
        fatal_print('Run error, map or list cannot be hashed')
        sys.exit(1)
    if key in obj.map:
        del obj.map[key]

def map_to_str(obj):
    s = '{'
    for key in obj.map:
        s += type_to_pystr(key) + ':' + type_to_pystr(obj.map[key]) + ','
    return StrObj(s[:-1] + '}')


def map_bind_methods():
    map_cls.methods['tostr(_)'] = map_to_str
    map_cls.methods['@put(_,_,_)'] = map_put
    map_cls.methods['@get(_,_)'] = map_get
    map_cls.methods['@remove(_,_)'] = map_remove


class FunObj(object):
    """
    函数对象与模块对象共用一个FunObj对象表示, 因为他们都是可以执行代码的最小单元
    """

    def __init__(self):
        self.obj_header = ObjHeader('fun', fun_cls, self)
        self.stream = []
        self.cur_idx = 0
        
        # 为函数时使用
        self.arg_num = 0
        self.local_vars = []
        self.local_var_num = 0
        
        # 为模块时使用
        self.constants = []
        self.constant_num = 0


class NilObj(object):

    def __init__(self):
        self.obj_header = ObjHeader('nil', nil_cls, self)
        self.nil = None
    
    def __hash__(self):
        return hash(self.nil)

    def __eq__(self, other):
        return hash(self.nil) == hash(other.nil)

class BoolObj(object):

    def __init__(self, boolean):
        self.obj_header = ObjHeader('bool', bool_cls, self)
        self.bool = boolean
    
    def __hash__(self):
        return hash(self.bool)

    def __eq__(self, other):
        return hash(self.bool) == hash(other.bool)


class StrObj(object):
    
    def __init__(self, string):
        self.obj_header = ObjHeader('str', str_cls, self) 
        self.str = str(string)
    
    def __hash__(self):
        return hash(self.str)

    def __eq__(self, other):
        return hash(self.str) == hash(other.str)


class IntObj(object):

    def __init__(self, integer):
        self.obj_header = ObjHeader('int', int_cls, self)
        self.int = int(integer)
    
    def __hash__(self):
        return hash(self.int)

    def __eq__(self, other):
        return hash(self.int) == hash(other.int)

class FloatObj(object):

    def __init__(self, float_):
        self.obj_header = ObjHeader('float', float_cls, self)
        self.float = float(float_)
    
    def __hash__(self):
        return hash(self.float)

    def __eq__(self, other):
        return hash(self.float) == hash(other.float)

class ListObj(object):

    def __init__(self, list_):
        self.obj_header = ObjHeader('list', list_cls, self)
        self.list = list(list_)

class MapObj(object):

    def __init__(self, map_):
        self.obj_header = ObjHeader('map', map_cls, self)
        self.map = dict(map_)

    
def bind_methods():
    nil_bind_methods()
    bool_bind_methods()
    str_bind_methods()
    int_bind_methods()
    float_bind_methods()
    list_bind_methods()
    map_bind_methods()

bind_methods()


def main(argv=None):
    pass

if __name__ == '__main__':
    main()
