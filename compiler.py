#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from tokentype import *
from color_print import warning_print


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
        # parser获取token
        self.parser = parser
        # module与fun只能有一个有效, 存放编译的指令
        self.fun = fun
        # 默认为模块编译单元
        self.scope = scope
        self.local_vars = []
        self.local_var_num = 0
        self.outter_cu = None
        self.cur_loop = None
    
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

    def define_var(self, var):
        if self.module:
            module_idx = self.module.find_var(var)
            # 第一次定义var
            if module_idx == -1:
                module_idx = self.module.add_var(var)
            else:
                self.module.global_vars[module_idx] = var
        elif self.fun:
            fun_idx = self.fun.find_var(var)
            if fun_idx == -1:
                fun_idx = self.fun.add_var(var)
            else:
                self.fun.local_vars[fun_idx] = var
        warning_print('module and fun are both None')
        sys.exit(1) 
    
    def discard_var(self, var):
        if self.module:
            module_idx = self.module.find_var(var)
            # 第一次定义var
            if module_idx == -1:
                return False
            del self.module.global_vars[module_idx]
            return True
            
        elif self.fun:
            fun_idx = self.fun.find_var(var)
            if fun_idx == -1:
                return False
            else:
                del self.fun.local_vars[fun_idx]
                return True
        warning_print('module and fun are both None')
        sys.exit(1) 

    def get_vars(self):
        if self.module:
            return self.module.global_vars
        elif self.fun:
            return self.fun.local_vars
        warning_print('module and fun are both None')
        sys.exit(1) 

    def get_type(self):
        if self.module:
            return 'module_cu'
        elif self.fun:
            return 'fun_cu'
        warning_print('module and fun are both None')
        sys.exit(1) 
    
    def get_module_or_fun(self):
        if self.module:
            return self.module
        elif self.fun:
            return self.fun
        warning_print('module and fun are both None')
        sys.exit(1) 


# 和JS一样, 除了函数, 其他结构没有自己的域, 他们都在同一个作用域中
class Loop(object):


    def __init__(self, scope=0):
        # 一般和父是一样的, 模仿JS
        self.scope = scope
        self.condition_start = 0
        self.body_start = 0
        self.exit = 0
        self.outter_loop = None


def main(argv=None):
    pass


if __name__ == '__main__':
    main()
