#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys


def call(obj, method_name):
    return obj.obj_header.cls_obj.methods[method_name]

# 方法地窖, 就是存放所有的方法
class Cellar(object):
    pass


class ObjHeader(object):
    

    def __init__(self, obj_type, cls_obj, obj):
        self.obj_type = obj_type 
        self.cls_obj = cls_obj
        self.obj = obj


class ClsObj(object):


    def __init__(self, name):
        self.name = name
        self.methods = {}


bool_cls = ClsObj('bool_cls')
str_cls = ClsObj('str_cls')
int_cls = ClsObj('int_cls')
float_cls = ClsObj('float_cls')
list_cls = ClsObj('list_cls')
map_cls = ClsObj('map_cls')


############################# bool methods ###################

def bool_to_str(obj):
    return StrObj(str(obj.bool))

def bool_equ(obj1, obj2):
    return BoolObj(obj1.bool == obj2.bool)

def bool_hash(obj):
    return IntObj(hash(obj.bool))

def bool_bind_methods():
    bool_cls.methods['bool_to_str'] = bool_to_str
    bool_cls.methods['bool_equ'] = bool_equ
    bool_cls.methods['bool_hash'] = bool_hash

############################ str methods #######################

def str_to_str(obj):
    return obj

def str_equ(obj1, obj2):
    return BoolObj(obj1.str == obj2.str)

def str_hash(obj):
    return IntObj(hash(obj.str))

def str_add(obj1, obj2):
    return StrObj(obj1.str + obj2.str)

def str_at(obj1, obj2):
    if obj2.obj_header.obj_type != 'int':
        print('***Run error: index must be int***')
        sys.exit(1)
    return StrObj(obj1.str[obj2.int])

def str_len(obj):
    return IntObj(len(obj.str))

def str_bind_methods():
    str_cls.methods['str_to_str'] = str_to_str
    str_cls.methods['str_equ'] = str_equ
    str_cls.methods['str_hash'] = str_hash
    str_cls.methods['str_add'] = str_add
    str_cls.methods['str_at'] = str_at
    str_cls.methods['str_len'] = str_len


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
        print('***Run error: %s obj2 is not a number***')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == 'float':
        return FloatObj(obj1.float + obj2.float)

    if obj1.obj_header.obj_type == 'int':
        return IntObj(obj1.int + obj2.int)

def int_sub(obj1, obj2):
    if obj2.obj_header.obj_type == 'float':
        obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == 'float':
        return FloatObj(obj1.float - obj2.float)

    if obj1.obj_header.obj_type == 'int':
        return IntObj(obj1.int - obj2.int)

def int_mul(obj1, obj2):
    if obj2.obj_header.obj_type == 'float':
        obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == 'float':
        return FloatObj(obj1.float * obj2.float)

    if obj1.obj_header.obj_type == 'int':
        return IntObj(obj1.int * obj2.int)

def int_div(obj1, obj2):
    if obj2.obj_header.obj_type == 'float':
        obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    
    if obj1.obj_header.obj_type == 'float':
        if obj2.float == 0.0:
            print('***Run error: obj2 is 0***')
            sys.exit(1)
        return FloatObj(obj1.float / obj2.float)

    if obj1.obj_header.obj_type == 'int':
        if obj2.int == 0:
            print('***Run error: obj2 is 0***')
            sys.exit(1)
        return IntObj(obj1.int / obj2.int)

def int_mod(obj1, obj2):
    if obj2.obj_header.obj_type != 'int':
        print('***Run error: obj2 should be int***')
        sys.exit(1)
    
    if obj2.int == 0:
        print('***Run error: obj2 is 0***')
        sys.exit(1)
    return IntObj(obj1.int % obj2.int)

