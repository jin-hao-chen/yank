#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import time
import copy
from ytypes import *
from color_print import fatal_print


class NilObj(object):


    def __init__(self):
        self.obj_header = ObjHeader(OT_NIL, nil_cls, self)
        self.nil = None
    
    def __hash__(self):
        return hash(self.nil)

    def __eq__(self, other):
        return hash(self.nil) == hash(other.nil)


class BoolObj(object):


    def __init__(self, boolean):
        self.obj_header = ObjHeader(OT_BOOL, bool_cls, self)
        self.bool = boolean
    
    def __hash__(self):
        return hash(self.bool)

    def __eq__(self, other):
        return hash(self.bool) == hash(other.bool)


class StrObj(object):
    

    def __init__(self, string):
        self.obj_header = ObjHeader(OT_STR, str_cls, self) 
        self.str = str(string)
    
    def __hash__(self):
        return hash(self.str)

    def __eq__(self, other):
        return hash(self.str) == hash(other.str)


class IntObj(object):


    def __init__(self, integer):
        self.obj_header = ObjHeader(OT_INT, int_cls, self)
        self.int = int(integer)
    
    def __hash__(self):
        return hash(self.int)

    def __eq__(self, other):
        return hash(self.int) == hash(other.int)


class FloatObj(object):


    def __init__(self, float_):
        self.obj_header = ObjHeader(OT_FLOAT, float_cls, self)
        self.float = float(float_)
    
    def __hash__(self):
        return hash(self.float)

    def __eq__(self, other):
        return hash(self.float) == hash(other.float)


class ListObj(object):


    def __init__(self, list_=[]):
        self.obj_header = ObjHeader(OT_LIST, list_cls, self)
        if not list_:
            list_ = []
        self.list = list(list_)


class MapObj(object):


    def __init__(self, map_=None):
        self.obj_header = ObjHeader(OT_MAP, map_cls, self)
        if not map_:
            map_ = {}
        self.map = dict(map_)


class ModuleObj(object):


    def __init__(self, name):
        self.obj_header = ObjHeader(OT_MODULE, module_cls, self)
        self.name = name
        self.module_var_names = []
        self.module_var_values = []


class FunObj(object):


    def __init__(self, name, scope=1, arg_num=0):
        self.obj_header = ObjHeader(OT_FUN, fun_cls, self)
        self.name = name
        self.stream = []
        self.stream_num = 0
        
        # 存放的是Python级别的字符串, 包括数字和字符串的字面量
        self.constants = []
        self.constant_num = 0
        self.max_used_slots = 0
        self.cur_idx = 0
        
        self.scope = scope
        self.arg_num = arg_num
    
    def add_constant(self, value):
        self.constants.append(value)
        self.constant_num += 1
        return self.constant_num - 1
    

def call(obj, method_name):
    return obj.obj_header.cls_obj.methods[method_name]

def call_by_value(value, method_name):
    return call(value.obj(), method_name)

def exit_if_false(cond):
    if not cond:
        sys.exit(1)
    return True

def _type_to_pystr(obj):
    if obj.obj_header.obj_type == OT_INT:
        return _int_to_str(obj).str
    elif obj.obj_header.obj_type == OT_FLOAT:
        return _float_to_str(obj).str
    elif obj.obj_header.obj_type == OT_STR:
        return _str_to_str(obj).str
    elif obj.obj_header.obj_type == OT_LIST:
        return _list_to_str(obj).str
    elif obj.obj_header.obj_type == OT_MAP:
        return _map_to_str(obj).str
    elif obj.obj_header.obj_type == OT_NIL:
        return _nil_to_str(obj).str
    elif obj.obj_header.obj_type == OT_BOOL:
        return _bool_to_str(obj).str
    elif obj.obj_header.obj_type == OT_FUN:
        return _fun_to_str(obj).str
    elif obj.obj_header.obj_type == OT_MODULE:
        return _module_to_str(obj).str

def type_to_pystr(start, args):
    obj = args[start].obj()
    if obj.obj_header.obj_type == OT_INT:
        return int_to_str(start, args).str
    elif obj.obj_header.obj_type == OT_FLOAT:
        return float_to_str(start, args).str
    elif obj.obj_header.obj_type == OT_STR:
        return str_to_str(start, args).str
    elif obj.obj_header.obj_type == OT_LIST:
        return list_to_str(start, args).str
    elif obj.obj_header.obj_type == OT_MAP:
        return map_to_str(start, args).str
    elif obj.obj_header.obj_type == OT_NIL:
        return nil_to_str(start, args).str
    elif obj.obj_header.obj_type == OT_BOOL:
        return bool_to_str(start, args).str
    elif obj.obj_header.obj_type == OT_FUN:
        return fun_to_str(start, args).str
    elif obj.obj_header.obj_type == OT_MODULE:
        return module_to_str(start, args).str

