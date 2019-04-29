#!/usr/bin/env python

# Keyword
TOKEN_TYPE_IF = 0
TOKEN_TYPE_ELIF = 1
TOKEN_TYPE_ELSE = 2
TOKEN_TYPE_FOR = 3
TOKEN_TYPE_IN = 4
TOKEN_TYPE_WHILE = 5
TOKEN_TYPE_BREAK = 6
TOKEN_TYPE_NOT = 7
TOKEN_TYPE_AND = 8
TOKEN_TYPE_OR = 9
TOKEN_TYPE_RETURN = 10
TOKEN_TYPE_IMPORT = 11
TOKEN_TYPE_FUN = 12
TOKEN_TYPE_CLASS = 13
TOKEN_TYPE_LET = 14
TOKEN_TYPE_GLOBAL = 15
TOKEN_TYPE_TRUE = 16
TOKEN_TYPE_FALSE = 17
TOKEN_TYPE_CONTINUE = 18
TOKEN_TYPE_DEL = 19

keyword_strs = {
        'if': TOKEN_TYPE_IF,
        'elif': TOKEN_TYPE_ELIF,
        'else': TOKEN_TYPE_ELSE,
        'for': TOKEN_TYPE_FOR,
        'in': TOKEN_TYPE_IN,
        'while': TOKEN_TYPE_WHILE,
        'break': TOKEN_TYPE_BREAK,
        'not': TOKEN_TYPE_NOT,
        'and': TOKEN_TYPE_AND,
        'or': TOKEN_TYPE_OR,
        'return': TOKEN_TYPE_RETURN,
        'import': TOKEN_TYPE_IMPORT,
        'fun': TOKEN_TYPE_FUN,
        'class': TOKEN_TYPE_CLASS,
        'let': TOKEN_TYPE_LET,
        'global': TOKEN_TYPE_GLOBAL,
        'True': TOKEN_TYPE_TRUE,
        'False': TOKEN_TYPE_FALSE,
        'continue': TOKEN_TYPE_CONTINUE,
        'del': TOKEN_TYPE_DEL,
}


# Arithmetic operators
TOKEN_TYPE_ADD = 20
TOKEN_TYPE_SUB = 21
TOKEN_TYPE_MUL = 22
TOKEN_TYPE_DIV = 23
TOKEN_TYPE_MOD = 24 # %
TOKEN_TYPE_POWER = 25

#  Logical operators
TOKEN_TYPE_EQU = 26
TOKEN_TYPE_NEQU = 27 # !=
TOKEN_TYPE_GT = 28
TOKEN_TYPE_LT = 29
TOKEN_TYPE_GE = 30
TOKEN_TYPE_LE = 31

# Assigning operator
TOKEN_TYPE_ASSIGN = 32

# Bitwise operator
TOKEN_TYPE_LOGIC_AND = 33
TOKEN_TYPE_LOGIC_OR = 34
TOKEN_TYPE_LOGIC_XOR = 35
TOKEN_TYPE_LOGIC_NOT = 36
TOKEN_TYPE_LOGIC_SHL = 37
TOKEN_TYPE_LOGIC_SHR = 38

# Data type
TOKEN_TYPE_NUM = 39
TOKEN_TYPE_STR = 40

# Others
TOKEN_TYPE_COMMA = 41
TOKEN_TYPE_POINT = 42
TOKEN_TYPE_COLON = 43 # :
TOKEN_TYPE_SEMICOLON = 44 # ;, ; is comment

TOKEN_TYPE_LEFT_PARENT = 45 # (
TOKEN_TYPE_RIGHT_PARENT = 46 # )
TOKEN_TYPE_LEFT_BRACKET = 47 # [
TOKEN_TYPE_RIGHT_BRACKET = 48 # ]
TOKEN_TYPE_LEFT_BRACE = 49 # {
TOKEN_TYPE_RIGHT_BRACE = 50 # }
TOKEN_TYPE_DOUBLE_QUOTATION = 51
TOKEN_TYPE_SINGLE_QUOTE = 52 # ' is anonymous function 

TOKEN_TYPE_EOF = 53 # The end of file
TOKEN_TYPE_UNKNOWN = 54

# Extra
TOKEN_TYPE_NIL = 55 # File start sign
TOKEN_TYPE_ID = 56
TOKEN_TYPE_SPACER = 57 # `
TOKEN_TYPE_STR_LINES = 58

TOKEN_TYPE_SELF = 59
