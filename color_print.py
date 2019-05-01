#!/usr/bin/env python
# -*- coding: utf-8 -*-


FATAL = '\033[0;31;m'
WARNING = '\033[0;33;m'
SUCCESS = '\033[0;32;m'
NORMAL = '\033[0;m'


_END = '\033[0m'


def color_print(msg, level=NORMAL, hint=''):
    print(level + hint + msg + _END)

def fatal_print(msg, hint='FATAL: '):
    color_print(msg, level=FATAL, hint=hint)

def warning_print(msg, hint='WARNING: '):
    color_print(msg, level=WARNING, hint=hint)

def success_print(msg, hint='SUCCESS: '):
    color_print(msg, level=SUCCESS, hint=hint)

def norml_print(msg, hint=''):
    color_print(msg, level=NORMAL, hint=hint)

def color_str(msg, level=NORMAL):
    return level + msg + _END

def fatal_str(msg):
    return color_str(msg, level=FATAL)

def warning_str(msg):
    return color_str(msg, level=WARNING)

def success_str(msg):
    return color_str(msg, level=SUCCESS)

def normal_str(msg):
    return color_str(msg, level=NORMAL)


def main(argv=None):
    fatal_print('WTF')


if __name__ == '__main__':
    main()
