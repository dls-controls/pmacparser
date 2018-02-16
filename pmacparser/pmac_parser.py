from math import sqrt, sin, cos, tan, asin, acos, atan, atan2, exp, log, degrees, radians

from pygments.token import Number
from pmacparser.pmac_lexer import PmacLexer


class ParserError(Exception):
    """Parser error exception."""
    def __init__(self, message, token):
        super(ParserError, self).__init__()
        self.message = message
        self.line = token.line

    def __str__(self):
        return '[Line %s] %s' % (self.line, self.message)


class Variables(object):
    """ Represents a PMAC Variable (I, M, P, Q) """
    def __init__(self):
        self.variable_dict = {}

    def get_i_variable(self, var_num):
        return self.get_var('I', var_num)

    def get_p_variable(self, var_num):
        return self.get_var('P', var_num)

    def get_q_variable(self, var_num):
        return self.get_var('Q', var_num)

    def get_m_variable(self, var_num):
        return self.get_var('M', var_num)

    def set_i_variable(self, var_num, value):
        self.set_var('I', var_num, value)

    def set_p_variable(self, var_num, value):
        self.set_var('P', var_num, value)

    def set_q_variable(self, var_num, value):
        self.set_var('Q', var_num, value)

    def set_m_variable(self, var_num, value):
        self.set_var('M', var_num, value)

    def get_var(self, t, var_num):
        addr = '%s%s' % (t, var_num)
        if addr in self.variable_dict:
            result = float(self.variable_dict[addr])
        else:
            result = 0
        return result

    def set_var(self, t, var_num, value):
        addr = '%s%s' % (t, var_num)
        self.variable_dict[addr] = value

    def populate_with_dict(self, dictionary):
        self.variable_dict = dictionary.copy()

    def to_dict(self):
        return self.variable_dict


