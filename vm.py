#!/usr/bin/env python
# -*- coding: utf-8 -*-


from objects import (module_cls, fun_cls, nil_cls, bool_cls, str_cls, int_cls, \
                        float_cls, list_cls, map_cls)


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
        self.module_cls = module_cls
        self.builtin_clses = [fun_cls, nil_cls, bool_cls, str_cls, int_cls, float_cls, list_cls, map_cls, module_cls]
        """
        self.method_names = ['nil.tostr()', 'nil.==(_)', 'nil.hash(_)',
                            'bool.tostr()', 'bool.==(_)', 'bool.hash()',
                            'str.tostr()', 'str.==(_)', 'str.hash()','str.+(_)', 
                            'str.at(_)', 'str.len()', 'str.empty()', 'str.numbers()', 
                            'int.tostr()', 'int.==(_)', 'int.hash()', 'int.float()',
                            'int.+(_)', 'int.-(_)', 'int.*(_)', 'int./(_)', 'int.%(_)',
                            'int.>(_)', 'int.>=(_)', 'int.<(_)', 'int.<=(_)',
                            'float.tostr()', 'float.==(_)', 'float.hash()', 'float.int()',
                            'float.+(_)', 'float.-(_)', 'float.*(_)', 'float./(_)',
                            'float.>(_)', 'float.>=(_)', 'float.<(_)', 'float.<=(_)',
                            'list.len()', 'list.tostr()', 'list.insert(_,_)', 'list.at(_)',
                            'list.remove(_)', 'list.append(_)', 'map.tostr()', 
                            'map.put(_,_)', 'map.get(_)', 'map.remove(_)', 'map.@put(_,_)',
                            'map.@get(_)', 'map.@remove(_)']
        """
    
    def build_core_module(self):
        pass