def is_type(obj, obj_type):
    return obj.obj_header.obj_type == obj_type

def args_num(pystr):
    left = pystr.find('(')
    right = pystr.rfind(')')
    args_str = pystr[left + 1: right]
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


module_cls = ClsObj('module_cls')
fun_cls = ClsObj('fun_cls')
nil_cls = ClsObj('nil_cls')
bool_cls = ClsObj('bool_cls')
str_cls = ClsObj('str_cls')
int_cls = ClsObj('int_cls')
float_cls = ClsObj('float_cls')
list_cls = ClsObj('list_cls')

# map对象比较特别, 在yank中就是对象, map的remove, put, get在内部的方式是@remove, @put, @get, 因为yank中通过map实现对象的, 模仿一下js
map_cls = ClsObj('map_cls')


def return_true(start, args, obj):
    args[start].to_value(obj)
    return True

def return_false():
    return False

# 参数被封装成了yank_list
def fun_call(obj, args):
    pass


def nil_to_str(start, args):
    obj = args[start].obj()
    return return_true(start, args, StrObj(str(obj.nil)))


def nil_equ(start, args):
    obj1 = args[start].obj() 
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type != OT_NIL:
        return return_true(start, args, BoolObj(False))
    return return_true(start, args, BoolObj(True)) 

def nil_hash(start, args):
    fatal_print('Runtime error, nil cannot be hashed!')
    return return_false()

def nil_bind_methods():
    nil_cls.methods['tostr()'] = nil_to_str
    nil_cls.methods['==(_)'] = nil_equ
    nil_cls.methods['hash(_)'] = nil_hash

    nil_cls.methods['_tostr()'] = _nil_to_str
    nil_cls.methods['_==(_)'] = _nil_equ
    nil_cls.methods['_hash()'] = _nil_hash

def bool_to_str(start, args):
    obj = args[start].obj()
    return return_true(start, args, StrObj(str(obj.bool)))