class PMACParser(object):
    """Uses the PMAC Lexer to tokenise a list of strings, and then parses the tokens,
    using an input dictionary or variables to evaluate the expressions in the code,
    populating a dictionary with the results of the program operations.
    It is a modification of the dls_pmacanalyse code developed by J Thompson.
    """
    def __init__(self, program_lines):
        self.lexer = PmacLexer()
        self.lines = program_lines
        self.lexer.lex(self.lines)
        self.variable_dict = Variables()
        self.if_level = 0
        self.while_level = 0
        self.while_dict = {}
        self.pre_process()

    def tokens(self):
        return self.lexer.tokens

    def pre_process(self):
        """Evaluate and replace any Constants Expressions (e.g. 4800+17)"""
        t = self.lexer.get_token()
        while t is not None:
            if t.type == Number.ConstantExpression:
                token_text = str(t)
                token_text = token_text.replace("(", "")
                token_text = token_text.replace(")", "")
                tokens = token_text.split("+")
                int1 = int(tokens[0])
                int2 = int(tokens[1])
                val = int1 + int2
                t.set(str(val), t.line)
                t.type = Number

            t = self.lexer.get_token()
        self.lexer.reset()

    def parse(self, variable_dict):
        """Top level kinematic program parser."""
        self.variable_dict.populate_with_dict(variable_dict)

        t = self.lexer.get_token()
        while t is not None:
            if t == 'Q':
                self.parseQ()
            elif t == 'P':
                self.parseP()
            elif t == 'I':
                self.parseI()
            elif t == 'M':
                self.parseM()
            elif t == 'IF':
                self.parseIf()
            elif t == 'ELSE':
                self.parseElse(t)
            elif t == 'ENDIF':
                self.parseEndIf(t)
            elif t == 'WHILE':
                self.parseWhile(t)
            elif t == 'ENDWHILE':
                self.parseEndWhile(t)
            else:
                raise ParserError('Unexpected token: %s' % t, t)
            t = self.lexer.get_token()

        self.lexer.reset()
        return self.variable_dict.to_dict()

    def parseM(self):
        """Parse an M expression - typically an assignment"""
        n = self.lexer.get_token()
        if n.is_int():
            n = n.to_int()
            t = self.lexer.get_token()
            if t == '=':
                val = self.parseExpression()
                self.variable_dict.set_m_variable(n, val)
            else:
                self.lexer.put_token(t)
                # Report M variable values (do nothing)
        else:
            raise ParserError('Unexpected statement: M %s' % n, n)

    def parseI(self):
        """Parse an I expression - typically an assignment"""
        n = self.lexer.get_token()
        if n.is_int():
            n = n.to_int()
            t = self.lexer.get_token()
            if t == '=':
                val = self.parseExpression()
                self.variable_dict.set_i_variable(n, val)
            else:
                self.lexer.put_token(t)
                # Report I variable values (do nothing)
        elif n == '(':
            n = self.parseExpression()
            t = self.lexer.get_token(')')
            t = self.lexer.get_token()
            if t == '=':
                val = self.parseExpression()
                self.variable_dict.set_i_variable(n, val)
            else:
                self.lexer.put_token(t)
                # Report I variable values (do nothing)
        else:
            raise ParserError('Unexpected statement: I %s' % n, n)

    def parseP(self):
        """Parse a P expression - typically an assignment"""
        n = self.lexer.get_token()
        if n.is_int():
            n = n.to_int()
            t = self.lexer.get_token()
            if t == '=':
                val = self.parseExpression()
                self.variable_dict.set_p_variable(n, val)
            else:
                self.lexer.put_token(t)
                # Report P variable values (do nothing)
        elif n == '(':
            n = self.parseExpression()
            t = self.lexer.get_token(')')
            t = self.lexer.get_token()
            if t == '=':
                val = self.parseExpression()
                self.variable_dict.set_p_variable(n, val)
            else:
                self.lexer.put_token(t)
                # Report P variable values (do nothing)
        else:
            self.lexer.put_token(n)
            # Do nothing

    def parseQ(self):
        """Parse a Q expression - typically an assignment"""
        n = self.lexer.get_token()
        if n.is_int():
            n = n.to_int()
            t = self.lexer.get_token()
            if t == '=':
                val = self.parseExpression()
                self.variable_dict.set_q_variable(n, val)
            else:
                self.lexer.put_token(t)
                # Report Q variable values (do nothing)
        elif n == '(':
            n = self.parseExpression()
            t = self.lexer.get_token(')')
            t = self.lexer.get_token()
            if t == '=':
                val = self.parseExpression()
                self.variable_dict.set_q_variable(n, val)
            else:
                self.lexer.put_token(t)
                # Report Q variable values (do nothing)
        else:
            self.lexer.put_token(n)
            # Do nothing

    def parseCondition(self):
        """Parse a condition, return the result of the condition"""
        has_parenthesis = True
        t = self.lexer.get_token()
        if t != '(':
            self.lexer.put_token(t)
            has_parenthesis = False
            # raise ParserError('Expected (, got: %s' % t, t)

        value1 = self.parseExpression()
        t = self.lexer.get_token()
        comparator = t
        value2 = self.parseExpression()

        if comparator == '=':
            result = value1 == value2
        elif comparator == '!=':
            result = value1 != value2
        elif comparator == '>':
            result = value1 > value2
        elif comparator == '!>':
            result = value1 <= value2
        elif comparator == '<':
            result = value1 < value2
        elif comparator == '!<':
            result = value1 >= value2
        else:
            raise ParserError('Expected comparator, got: %s' % comparator, comparator)

        # Take ) or AND or OR
        t = self.lexer.get_token()
        if t == 'AND' or t == 'OR':
            self.lexer.put_token(t)
            result = self.parseConditionalOR(result)
            if has_parenthesis:
                t = self.lexer.get_token(')')
        elif t == ')':
            if not has_parenthesis:
                self.lexer.put_token(t)
        elif t != ')':
            raise ParserError('Expected ) or AND/OR, got: %s' % comparator, comparator)

        return result

    def parseConditionalOR(self, current_value):
        """Parse a conditional OR token, return the result of the condition"""
        result = self.parseConditionalAND(current_value)
        t = self.lexer.get_token()
        if t == 'OR':
            condition_result = self.parseCondition()
            result = self.parseConditionalOR(condition_result) or current_value
        elif t == 'AND':
            self.lexer.put_token(t)
            result = self.parseConditionalOR(result)
        else:
            self.lexer.put_token(t)

        return result

    def parseConditionalAND(self, current_value):
        """Parse a conditional AND token, return the result of the condition"""
        t = self.lexer.get_token()
        if t == 'AND':
            result = self.parseCondition() and current_value
        else:
            self.lexer.put_token(t)
            result = current_value
        return result

    def parseIf(self):
        """Parse an IF token, skipping to after the else necessary"""
        condition = self.parseCondition()

        condition = self.parseConditionalOR(condition)

        if_condition = condition

        self.if_level += 1
        if not if_condition:
            this_if_level = self.if_level
            t = self.lexer.get_token()
            while (t != 'ELSE' and t != 'ENDIF') or this_if_level != self.if_level:
                if t == 'ENDIF':
                    self.if_level -= 1
                t = self.lexer.get_token()
                if t == 'IF':
                    self.if_level += 1
                    # self.lexer.putToken(t)

            if t == 'ENDIF':
                self.parseEndIf(t)

    def parseElse(self, t):
        """Parse an ELSE token, skipping to ENDIF if necessary"""
        if self.if_level > 0:
            this_if_level = self.if_level
            while t != 'ENDIF' or this_if_level != self.if_level:
                if t == 'ENDIF':
                    self.if_level -= 1

                t = self.lexer.get_token()

                if t == 'IF':
                    self.if_level += 1
        else:
            raise ParserError('Unexpected ELSE', t)

    def parseEndIf(self,t):
        """Parse an ENDIF token, closing off the current IF level"""
        if self.if_level > 0:
            self.if_level -= 1
        else:
            raise ParserError('Unexpected ENDIF', t)

    def parseWhile(self, t):
        """Parse a WHILE token, skipping to the ENDWHILE the condition is false"""
        self.while_level += 1

        # Get all tokens up to the ENDWHILE
        while_tokens = []
        this_while_level = self.while_level
        while_tokens.append(t)

        while (t != 'ENDWHILE') or this_while_level != self.while_level:
            if t == 'ENDWHILE':
                self.while_level -= 1

            t = self.lexer.get_token()
            while_tokens.append(t)

            if t == 'WHILE':
                self.while_level += 1

        # Put the tokens back on
        self.lexer.put_tokens(while_tokens)

        # Get the WHILE
        t = self.lexer.get_token()

        condition = self.parseCondition()

        condition = self.parseConditionalOR(condition)

        if condition:
            self.while_dict[this_while_level] = while_tokens
        else:
            while (t != 'ENDWHILE') or this_while_level != self.while_level:
                if t == 'ENDWHILE':
                    self.while_level -= 1

                t = self.lexer.get_token()
                while_tokens.append(t)

                if t == 'WHILE':
                    self.while_level += 1
            self.while_level -= 1

    def parseEndWhile(self, t):
        """Parse an ENDWHILE statement, placing the tokens within the while back on to the list to be executed"""
        if self.while_level > 0:

            while_tokens = self.while_dict[self.while_level]

            # Put the tokens back on
            self.lexer.put_tokens(while_tokens)

            self.while_level -= 1
        else:
            raise ParserError('Unexpected ENDWHILE', t)

    def parseExpression(self):
        """Return the result of the expression."""
        # Currently supports syntax of the form:
        #    <expression> ::= <e1> { <sumop> <e1> }
        #    <e1> ::= <e2> { <multop> <e2> }
        #    <e2> ::= [ <monop> ] <e3>
        #    <e3> ::= '(' <expression> ')' | <constant> | 'P'<integer> | 'Q'<integer> | 'I'<integer> | 'M' <integer>
        #                  | <mathop><float>
        #    <sumop> ::= '+' | '-' | '|' | '^'
        #    <multop> ::= '*' | '/' | '%' | '&'
        #    <monop> ::= '+' | '-'
        #    <mathop> ::= 'SIN' | 'COS' | 'TAB' | 'ASIN' | 'ACOS' | 'ATAN' | 'ATAN2'
        #                  | 'SQRT' | 'ABS' | 'EXT' | 'IN' | 'LN'
        result = self.parseE1()
        going = True
        while going:
            t = self.lexer.get_token()
            if t == '+':
                result = result + self.parseE1()
            elif t == '-':
                result = result - self.parseE1()
            elif t == '|':
                result = float(int(result) | int(self.parseE1()))
            elif t == '^':
                result = float(int(result) ^ int(self.parseE1()))
            else:
                self.lexer.put_token(t)
                going = False
        return result

    def parseE1(self):
        """Return the result of a sub-expression containing multiplicative operands."""
        result = self.parseE2()
        going = True
        while going:
            t = self.lexer.get_token()
            if t == '*':
                result = result * self.parseE2()
            elif t == '/':
                result = result / self.parseE2()
            elif t == '%':
                result = result % self.parseE2()
            elif t == '&':
                result = float(int(result) & int(self.parseE2()))
            else:
                self.lexer.put_token(t)
                going = False
        return result

    def parseE2(self):
        """Return the result of a sub-expression containing monadic operands."""
        monop = self.lexer.get_token()
        if monop not in ['+', '-']:
            self.lexer.put_token(monop)
            monop = '+'
        result = self.parseE3()
        if monop == '-':
            result = -result
        return result

    def parseE3(self):
        """Return the result of a sub-expression that is an I,P,Q or M variable or
           a constant or a parenthesised expression, or a mathematical operation."""
        t = self.lexer.get_token()
        if t == '(':
            result = self.parseExpression()
            t = self.lexer.get_token(')')
        elif t == 'Q':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = self.variable_dict.get_q_variable(value)
        elif t == 'P':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = self.variable_dict.get_p_variable(value)
        elif t == 'I':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = self.variable_dict.get_i_variable(value)
        elif t == 'M':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = self.variable_dict.get_m_variable(value)
        elif t == 'SIN':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            I15 = self.variable_dict.get_i_variable(15)
            if I15 == 0:
                value = radians(value)
            result = sin(value)
        elif t == 'COS':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            I15 = self.variable_dict.get_i_variable(15)
            if I15 == 0:
                value = radians(value)
            result = cos(value)
        elif t == 'TAN':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            I15 = self.variable_dict.get_i_variable(15)
            if I15 == 0:
                value = radians(value)
            result = tan(value)
        elif t == 'ASIN':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = asin(value)
            I15 = self.variable_dict.get_i_variable(15)
            if I15 == 0:
                result = degrees(result)
        elif t == 'ACOS':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = acos(value)
            I15 = self.variable_dict.get_i_variable(15)
            if I15 == 0:
                result = degrees(result)
        elif t == 'ATAN':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = atan(value)
            I15 = self.variable_dict.get_i_variable(15)
            if I15 == 0:
                result = degrees(result)
        elif t == 'ATAN2':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t

            # PMAC uses the value in Q0 as the cosine argument
            Q0 = self.variable_dict.get_q_variable(0)

            result = atan2(value, Q0)
            I15 = self.variable_dict.get_i_variable(15)
            if I15 == 0:
                result = degrees(result)
        elif t == 'SQRT':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = sqrt(value)
        elif t == 'ABS':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = abs(value)
        elif t == 'EXP':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = exp(value)
        elif t == 'INT':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = int(value)
        elif t == 'LN':
            t = self.lexer.get_token()
            if t == '(':
                value = self.parseExpression()
                t = self.lexer.get_token(')')
            else:
                value = t
            result = log(value)
        else:
            result = t.to_float()
        return result