def int_gt(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    obj1 = int_to_float(obj1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    return BoolObj(obj1.float > obj2.float)

def int_ge(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    obj1 = int_to_float(obj1)
    
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    return BoolObj(obj1.float >= obj2.float)

def int_lt(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
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
    int_cls.methods['int_to_str'] = int_to_str
    int_cls.methods['int_equ'] = int_equ
    int_cls.methods['int_hash'] = int_hash
    int_cls.methods['int_to_float'] = int_to_float
    int_cls.methods['int_add'] = int_add
    int_cls.methods['int_sub'] = int_sub
    int_cls.methods['int_mul'] = int_mul
    int_cls.methods['int_div'] = int_div
    int_cls.methods['int_mod'] = int_mod
    int_cls.methods['int_gt'] = int_gt
    int_cls.methods['int_ge'] = int_ge
    int_cls.methods['int_lt'] = int_lt
    int_cls.methods['int_le'] = int_le
    

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
        print('***Run error: %s obj2 is not a number***')
        sys.exit(1)
    
    return FloatObj(obj1.float + obj2.float)

def float_sub(obj1, obj2):
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: %s obj2 is not a number***')
        sys.exit(1)
    return FloatObj(obj1.float - obj2.float)

def float_mul(obj1, obj2):
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: %s obj2 is not a number***')
        sys.exit(1)
    return FloatObj(obj1.float * obj2.float)

def float_div(obj1, obj2):
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2)
    
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: %s obj2 is not a number***')
        sys.exit(1)
    if obj2.float == 0:
        print('***Run error: obj2 is 0***')
    return FloatObj(obj1.float / obj2.float)

def float_gt(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2) 
    return BoolObj(obj1.float > obj2.float)

def float_ge(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2) 
    return BoolObj(obj1.float >= obj2.float)

def float_lt(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2) 
    return BoolObj(obj1.float < obj2.float)

def float_le(obj1, obj2):
    if obj2.obj_header.obj_type not in ['float', 'int']:
        print('***Run error: obj2 is not a number***')
        sys.exit(1)
    if obj2.obj_header.obj_type == 'int':
        obj2 = int_to_float(obj2) 
    return BoolObj(obj1.float <= obj2.float)

def float_bind_methods():
    float_cls.methods['float_to_str'] = float_to_str
    float_cls.methods['float_equ'] = float_equ
    float_cls.methods['float_hash'] = float_hash
    float_cls.methods['float_to_int'] = float_to_int
    float_cls.methods['float_add'] = float_add
    float_cls.methods['float_sub'] = float_sub
    float_cls.methods['float_mul'] = float_mul
    float_cls.methods['float_div'] = float_div
    float_cls.methods['float_gt'] = float_gt
    float_cls.methods['float_ge'] = float_ge
    float_cls.methods['float_lt'] = float_lt
    float_cls.methods['float_le'] = float_le

def list_len(obj):
    return IntObj(len(obj.list))

def list_to_str(obj):
    s = '['
    for item in obj.list:
        if item.obj_header.obj_type == 'int':
            s += int_to_str(item).str
        elif item.obj_header.obj_type == 'float':
            s += float_to_str(item).str
        elif item.obj_header.obj_type == 'str':
            s += str_to_str(item).str
        elif item.obj_header.obj_type == 'list':
            s += list_to_str(item).str
        elif item.obj_header.obj_type == 'map':
            pass
        elif item.obj_header.obj_type == 'fun':
            pass
        s += ','
    s = s[:-1] + ']'
    return StrObj(s)

def list_at(obj1, obj2):
    if obj2.obj_header.obj_type != 'int':
        print('***Run error: obj2 must be int***')
        sys.exit(1)
    return obj1.list[obj2.int]

def list_insert(obj1, obj2, obj3):
    """obj3: 下标
    """
    if obj3.obj_header.obj_type != 'int':
        print('***Run error: index must be int***')
        sys.exit(1)
    obj1.list.insert(obj3.int, obj2)
    
def list_append(obj1, obj2):
    obj1.list.append(obj2)

def list_remove(obj1, obj2):
    """obj2: 下标
    """
    if obj2.obj_header.obj_type != 'int':
        print('***Run error: index must be int***')
        sys.exit(1)
    length = list_len(obj1) 
    if obj2.int >= length or obj2.int < 0:
        print('***Run error: index out of rang***')
        sys.exit(1)
    del obj1.list[obj2.int]


def list_bind_methods():
    list_cls.methods['list_len'] = list_len
    list_cls.methods['list_to_str'] = list_to_str
    list_cls.methods['list_insert'] = list_insert
    list_cls.methods['list_at'] = list_at
    list_cls.methods['list_remove'] = list_remove
    list_cls.methods['list_append'] = list_append


class BoolObj(object):

    def __init__(self, boolean):
        self.obj_header = ObjHeader('bool', bool_cls, self)
        self.bool = boolean

class StrObj(object):
    
    def __init__(self, string):
        self.obj_header = ObjHeader('str', str_cls, self) 
        self.str = str(string)


class IntObj(object):

    def __init__(self, integer):
        self.obj_header = ObjHeader('int', int_cls, self)
        self.int = int(integer)
    

class FloatObj(object):

    def __init__(self, float_):
        self.obj_header = ObjHeader('float', float_cls, self)
        self.float = float(float_)


class ListObj(object):

    def __init__(self, list_):
        self.obj_header = ObjHeader('list', list_cls, self)
        self.list = list(list_)

class MapObj(object):

    def __init__(self, map_):
        self.obj_header = ObjHeader('map', map_cls, self)
        self.map = map(map_)

    
def bind_methods():
    bool_bind_methods()
    str_bind_methods()
    int_bind_methods()
    float_bind_methods()
    list_bind_methods()


bind_methods()


def main(argv=None):
    pass


if __name__ == '__main__':
    main()