def bool_equ(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    return return_true(start, args, BoolObj(obj1.bool == obj2.bool))

def bool_hash(start, args):
    obj = args[start].obj()
    return return_true(start, args, IntObj(hash(obj.bool)))

def bool_bind_methods():
    bool_cls.methods['tostr()'] = bool_to_str
    bool_cls.methods['==(_)'] = bool_equ
    bool_cls.methods['hash()'] = bool_hash

    bool_cls.methods['_tostr()'] = _bool_to_str
    bool_cls.methods['_==(_)'] = _bool_equ
    bool_cls.methods['_hash()'] = _bool_hash

def str_to_str(start, args):
    obj = args[start].obj()
    return return_true(start, args, StrObj(str(obj.str)))

def str_equ(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    return return_true(start, args, BoolObj(obj1.str == obj2.str))

def str_hash(start, args):
    obj = args[start].obj()
    return return_true(start, args, IntObj(hash(obj.str)))

def str_add(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type != OT_STR:
        fatal_print('Runtime error, arg2 must be string')
        return return_false()
    return return_true(start, args, StrObj(obj1.str + obj2.str))

def str_numbers(start, args):
    obj = args[start].obj()
    if obj.str.isdigit():
        ret = IntObj(int(obj.str))
    else:
        try:
            ret = FloatObj(float(obj.str))
        except:
            fatal_print('Runtime error, cannot convert %s to numbers' % obj.str)
            return return_false()
    return return_true(start, args, ret)

def str_at(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type != OT_STR:
        fatal_print('Runtime error, index must be int')
        return return_false()
    return return_true(start, args, StrObj(obj1.str[obj2.int]))

def str_len(start, args):
    obj = args[start].obj()
    return return_true(start, args, IntObj(len(obj.str)))

def str_emtpy(start, args):
    obj = args[start].obj()
    return return_true(start, args, BoolObj(len(obj.str) == 0))

def _str_numbers(obj):
    if obj.str.isdigit():
        ret = IntObj(int(obj.str))
    else:
        try:
            ret = FloatObj(float(obj.str))
        except:
            fatal_print('Runtime error, cannot convert %s to numbers' % obj.str)
            sys.exit(1)
    return ret

def str_bind_methods():
    str_cls.methods['tostr()'] = str_to_str
    str_cls.methods['==(_)'] = str_equ
    str_cls.methods['hash()'] = str_hash
    str_cls.methods['+(_)'] = str_add
    str_cls.methods['at(_)'] = str_at
    str_cls.methods['len()'] = str_len
    str_cls.methods['empty()'] = str_emtpy
    str_cls.methods['numbers()'] = str_numbers

    str_cls.methods['_tostr()'] = _str_to_str
    str_cls.methods['_==(_)'] = _str_equ
    str_cls.methods['_hash()'] = _str_hash
    str_cls.methods['_+(_)'] = _str_add
    str_cls.methods['_at(_)'] = _str_at
    str_cls.methods['_len()'] = _str_len
    str_cls.methods['_empty()'] = _str_emtpy
    str_cls.methods['_numbers()'] = _str_numbers

def int_to_str(start, args):
    obj = args[start].obj()
    return return_true(start, args, StrObj(str(obj.int)))

def int_equ(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    return return_true(start, args, BoolObj(obj1.int == obj2.int))

def int_hash(start, args):
    obj = args[start].obj()
    return return_true(start, args, IntObj(hash(obj.int)))

def int_to_float(start, args):
    obj = args[start].obj()
    return return_true(start, args, FloatObj(float(obj.int)))

def int_add(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type == OT_FLOAT:
        obj1 = _int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    
    if obj1.obj_header.obj_type == OT_FLOAT:
        return return_true(start, args, FloatObj(obj1.float + obj2.float))

    if obj1.obj_header.obj_type == OT_INT:
        return return_true(start, args, IntObj(obj1.int + obj2.int))

def int_sub(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type == OT_FLOAT:
        obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    
    if obj1.obj_header.obj_type == OT_FLOAT:
        return return_true(start, args, FloatObj(obj1.float - obj2.float))

    if obj1.obj_header.obj_type == OT_INT:
        return return_true(start, args, IntObj(obj1.int - obj2.int))

def int_mul(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type == OT_FLOAT:
        obj1 = _int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    
    if obj1.obj_header.obj_type == OT_FLOAT:
        return return_true(start, args, FloatObj(obj1.float * obj2.float))

    if obj1.obj_header.obj_type == OT_INT:
        return return_true(start, args, IntObj(obj1.int * obj2.int))

def int_div(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type == OT_FLOAT:
        obj1 = _int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    
    if obj1.obj_header.obj_type == OT_FLOAT:
        if obj2.float == 0.0:
            fatal_print('Runtime error, arg2 cannot be 0')
            return return_false()
        return return_true(FloatObj(obj1.float / obj2.float))

    if obj1.obj_header.obj_type == OT_INT:
        if obj2.int == 0:
            fatal_print('Runtime error, arg2 cannot be 0')
            return return_false()
        return return_true(start, args, IntObj(obj1.int / obj2.int))

def int_mod(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type != OT_INT:
        fatal_print('Runtime error, arg2 must be int')
        return return_false()
    
    if obj2.int == 0:
        fatal_print('Runtime error, arg2 cannot be 0')
        return return_false()
    return return_true(start, args, IntObj(obj1.int % obj2.int))

def int_gt(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    obj1 = _int_to_float(obj1)
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    return return_true(start, args, BoolObj(obj1.float > obj2.float))


def int_ge(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, args is not a number')
        return return_false()
    obj1 = _int_to_float(obj1)
    
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    return return_true(start, args, BoolObj(obj1.float >= obj2.float))


def int_lt(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, args is not a number')
        return return_false()
    obj1 = _int_to_float(obj1)

    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    return return_true(start, args, BoolObj(obj1.float < obj2.float))


def int_le(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, obj2 is not a number')
        return return_false()
    obj1 = _int_to_float(obj1)
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    return return_true(start, args, BoolObj(obj1.float <= obj2.float))


def int_bind_methods():
    int_cls.methods['tostr()'] = int_to_str
    int_cls.methods['==(_)'] = int_equ
    int_cls.methods['hash()'] = int_hash
    int_cls.methods['float()'] = int_to_float
    int_cls.methods['+(_)'] = int_add
    int_cls.methods['-(_)'] = int_sub
    int_cls.methods['*(_)'] = int_mul
    int_cls.methods['/(_)'] = int_div
    int_cls.methods['%(_)'] = int_mod
    int_cls.methods['>(_)'] = int_gt
    int_cls.methods['>=(_)'] = int_ge
    int_cls.methods['<(_)'] = int_lt
    int_cls.methods['<=(_,_)'] = int_le
    
    int_cls.methods['_tostr(_)'] = _int_to_str
    int_cls.methods['_==(_,_)'] = _int_equ
    int_cls.methods['_hash(_)'] = _int_hash
    int_cls.methods['_float(_)'] = _int_to_float
    int_cls.methods['_+(_,_)'] = _int_add
    int_cls.methods['_-(_,_)'] = _int_sub
    int_cls.methods['_*(_,_)'] = _int_mul
    int_cls.methods['_/(_,_)'] = _int_div
    int_cls.methods['_%(_,_)'] = _int_mod
    int_cls.methods['_>(_,_)'] = _int_gt
    int_cls.methods['_>=(_,_)'] = _int_ge
    int_cls.methods['_<(_,_)'] = _int_lt
    int_cls.methods['_<=(_,_)'] = _int_le

def float_to_str(start, args):
    obj = args[start].obj()
    return return_true(start, args, StrObj(str(obj.float)))


def float_equ(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    return return_true(start, args, BoolObj(obj1.float == obj2.float))


def float_hash(start, args):
    obj = args[start].obj()
    return return_true(start, args, IntObj(hash(obj.float)))


def float_to_int(start, args):
    obj = args[start].obj()
    return return_true(start, args, IntObj(int(obj.float)))

def float_add(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    return return_true(start, args, FloatObj(obj1.float + obj2.float))


def float_sub(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    return return_true(start, args, FloatObj(obj1.float - obj2.float))


def float_mul(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in [OT_INT, OT_FLOAT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    return return_true(start, args, FloatObj(obj1.float * obj2.float))


def float_div(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    if obj2.float == 0:
        fatal_print('Runtime error, arg2 cannot be 0')
        return return_false()
    return return_true(start, args, FloatObj(obj1.float / obj2.float))


def float_gt(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2) 
    return return_true(start, args, BoolObj(obj1.float > obj2.float))


def float_ge(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2) 

    return return_true(start, args, BoolObj(obj1.float >= obj2.float))


def float_lt(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2) 
    return return_true(start, args, BoolObj(obj1.float < obj2.float))


def float_le(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        return return_false()
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2) 
    return return_true(start, args, BoolObj(obj1.float <= obj2.float))


def float_bind_methods():
    float_cls.methods['tostr()'] = float_to_str
    float_cls.methods['==(_)'] = float_equ
    float_cls.methods['hash()'] = float_hash
    float_cls.methods['int()'] = float_to_int
    float_cls.methods['+(_)'] = float_add
    float_cls.methods['-(_)'] = float_sub
    float_cls.methods['*(_)'] = float_mul
    float_cls.methods['/(_)'] = float_div
    float_cls.methods['>(_)'] = float_gt
    float_cls.methods['>=(_)'] = float_ge
    float_cls.methods['<(_)'] = float_lt
    float_cls.methods['<=(_)'] = float_le

    float_cls.methods['_tostr(_)'] = _float_to_str
    float_cls.methods['_==(_,_)'] = _float_equ
    float_cls.methods['_hash(_)'] = _float_hash
    float_cls.methods['_int(_)'] = _float_to_int
    float_cls.methods['_+(_,_)'] = _float_add
    float_cls.methods['_-(_,_)'] = _float_sub
    float_cls.methods['_*(_,_)'] = _float_mul
    float_cls.methods['_/(_,_)'] = _float_div
    float_cls.methods['_>(_,_)'] = _float_gt
    float_cls.methods['_>=(_,_)'] = _float_ge
    float_cls.methods['_<(_,_)'] = _float_lt
    float_cls.methods['_<=(_,_)'] = _float_le


def list_len(start, args):
    obj = args[start].obj()
    return return_true(start, args, IntObj(len(obj.list)))

def list_to_str(start, args):
    obj = args[start].obj()
    s = '['
    for item in obj.list:
        s += _type_to_pystr(item.obj()) + ', '
    s = s[:-2] + ']'
    return return_true(start, args, StrObj(s))


def list_at(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    if obj2.obj_header.obj_type != OT_INT:
        fatal_print('Runtime error, arg2 must be int')
        return return_false()
    ret = copy.copy(obj1.list[obj2.int])
    args[start].value_type = ret.value_type
    args[start].obj_header = ret.obj_header
    return True


def list_insert(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    obj3 = args[start + 2].obj()
    # obj2为下标
    if obj2.obj_header.obj_type != OT_INT:
        fatal_print('Runtime error, index must be int')
        return return_false()
    obj1.list.insert(obj2.int, copy.copy(args[start + 2]))
    return return_true(start, args, NilObj())
    

def list_append(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    obj1.list.append(copy.copy(args[start + 1]))
    return return_true(start, args, NilObj())


def list_remove(start, args):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    # obj2为下标
    if obj2.obj_header.obj_type != OT_INT:
        fatal_print('Runtime error, index must be int')
        return return_false()
    length = list_len(obj1) 
    if obj2.int >= length or obj2.int < 0:
        fatal_print('Runtime error, index out of rang')
        return return_false()
    del obj1.list[obj2.int]
    return return_true(start, args, NilObj())


def list_bind_methods():
    list_cls.methods['len()'] = list_len
    list_cls.methods['tostr()'] = list_to_str
    list_cls.methods['insert(_,_)'] = list_insert
    list_cls.methods['at(_)'] = list_at
    list_cls.methods['remove(_)'] = list_remove
    list_cls.methods['append(_)'] = list_append
    list_cls.methods['_len(_)'] = _list_len
    list_cls.methods['_tostr(_)'] = _list_to_str
    list_cls.methods['_insert(_,_,_)'] = _list_insert
    list_cls.methods['_at(_,_)'] = _list_at
    list_cls.methods['_remove(_,_)'] = _list_remove
    list_cls.methods['_append(_,_)'] = _list_append


def map_put(start, args):
    obj = args[start].obj()
    key = args[start + 1].obj()
    val = args[start + 2].obj()
    if key.obj_header.obj_type in [OT_MAP, OT_LIST]:
        fatal_print('Runtime error, map or list cannot be hashed')
        return return_false()
    obj.map[copy.copy(args[start + 1])] = copy.copy(args[start + 2])
    return return_true(start, args, NilObj())


def map_get(start, args):
    obj = args[start].obj()
    key = args[start + 1].obj()
    if key.obj_header.obj_type == OT_NIL:
        fatal_print('Runtime error, key cannot be nil')
        return return_false()
    if key.obj_header.obj_type in [OT_MAP, OT_LIST]:
        fatal_print('Runtime error, map or list cannot be hashed')
        return return_false()
    if args[start + 1] not in obj.map:
        return return_true(start, args, NilObj())
    ret = copy.copy(obj.map[args[start + 1]])
    args[start].value_type = ret.value_type
    args[start].obj_header = ret.obj_header
    return True


def map_remove(start, args):
    obj = args[start].obj()
    key = args[start + 1].obj()
    if key.obj_header.obj_type == OT_NIL:
        fatal_print('Runtime error, key cannot be nil')
        return return_false()
    if key.obj_header.obj_type in [OT_MAP, OT_LIST]:
        fatal_print('Runtime error, map or list cannot be hashed')
        return return_false()
    if args[start + 1] in obj.map:
        del obj.map[args[start + 1]]
    return return_true(start, args, NilObj())

def map_to_str(start, args):
    obj = args[start].obj()
    s = '{'
    for key in obj.map:
        s += _type_to_pystr(key.obj()) + ': ' + _type_to_pystr(obj.map[key].obj()) + ', '
    return return_true(start, args, StrObj(s[:-2] + '}'))    


def map_bind_methods():
    map_cls.methods['tostr()'] = map_to_str
    map_cls.methods['put(_,_)'] = map_put
    map_cls.methods['get(_)'] = map_get
    map_cls.methods['remove(_)'] = map_remove
    map_cls.methods['@put(_,_)'] = map_put
    map_cls.methods['@get(_)'] = map_get
    map_cls.methods['@remove(_)'] = map_remove
    map_cls.methods['@_tostr(_)'] = _map_to_str
    map_cls.methods['@_put(_,_,_)'] = _map_put
    map_cls.methods['@_get(_,_)'] = _map_get
    map_cls.methods['@_remove(_,_)'] = _map_remove


def module_to_str(start, args):
    obj = args[start].obj()
    addr = str(id(obj))
    return return_true(start, args, StrObj('<Module(addr: %s) %s>' % (addr, obj.name)))


def module_bind_methods():
    module_cls.methods['tostr(_)'] = module_to_str
    module_cls.methods['_tostr(_)'] = _module_to_str


def fun_to_str(start, args):
    obj = args[start].obj()
    addr = str(id(obj))
    return return_true(start, args, StrObj('<Function(addr: %s) %s>' % (addr, obj.name)))


def fun_bind_methods():
    fun_cls.methods['tostr(_)'] = fun_to_str
    fun_cls.methods['_tostr(_)'] = _fun_to_str


def _bind_methods():
    module_bind_methods()
    fun_bind_methods()
    nil_bind_methods()
    bool_bind_methods()
    str_bind_methods()
    int_bind_methods()
    float_bind_methods()
    list_bind_methods()
    map_bind_methods()

# 内部使用
def _nil_to_str(obj):
    return StrObj(str(obj.nil))


def _nil_equ(obj1, obj2):
    if obj2.obj_header.obj_type != OT_NIL:
        return BoolObj(False)
    return BoolObj(True)

def _nil_hash(obj):
    fatal_print('RuntimetimeError, nil cannot be hashed!')
    sys.exit(1)

def _bool_to_str(obj):
    return StrObj(str(obj.bool))


def _bool_equ(obj1, obj2):
    return BoolObj(obj1.bool == obj2.bool)


def _bool_hash(obj):
    return IntObj(hash(obj.bool))


def _str_to_str(obj):
    return obj


def _str_equ(obj1, obj2):
    return BoolObj(obj1.str == obj2.str)


def _str_hash(obj):
    return IntObj(hash(obj.str))


def _str_add(obj1, obj2):
    if obj2.obj_header.obj_type != OT_STR:
        fatal_print('Runtime error, arg2 must be string')
        sys.exit(1)
    return StrObj(obj1.str + obj2.str)


def _str_at(obj1, obj2):
    if obj2.obj_header.obj_type != OT_STR:
        fatal_print('Runtime error, index must be int')
        sys.exit(1)
    return StrObj(obj1.str[obj2.int])


def _str_len(obj):
    return IntObj(len(obj.str))


def _str_emtpy(obj):
    return BoolObj(len(obj.str) == 0)


def _int_to_str(obj):
    return StrObj(str(obj.int))


def _int_equ(obj1, obj2):
    obj1 = args[start].obj()
    obj2 = args[start + 1].obj()
    return BoolObj(obj1.int == obj2.int)


def _int_hash(obj):
    return IntObj(hash(obj.int))


def _int_to_float(obj):
    return FloatObj(float(obj.int))


def _int_add(obj1, obj2):
    if obj2.obj_header.obj_type == OT_FLOAT:
        obj1 = _int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == OT_FLOAT:
        return FloatObj(obj1.float + obj2.float)

    if obj1.obj_header.obj_type == OT_INT:
        return IntObj(obj1.int + obj2.int)


def _int_sub(obj1, obj2):
    if obj2.obj_header.obj_type == OT_FLOAT:
        obj1 = _int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == OT_FLOAT:
        return FloatObj(obj1.float - obj2.float)

    if obj1.obj_header.obj_type == OT_INT:
        return IntObj(obj1.int - obj2.int)


def _int_mul(obj1, obj2):
    if obj2.obj_header.obj_type == OT_FLOAT:
        obj1 = _int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == OT_FLOAT:
        return FloatObj(obj1.float * obj2.float)

    if obj1.obj_header.obj_type == OT_INT:
        return IntObj(obj1.int * obj2.int)


def _int_div(obj1, obj2):
    if obj2.obj_header.obj_type == OT_FLOAT:
        obj1 = _int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == OT_FLOAT:
        if obj2.float == 0.0:
            fatal_print('Runtime error, arg2 cannot be 0')
            sys.exit(1)
        return FloatObj(obj1.float / obj2.float)

    if obj1.obj_header.obj_type == OT_INT:
        if obj2.int == 0:
            fatal_print('Runtime error, arg2 cannot be 0')
            sys.exit(1)
        return IntObj(obj1.int / obj2.int)


def _int_mod(obj1, obj2):
    if obj2.obj_header.obj_type != OT_INT:
        fatal_print('Runtime error, arg2 must be int')
        sys.exit(1)
    
    if obj2.int == 0:
        fatal_print('Runtime error, arg2 cannot be 0')
        sys.exit(1)
    return IntObj(obj1.int % obj2.int)


def _int_gt(obj1, obj2):
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    obj1 = _int_to_float(obj1)
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    return BoolObj(obj1.float > obj2.float)


def _int_ge(obj1, obj2):
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, args is not a number')
        sys.exit(1)
    obj1 = _int_to_float(obj1)
    
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    return BoolObj(obj1.float >= obj2.float)


def _int_lt(obj1, obj2):
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, args is not a number')
        sys.exit(1)
    obj1 = _int_to_float(obj1)

    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    return BoolObj(obj1.float < obj2.float)


def _int_le(obj1, obj2):
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, obj2 is not a number')
        sys.exit(1)
    obj1 = _int_to_float(obj1)
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    return BoolObj(obj1.float <= obj2.float)


def _float_to_str(obj):
    return StrObj(str(obj.float))


def _float_equ(obj1, obj2):
    return BoolObj(obj1.float == obj2.float)


def _float_hash(obj):
    return IntObj(hash(obj.float))


def _float_to_int(obj):
    return IntObj(int(obj.float))


def _float_add(obj1, obj2):
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    
    return FloatObj(obj1.float + obj2.float)


def _float_sub(obj1, obj2):
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    return FloatObj(obj1.float - obj2.float)


def _float_mul(obj1, obj2):
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in [OT_INT, OT_FLOAT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    return FloatObj(obj1.float * obj2.float)


def _float_div(obj1, obj2):
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    if obj2.float == 0:
        fatal_print('Runtime error, arg2 cannot be 0')
    return FloatObj(obj1.float / obj2.float)


def _float_gt(obj1, obj2):
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2) 
    return BoolObj(obj1.float > obj2.float)


def _float_ge(obj1, obj2):
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2) 
    return BoolObj(obj1.float >= obj2.float)


def _float_lt(obj1, obj2):
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2) 
    return BoolObj(obj1.float < obj2.float)


def _float_le(obj1, obj2):
    if obj2.obj_header.obj_type not in [OT_FLOAT, OT_INT]:
        fatal_print('Runtime error, arg2 is not a number')
        sys.exit(1)
    if obj2.obj_header.obj_type == OT_INT:
        obj2 = _int_to_float(obj2) 
    return BoolObj(obj1.float <= obj2.float)


def _list_len(obj):
    return IntObj(len(obj.list))


def _list_to_str(obj):
    s = '['
    for item in obj.list:
        s += _type_to_pystr(item.obj()) + ', '
    s = s[:-2] + ']'
    return StrObj(s)


def _list_at(obj1, obj2):
    if obj2.obj_header.obj_type != OT_INT:
        fatal_print('Runtime error, arg2 must be int')
        sys.exit(1)
    return obj1.list[obj2.int]


def _list_insert(obj1, obj2, obj3):
    # obj2为下标
    if obj2.obj_header.obj_type != OT_INT:
        fatal_print('Runtime error, index must be int')
        sys.exit(1)
    obj1.list.insert(obj2.int, copy.copy(obj3))
    

def _list_append(obj1, obj2):
    obj1.list.append(copy.copy(obj2))


def _list_remove(obj1, obj2):
    # obj2为下标
    if obj2.obj_header.obj_type != OT_INT:
        fatal_print('Runtime error, index must be int')
        sys.exit(1)
    length = list_len(obj1) 
    if obj2.int >= length or obj2.int < 0:
        fatal_print('Runtime error, index out of rang')
        sys.exit(1)
    del obj1.list[obj2.int]


def _map_put(obj1, key, val):
    if key.obj().obj_header.obj_type in [OT_MAP, OT_LIST]:
        fatal_print('Runtime error, map or list cannot be hashed')
        sys.exit(1)
    obj.map[copy.copy(key)] = copy.copy(val)


def _map_get(obj, key):
    if key.obj().obj_header.obj_type == OT_NIL:
        fatal_print('Runtime error, key cannot be nil')
        sys.exit(1)
    if key.obj().obj_header.obj_type in [OT_MAP, OT_LIST]:
        fatal_print('Runtime error, map or list cannot be hashed')
        sys.exit(1)
    if key not in obj.map:
        return Value.to_value(NilObj())
    return copy.copy(obj.map[key])


def _map_remove(obj, key):
    if key.obj().obj_header.obj_type == OT_NIL:
        fatal_print('Runtime error, key cannot be nil')
        sys.exit(1)
    if key.obj().obj_header.obj_type in [OT_MAP, OT_LIST]:
        fatal_print('Runtime error, map or list cannot be hashed')
        sys.exit(1)
    if key in obj.map:
        del obj.map[key]


def _map_to_str(obj):
    s = '{'
    for key in obj.map:
        s += _type_to_pystr(key.obj()) + ': ' + _type_to_pystr(obj.map[key].obj()) + ', '
    return StrObj(s[:-2] + '}')


def _module_to_str(obj):
    addr = str(id(obj))
    return StrObj('<Module(addr: %s) %s>' % (addr, obj.name))


def _fun_to_str(obj):
    addr = str(id(obj))
    return StrObj('<Function(addr: %s) %s>' % (addr, obj.name))

class Value(object):


    def __init__(self, obj_header=NilObj().obj_header, value_type=VT_NIL):
        self.obj_header = obj_header
        self.value_type = value_type
    
    def to_value(self, obj):
        self.obj_header = obj.obj_header
        if is_type(obj, OT_INT):
            self.value_type = VT_INT
        elif is_type(obj, OT_FLOAT):
            self.value_type = VT_FLOAT
        elif is_type(obj, OT_STR):
            self.value_type = VT_STR
        elif is_type(obj, OT_FUN):
            self.value_type = VT_FUN
        elif is_type(obj, OT_MAP):
            self.value_type = VT_MAP
        elif is_type(obj, OT_LIST):
            self.value_type = VT_LIST
        elif is_type(obj, OT_NIL):
            self.value_type = VT_NIL
        elif is_type(obj, OT_BOOL):
            if obj.bool:
                self.value_type = VT_TRUE
            else:
                self.value_type = VT_FALSE
        elif is_type(obj, OT_MODULE):
            self.value_type = VT_MODULE
    
    @classmethod
    def new_value(cls, obj):
        ret = Value(obj.obj_header)
        if is_type(obj, OT_INT):
            ret.value_type = VT_INT
        elif is_type(obj, OT_FLOAT):
            ret.value_type = VT_FLOAT
        elif is_type(obj, OT_STR):
            ret.value_type = VT_STR
        elif is_type(obj, OT_FUN):
            ret.value_type = VT_FUN
        elif is_type(obj, OT_MAP):
            ret.value_type = VT_MAP
        elif is_type(obj, OT_LIST):
            ret.value_type = VT_LIST
        elif is_type(obj, OT_NIL):
            ret.value_type = VT_NIL
        elif is_type(obj, OT_BOOL):
            if obj.bool:
                ret.value_type = VT_TRUE
            else:
                ret.value_type = VT_FALSE
        elif is_type(obj, OT_MODULE):
            ret.value_type = VT_MODULE
        return ret

    def clear_value(self):
        self.obj_header = NilObj().obj_header
        self.value_type = VT_NIL 
    
    def obj(self):
        return self.obj_header.obj

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return call(self.obj(), '_hash(_)')(self.obj()).int


class Frame(object):


    def __init__(self, thread, start):
        self.thread = thread
        self.start = start
        # 含头含尾
        self.end = self.start

    def extend(self, steps=1):
        self.end += steps
        if self.thread.size - 1 - self.end <= 512:
            self.thread.values.extend([Value() for _ in range(self.thread.size)])
            self.thread.size *= 2
    
    def __getitem__(self, idx):
        return self.thread.values[self.start + idx]
    
    def __setitem__(self, idx, val):
        self.thread.values[self.start + idx] = val

    def __str__(self):
        return str((self.start, self.end))


class Thread(object):


    def __init__(self, size=1024):
        self.values = [Value() for _ in range(size)]
        self.frames = []
        self.frame_num = 0
        self.start = 0
        self.size = size
    
    def alloc_frame(self):
        # 第一个frame
        if not self.frames:
            frame = Frame(self, self.start)
            self.frames.append(frame)
            self.frame_num += 1
            return frame
        else:
            cur_frame = self.frames[self.frame_num - 1]
            next_idx = cur_frame.end + 1
            if self.size - 1 - next_idx <= 512:
                self.values.extend([Value() for _ in range(self.size)])
                self.size *= 2
            frame = Frame(self, next_idx)
            self.frames.append(frame)
            self.frame_num += 1
            return frame

    def recycle_frame(self):
        """回收当前的frame
        """
        del self.frames[self.frame_num - 1]
        self.frame_num -= 1
        # 如果还有上一个frame就返回上一个frame
        if self.frame_num >= 1:
            return self.frames[self.frame_num - 1]
        # 没有就返回None
        return None

_bind_methods()

