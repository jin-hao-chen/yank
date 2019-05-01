#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from color_print import *
from tokentype import *


# Y
def read_src(filename, buf_size=1024):
    src = ''
    try:
        with open(filename, 'r') as fd:
            src += fd.read(buf_size)
    except Exception as e:
        fatal_print("Can't read file '%s'" % filename)
        sys.exit(1)
    return src


class Token(object):

    def __init__(self, ptr, line_num, token_type=TOKEN_TYPE_UNKNOWN):
        self.type = token_type
        self.ptr = ptr
        self.len = 1
        self.line_num = line_num
        self.str = None

    def __str__(self):
        return '\033[0;31m%s\033[0m,\033[0;32m%s\033[0m' % (get_token_type_str(self), self.line_num)


class Parser(object):

    def __init__(self, filename):
        self.filename = filename
        self.src = read_src(filename)
        self.src_len = len(self.src)
        self.cur_char_ptr = -1
        self.next_char_ptr = 0
        self.line_num = 1
        self.pre_token = None
        self.cur_token = Token(-1, self.line_num)
    
    # Y
    def fetch_next_token(self):
        """给语法分析器和语义分析器调用的接口, 获取下一个token对象
        """
        self.pre_token = self.cur_token
        self.cur_char_ptr = self.next_char_ptr
        self.next_char_ptr += 1
        self.skip_blanks()
        self.cur_token = Token(-1, self.line_num)
        cur_token = self.cur_token
        while True:
            self.skip_blanks()
            cur_token.ptr = self.cur_char_ptr
            cur_char = self.peek_cur_char()
            if self.cur_char_ptr >= self.src_len - 1:
                cur_token.type = TOKEN_TYPE_EOF
                self.cur_token = cur_token
                return
            if cur_char == ';':
                self.skip_comment()
                cur_token.line_num = self.line_num
                continue
            if cur_char == '\n':
                self.skip_one_line()
                cur_token.line_num = self.line_num
                continue
            elif cur_char.isnumeric():
                self.parse_num(cur_token)
            elif cur_char == '"':
                self.parse_str(cur_token)
                break
            elif cur_char == "'":
                self.parse_str_ex(cur_token)
                break
            elif cur_char == '`':
                self.parse_str_lines(cur_token)
                break
            elif cur_char == '+':
                cur_token.type = TOKEN_TYPE_ADD
            elif cur_char == '-':
                if self.next_char_ptr <= self.src_len - 1 and self.peek_next_char().isnumeric():
                    ptr = cur_token.ptr
                    self.to_next_char()
                    cur_token.ptr = self.cur_char_ptr
                    self.parse_num(cur_token)
                    cur_token.ptr = ptr
                else:
                    cur_token.type = TOKEN_TYPE_SUB
            elif cur_char == '*':
                """
                * or **
                """
                cur_token.ptr = self.cur_char_ptr
                if self.to_next_char_if_next_char_is('*'):
                    cur_token.type = TOKEN_TYPE_POWER
                else:
                    cur_token.type = TOKEN_TYPE_MUL
            elif cur_char == '/':
                cur_token.type = TOKEN_TYPE_DIV
            elif cur_char == '%':
                cur_token.type = TOKEN_TYPE_MOD
            elif cur_char == '^':
                cur_token.type = TOKEN_TYPE_LOGIC_XOR
            elif cur_char == '=':
                """
                = or ==
                """
                cur_token.ptr = self.cur_char_ptr
                if self.to_next_char_if_next_char_is('='):
                    cur_token.type = TOKEN_TYPE_EQU
                else:
                    cur_token.type = TOKEN_TYPE_ASSIGN
            elif cur_char == '!':
                """
                !=
                """
                cur_token.ptr = self.cur_char_ptr
                if self.to_next_char_if_next_char_is('='):
                    cur_token.type = TOKEN_TYPE_NEQU
                else:
                    lex_error("line %s: '!' cannot appear alone" % cur_token.line_num)
            elif cur_char == '>':
                """
                > or >= or >>
                """
                cur_token.ptr = self.cur_char_ptr
                if self.to_next_char_if_next_char_is('>'):
                    cur_token.type = TOKEN_TYPE_LOGIC_SHR
                elif self.to_next_char_if_next_char_is('='):
                    cur_token.type = TOKEN_TYPE_GE 
                else:
                    cur_token.type = TOKEN_TYPE_GT

            elif cur_char == '<':
                """
                < or <= or <<
                """
                cur_token.ptr = self.cur_char_ptr
                if self.to_next_char_if_next_char_is('<'):
                    cur_token.type = TOKEN_TYPE_LOGIC_SHL
                elif self.to_next_char_if_next_char_is('='):
                    cur_token.type = TOKEN_TYPE_LE
                else:
                    cur_token.type = TOKEN_TYPE_LT
            elif cur_char == '&':
                cur_token.type = TOKEN_TYPE_LOGIC_AND 
            elif cur_char == '|':
                cur_token.type = TOKEN_TYPE_LOGIC_OR
            elif cur_char == '^':
                cur_token.type = TOKEN_TYPE_LOGIC_XOR
            elif cur_char == ',':
                cur_token.type = TOKEN_TYPE_COMMA
            elif cur_char == '.':
                cur_token.type = TOKEN_TYPE_POINT
            elif cur_char == ':':
                cur_token.type = TOKEN_TYPE_COLON
            elif cur_char == '(':
                cur_token.type = TOKEN_TYPE_LEFT_PARENT
            elif cur_char == ')':
                cur_token.type = TOKEN_TYPE_RIGHT_PARENT
            elif cur_char == '[':
                cur_token.type = TOKEN_TYPE_LEFT_BRACKET
            elif cur_char == ']':
                cur_token.type = TOKEN_TYPE_RIGHT_BRACKET
            elif cur_char == '{':
                cur_token.type = TOKEN_TYPE_LEFT_BRACE
            elif cur_char == '}':
                cur_token.type = TOKEN_TYPE_RIGHT_BRACE
            elif cur_char == "'":
                cur_token.type = TOKEN_TYPE_SINGLE_QUOTE
            elif cur_char.isalpha() or cur_char == '_':
                self.parse_id(cur_token)
            cur_token.str = self.src[cur_token.ptr: cur_token.ptr + cur_token.len]
            cur_token.len = self.next_char_ptr - cur_token.ptr
            cur_token.line_num = self.line_num
            cur_token.str = self.src[cur_token.ptr: cur_token.ptr + cur_token.len]
            self.cur_token = cur_token
            break
    
    # Y
    def peek_cur_char(self):
        return self.src[self.cur_char_ptr]
    
    # Y
    def peek_next_char(self):
        return self.src[self.next_char_ptr]
    
    # Y
    def peek_remain_src(self):
        return self.src[self.cur_char_ptr:]

    # Y
    def to_next_char_if_next_char_is(self, char):
        if self.next_char_ptr <= self.src_len - 1 and self.peek_next_char() == char:
            self.to_next_char()
            return True
        return False
    # Y 
    def to_next_char(self):
        if self.next_char_ptr <= self.src_len - 1:
            self.cur_char_ptr = self.next_char_ptr
            self.next_char_ptr += 1

    # Y
    def skip_one_line(self):
        while self.next_char_ptr <= self.src_len - 1 and self.peek_cur_char() != '\n':
            self.to_next_char()
        
        if self.next_char_ptr <= self.src_len - 1:
            self.to_next_char()
            self.line_num += 1
    
    # Y
    def skip_comment(self):
        # 在调用skip_comment之前, 已经判断cur_char为';'
        self.skip_one_line()
    
    # Y
    def skip_blanks(self):
        while self.next_char_ptr <= self.src_len - 1 and self.peek_cur_char() == ' ':
            self.to_next_char()
    
    # Y
    def to_next_token_if_cur_token_type_is(self, token_type):
        """
        调用该方法时, self.cur_token已经是一个完整的Token了
        """
        if self.cur_token.type == token_type:
            self.fetch_next_token()
            return True
        return False
    
    # Y
    def to_next_token_danger(self, token_type, msg):
        if not self.to_next_token_if_cur_token_type_is(token_type):
            fatal_print('Parse error, %s' % msg)
            sys.exit(1)
    
    # Y
    def parse_id(self, cur_token):
        while self.next_char_ptr <= self.src_len - 1 and (self.peek_next_char().isalnum() or self.peek_next_char() == '_'):
            self.to_next_char()
        str_len = self.next_char_ptr - cur_token.ptr
        token_str = self.src[cur_token.ptr: cur_token.ptr + str_len]
        if token_str in keyword_strs:
            cur_token.type = keyword_strs[token_str]
        else:
            cur_token.type = TOKEN_TYPE_ID
        
    # Y
    def _parse_str(self, cur_token, char):
        """被parse_str和parse_str_lines函数调用, 用于读取源码中的字符串
        Parameters
        ----------
        cur_token : Token
            当前parser处理的token
        char : character
            在soledad中, 字符串的表示有""和``两种, char用来分辨以哪种结尾, char为"和`其中一个

        Returns
        -------
        token_str : str
            解析出来的字符串
        """
        token_str = self.peek_cur_char()
        while not self.to_next_char_if_next_char_is(char):
            self.to_next_char()
            if self.peek_cur_char() == '\\':
                tmp = self.peek_next_char()
                if tmp == 'n':
                    token_str += '\n'
                elif tmp == 't':
                    token_str += '\t'
                elif tmp == 'a':
                    token_str += '\a'
                elif tmp == '\\':
                    token_str += '\\'
                elif tmp == 'b':
                    token_str += '\b'
                elif tmp == '"':
                    token_str += '"'
                elif tmp == "'":
                    token_str += "'"
                self.to_next_char()
            else:
                token_str += self.peek_cur_char()
            if char == '"':
                if self.cur_char_ptr >= self.src_len - 1 or self.peek_cur_char() == '\n':
                    fatal_print('Line %s, string is not terminated by %s' % (cur_token.line_num, char))
                    sys.exit(1)
            elif char == "'":
                if self.cur_char_ptr >= self.src_len - 1 or self.peek_cur_char() == '\n':
                    fatal_print('Line %s, string is not terminated by %s' % (cur_token.line_num, char))
                    sys.exit(1)
            elif char == '`':
                if self.cur_char_ptr >= self.src_len - 1:
                    fatal_print('Line %s, long string is not terminated by `' % (cur_token.line_num))
                    sys.exit(1)
        token_str += char
        return token_str


    # Y
    def parse_str(self, cur_token):
        """解析字符串, 修改cur_token的属性值, 与其他解析不同, parse_str在fetch_next_token函数中调用, 调用完毕直接返回
        因为需要考虑字符串中控制字符
        """
        cur_token.type = TOKEN_TYPE_STR
        token_str = self._parse_str(cur_token, '"')
        cur_token.str = token_str
        cur_token.line_num = self.line_num
        cur_token.len = len(cur_token.str)
        self.cur_token = cur_token

    def parse_str_ex(self, cur_token):
        """解析字符串, 修改cur_token的属性值, 与其他解析不同, parse_str在fetch_next_token函数中调用, 调用完毕直接返回
        因为需要考虑字符串中控制字符
        """
        cur_token.type = TOKEN_TYPE_STR
        token_str = self._parse_str(cur_token, "'")
        cur_token.str = token_str
        cur_token.line_num = self.line_num
        cur_token.len = len(cur_token.str)
        self.cur_token = cur_token
    
    # Y
    def parse_str_lines(self, cur_token):
        """解析多行字符串, 修改cur_token的属性值, 与其他解析不同, parse_str在fetch_next_token函数中调用, 调用完毕直接返回
        因为需要考虑字符串中控制字符
        """
        cur_token.type = TOKEN_TYPE_STR_LINES
        token_str = self._parse_str(cur_token, '`')
        cur_token.str = token_str
        cur_token.line_num = self.line_num
        cur_token.len = len(cur_token.str)
        self.cur_token = cur_token
        
    # Y
    def _parse_decimal_num(self):
        while self.next_char_ptr <= self.src_len - 1 and self.peek_next_char().isnumeric():
            self.cur_char_ptr = self.next_char_ptr
            self.next_char_ptr += 1
        if self.to_next_char_if_next_char_is('.'):
            while self.next_char_ptr <= self.src_len - 1 and self.peek_next_char().isnumeric():
                self.to_next_char()

    def _parse_octal_num(self):
        while self.next_char_ptr <= self.src_len - 1 and \
                (self.peek_next_char() >= '0' and self.peek_next_char() <= '7'):
            self.to_next_char()

    def _parse_hex_num(self):
        while self.next_char_ptr <= self.src_len - 1 and \
                ((self.peek_next_char() >= '0' and self.peek_next_char() <= '9') or \
                (self.peek_next_char() >= 'a' and self.peek_next_char() <= 'f') or \
                (self.peek_next_char() >= 'A' and self.peek_next_char() <= 'F')):
            self.to_next_char()

    def _parse_binary_num(self):
        while self.next_char_ptr <= self.src_len - 1 and \
                (self.peek_next_char() >= '0' and self.peek_next_char() <= '1'):
            self.to_next_char()

    # Y
    def parse_num(self, cur_token):
        """解析数字, 包括整数, 小数和负数
        """
        cur_token.type = TOKEN_TYPE_NUM
        prefix = self.peek_cur_char()
        if prefix != '0':
            self._parse_decimal_num()

        else:
            next_prefix = self.peek_next_char()
            # 8进制
            if next_prefix.isnumeric():
                self._parse_octal_num()
            elif next_prefix == 'x':
                self.to_next_char()
                self._parse_hex_num()
            elif next_prefix == 'b':
                self.to_next_char()
                self._parse_binary_num()
    
    # Y
    def print_remained_src(self):
        """开发调试辅助函数, 剩余需要解析的字符串
        """
        print('***Debug***' + self.src[self.cur_char_ptr: self.cur_char_ptr + self.src_len])


# Y
def get_token_type_str(token):
    """根据传入的token对象的类型返回该token的类型的字符串表达
    Parameters
    ----------
    token : Token

    Returns
    --------
    str : str
    """
    token_type = token.type
    if token_type == TOKEN_TYPE_IF:
        return '(keyword)if'
    elif token_type == TOKEN_TYPE_ELIF:
        return '(keyword)elif'
    elif token_type == TOKEN_TYPE_ELSE:
        return '(keyword)else'
    elif token_type == TOKEN_TYPE_FOR:
        return '(keyword)for'
    elif token_type == TOKEN_TYPE_IN:
        return '(keyword)in'
    elif token_type == TOKEN_TYPE_WHILE:
        return '(keyword)while'
    elif token_type == TOKEN_TYPE_BREAK:
        return '(keyword)break'
    elif token_type == TOKEN_TYPE_NOT:
        return '(keyword)not'
    elif token_type == TOKEN_TYPE_AND:
        return '(keyword)and'
    elif token_type == TOKEN_TYPE_OR:
        return '(keyword)or'
    elif token_type == TOKEN_TYPE_RETURN:
        return '(keyword)return'
    elif token_type == TOKEN_TYPE_IMPORT:
        return '(keyword)import'
    elif token_type == TOKEN_TYPE_FUN:
        return '(keyword)fun'
    elif token_type == TOKEN_TYPE_CLASS:
        return '(keyword)class'
    elif token_type == TOKEN_TYPE_LET:
        return '(keyword)let'
    elif token_type == TOKEN_TYPE_GLOBAL:
        return '(keyword)global'
    elif token_type == TOKEN_TYPE_TRUE:
        return '(keyword)True'
    elif token_type == TOKEN_TYPE_FALSE:
        return '(keyword)False'
    elif token_type == TOKEN_TYPE_CONTINUE:
        return '(keyword)continue'
    elif token_type == TOKEN_TYPE_DEL:
        return '(keyword)del'
    elif token_type == TOKEN_TYPE_ADD:
        return '(add)+'
    elif token_type == TOKEN_TYPE_SUB:
        return '(sub)-'
    elif token_type == TOKEN_TYPE_MUL:
        return '(mul)*'
    elif token_type == TOKEN_TYPE_DIV:
        return '(div)/'
    elif token_type == TOKEN_TYPE_MOD:
        return '(mod)%'
    elif token_type == TOKEN_TYPE_POWER:
        return '(power)**'
    elif token_type == TOKEN_TYPE_EQU:
        return '(equ)=='
    elif token_type == TOKEN_TYPE_NEQU:
        return '(nequ)!='
    elif token_type == TOKEN_TYPE_GT:
        return '(gt)>'
    elif token_type == TOKEN_TYPE_LT:
        return '(lt)<'
    elif token_type == TOKEN_TYPE_GE:
        return '(ge)>='
    elif token_type == TOKEN_TYPE_LE:
        return '(le)<='
    elif token_type == TOKEN_TYPE_ASSIGN:
        return '(assign)='
    elif token_type == TOKEN_TYPE_LOGIC_AND:
        return '(logic_and)&'
    elif token_type == TOKEN_TYPE_LOGIC_OR:
        return '(logic_or)|'
    elif token_type == TOKEN_TYPE_LOGIC_NOT:
        return '(logic_not)~'
    elif token_type == TOKEN_TYPE_LOGIC_XOR:
        return '(logic_xor)^'
    elif token_type == TOKEN_TYPE_LOGIC_SHL:
        return '(logic_shl)<<'
    elif token_type == TOKEN_TYPE_LOGIC_SHR:
        return '(logic_shr)>>'
    elif token_type == TOKEN_TYPE_NUM:
        return '(num)' + token.str
    elif token_type == TOKEN_TYPE_STR:
        return '(str)' + token.str
    elif token_type == TOKEN_TYPE_COMMA:
        return '(comma),'
    elif token_type == TOKEN_TYPE_POINT:
        return '(point).'
    elif token_type == TOKEN_TYPE_COLON:
        return '(colon):'
    elif token_type == TOKEN_TYPE_SEMICOLON:
        return '(semicolon);'
    elif token_type == TOKEN_TYPE_LEFT_PARENT:
        return '(left_parent)('
    elif token_type == TOKEN_TYPE_RIGHT_PARENT:
        return '(right_parent))'
    elif token_type == TOKEN_TYPE_LEFT_BRACKET:
        return '(left_bracket)['
    elif token_type == TOKEN_TYPE_RIGHT_BRACKET:
        return '(right_bracket)]'
    elif token_type == TOKEN_TYPE_LEFT_BRACE:
        return '(left_brace){'
    elif token_type == TOKEN_TYPE_RIGHT_BRACE:
        return '(right_brace)}'
    elif token_type == TOKEN_TYPE_DOUBLE_QUOTATION:
        return '(double_quotation)"'
    elif token_type == TOKEN_TYPE_SINGLE_QUOTE:
        return "(single_quote)'"
    elif token_type == TOKEN_TYPE_ID:
        return '(id)' + token.str
    elif token_type == TOKEN_TYPE_STR_LINES:
        return '(str_line)' + token.str
    elif token_type == TOKEN_TYPE_SELF:
        return '(keyword)this'
    elif token_type == TOKEN_TYPE_UNKNOWN:
        return '(unknown)UNKNOWN'
    elif token_type == TOKEN_TYPE_EOF:
        return '(eof)EOF'
    print("Token '%s' doesn't exist!" % token.str)
    sys.exit(1)
