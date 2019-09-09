import unittest
from math import sqrt, exp, log

import numpy as np

from pmacparser.pmac_parser import PMACParser, ParserError


class TestParser(unittest.TestCase):

    def test_QP(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=P1")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["Q1"], 42)

    def test_QP2(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("P(1)=Q(1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["Q1"], 42)

    def test_QP3(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q(1)=P(1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["Q1"], 42)

    def test_IM(self):

        input_dict = {"I1": 42}

        lines = []
        lines.append("M1=I1")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["I1"], 42)
        self.assertEqual(output_dict["M1"], 42)

    def test_IM2(self):

        input_dict = {"M1": 42}

        lines = []
        lines.append("I(1)=M(1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["I1"], 42)
        self.assertEqual(output_dict["M1"], 42)

    def test_float(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("Q1=56.254")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 1)
        self.assertEqual(output_dict["Q1"], 56.254)

    def test_add(self):

        input_dict = {"P1": 42, "P2": 9}

        lines = []
        lines.append("Q1=P1+P2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 9)
        self.assertEqual(output_dict["Q1"], 51)

    def test_subtraction(self):

        input_dict = {"P1": 5.5, "P2": 3}

        lines = []
        lines.append("P3=P1-P2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 5.5)
        self.assertEqual(output_dict["P2"], 3)
        self.assertEqual(output_dict["P3"], 2.5)

    def test_subtraction_negative(self):

        input_dict = {"P1": 5, "P2": 11}

        lines = []
        lines.append("P3=P1-P2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 5)
        self.assertEqual(output_dict["P2"], 11)
        self.assertEqual(output_dict["P3"], -6)

    def test_multiply(self):

        input_dict = {"Q1": 3, "P2": 22}

        lines = []
        lines.append("I1=Q1*P2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["Q1"], 3)
        self.assertEqual(output_dict["P2"], 22)
        self.assertEqual(output_dict["I1"], 66)

    def test_divide(self):

        input_dict = {"I1": 22, "Q5": 7}

        lines = []
        lines.append("P99=I1/Q5")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["I1"], 22)
        self.assertEqual(output_dict["Q5"], 7)
        self.assertEqual(output_dict["P99"], 22/7.0)

    def test_multiply_precedence1(self):

        input_dict = {}

        lines = []
        lines.append("Q1=3+4*5")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 1)
        self.assertEqual(output_dict["Q1"], 23)

    def test_multiply_precedence2(self):

        input_dict = {}

        lines = []
        lines.append("P1=3*4+5")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 1)
        self.assertEqual(output_dict["P1"], 17)

    def test_multiply_precedence3(self):

        input_dict = {}

        lines = []
        lines.append("Q1=3+4*5+6")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 1)
        self.assertEqual(output_dict["Q1"], 29)

    def test_multiply_precedence4(self):

        input_dict = {}

        lines = []
        lines.append("Q1=2*3*4+5*6*7")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 1)
        self.assertEqual(output_dict["Q1"], 234)

    def test_divide_precedence1(self):

        input_dict = {}

        lines = []
        lines.append("Q1=3+20/5")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 1)
        self.assertEqual(output_dict["Q1"], 7)

    def test_divide_precedence2(self):

        input_dict = {}

        lines = []
        lines.append("P1=8/4+5")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 1)
        self.assertEqual(output_dict["P1"], 7)

    def test_divide_precedence3(self):

        input_dict = {}

        lines = []
        lines.append("P1=16/4+5/5")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 1)
        self.assertEqual(output_dict["P1"], 5)

    def test_parenthesis_precedence(self):

        input_dict = {}

        lines = []
        lines.append("Q1=2*3*(4+5)*6*7")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 1)
        self.assertEqual(output_dict["Q1"], 2268)

    def test_mod(self):

        input_dict = {"P1": 8}

        lines = []
        lines.append("Q1=P1%3")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 8)
        self.assertEqual(output_dict["Q1"], 2)

    def test_bitand(self):

        input_dict = {"P1": 54254323}

        lines = []
        lines.append("Q1=P1&213411")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 54254323)
        self.assertEqual(output_dict["Q1"], 213155)

    def test_bitor(self):

        input_dict = {"P1": 54254323}

        lines = []
        lines.append("Q1=P1|213411")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 54254323)
        self.assertEqual(output_dict["Q1"], 54254579)

    def test_bitxor(self):

        input_dict = {"P1": 54254323}

        lines = []
        lines.append("Q1=P1^213411")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 54254323)
        self.assertEqual(output_dict["Q1"], 54041424)

    def test_abs(self):

        input_dict = {"P1": -3}

        lines = []
        lines.append("Q1=ABS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], -3)
        self.assertEqual(output_dict["Q1"], 3)

    def test_abs2(self):

        input_dict = {"P1": 4.5}

        lines = []
        lines.append("Q1=ABS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 4.5)
        self.assertEqual(output_dict["Q1"], 4.5)

    def test_int(self):

        input_dict = {"P32": 3.141}

        lines = []
        lines.append("Q3=INT(P32)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P32"], 3.141)
        self.assertEqual(output_dict["Q3"], 3)

    def test_int_2(self):

        input_dict = {"P32": 3.6}

        lines = []
        lines.append("Q3=INT(P32)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P32"], 3.6)
        self.assertEqual(output_dict["Q3"], 3)

    def test_int_neg(self):

        input_dict = {"P32": -10.244}

        lines = []
        lines.append("Q3=INT(P32)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P32"], -10.244)
        self.assertEqual(output_dict["Q3"], -11)

    def test_int_neg_2(self):

        input_dict = {"P32": -3.6}

        lines = []
        lines.append("Q3=INT(P32)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P32"], -3.6)
        self.assertEqual(output_dict["Q3"], -4)

    def test_sqrt(self):

        input_dict = {"P45": 25}

        lines = []
        lines.append("Q2=SQRT(P45)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P45"], 25)
        self.assertEqual(output_dict["Q2"], 5)

    def test_sqrt2(self):

        input_dict = {"P2": 2}

        lines = []
        lines.append("Q2=SQRT(P2)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P2"], 2)
        self.assertEqual(output_dict["Q2"], sqrt(2))

    def test_exp(self):

        input_dict = {"P1": 33}

        lines = []
        lines.append("Q1=EXP(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 33)
        self.assertEqual(output_dict["Q1"], exp(33))

    def test_ln(self):

        input_dict = {"P1": 33}

        lines = []
        lines.append("Q1=LN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 33)
        self.assertEqual(output_dict["Q1"], log(33))

    def test_sin_deg(self):

        input_dict = {"P1": 30}

        lines = []
        lines.append("Q1=SIN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 30)
        self.assertAlmostEqual(output_dict["Q1"], 0.5)

    def test_sin_rad(self):

        input_dict = {"P1": 30, "I15": 1}

        lines = []
        lines.append("Q1=SIN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 30)
        self.assertAlmostEqual(output_dict["Q1"], -0.988031624)
        self.assertEqual(output_dict["I15"], 1)

    def test_cos_deg(self):

        input_dict = {"P1": 60}

        lines = []
        lines.append("Q1=COS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 60)
        self.assertAlmostEqual(output_dict["Q1"], 0.5)

    def test_cos_rad(self):

        input_dict = {"P1": 60, "I15": 1}

        lines = []
        lines.append("Q1=COS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 60)
        self.assertAlmostEqual(output_dict["Q1"], -0.95241298)
        self.assertEqual(output_dict["I15"], 1)

    def test_tan_deg(self):

        input_dict = {"P1": 60}

        lines = []
        lines.append("Q1=TAN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 60)
        self.assertAlmostEqual(output_dict["Q1"], 1.732050808)

    def test_tan_rad(self):

        input_dict = {"P1": 60, "I15": 1}

        lines = []
        lines.append("Q1=TAN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 60)
        self.assertAlmostEqual(output_dict["Q1"], 0.320040389)
        self.assertEqual(output_dict["I15"], 1)

    def test_asin_deg(self):

        input_dict = {"P1": 0.5}

        lines = []
        lines.append("Q1=ASIN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 0.5)
        self.assertAlmostEqual(output_dict["Q1"], 30)

    def test_asin_rad(self):

        input_dict = {"P1": 0.5, "I15": 1}

        lines = []
        lines.append("Q1=ASIN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 0.5)
        self.assertAlmostEqual(output_dict["Q1"], 0.523598776)
        self.assertEqual(output_dict["I15"], 1)

    def test_acos_deg(self):

        input_dict = {"P1": 0.5}

        lines = []
        lines.append("Q1=ACOS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 0.5)
        self.assertAlmostEqual(output_dict["Q1"], 60)

    def test_acos_rad(self):

        input_dict = {"P1": 0.5, "I15": 1}

        lines = []
        lines.append("Q1=ACOS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 0.5)
        self.assertAlmostEqual(output_dict["Q1"], 1.047197551)
        self.assertEqual(output_dict["I15"], 1)

    def test_atan_deg(self):

        input_dict = {"P1": 0.5}

        lines = []
        lines.append("Q1=ATAN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"], 0.5)
        self.assertAlmostEqual(output_dict["Q1"], 26.565051177)

    def test_atan_rad(self):

        input_dict = {"P1": 0.5, "I15": 1}

        lines = []
        lines.append("Q1=ATAN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 0.5)
        self.assertAlmostEqual(output_dict["Q1"], 0.463647609)
        self.assertEqual(output_dict["I15"], 1)

    def test_atan2_deg(self):

        input_dict = {"P1": 0.5, "Q0": 2}

        lines = []
        lines.append("Q1=ATAN2(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 0.5)
        self.assertAlmostEqual(output_dict["Q1"], 14.036243467934)
        self.assertEqual(output_dict["Q0"], 2)

    def test_atan2_rad(self):

        input_dict = {"P1": 0.5, "I15": 1, "Q0": 2}

        lines = []
        lines.append("Q1=ATAN2(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 0.5)
        self.assertAlmostEqual(output_dict["Q1"], 0.244978663127)
        self.assertEqual(output_dict["I15"], 1)
        self.assertEqual(output_dict["Q0"], 2)

    def test_return(self):
        input_dict = {"P1": 42, "P2": 9}

        lines = []
        lines.append("Q1=P1+P2")
        lines.append("RETURN")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 9)
        self.assertEqual(output_dict["Q1"], 51)

    def test_ret(self):
        input_dict = {"P1": 42, "P2": 9}

        lines = []
        lines.append("Q1=P1+P2")
        lines.append("RET")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 9)
        self.assertEqual(output_dict["Q1"], 51)

    def test_multi_line(self):

        input_dict = {"P1": 42, "P2": 9}

        lines = []
        lines.append("Q1=P1+P2")
        lines.append("Q2=Q1+6")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 9)
        self.assertEqual(output_dict["Q1"], 51)
        self.assertEqual(output_dict["Q2"], 57)

    def test_if(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=42)")
        lines.append("P2=222")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_endi(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=42)")
        lines.append("P2=222")
        lines.append("ENDI")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_false(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=43)")
        lines.append("P2=222")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_else(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=42)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_else(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_not_equal_true(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1!=40)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_not_equal_false(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1!=42)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_gt_true(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1>40)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_gt_false(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1>42)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_not_gt_true(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1!>42)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_not_gt_false(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1!>41)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_lt_true(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1<43)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_lt_false(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1<42)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_not_lt_true(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1!<42)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_not_lt_false(self):

        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1!<43)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_if_and_inline_true(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1ANDI1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_and_inline_false1(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=2ANDI1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_and_inline_false2(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1ANDI1=2)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_and_inline_false3(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=2ANDI1=2)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_or_inline_true(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1ORI1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_or_inline_false1(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=2ORI1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_or_inline_false2(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1ORI1=2)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_or_inline_false3(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=2ORI1=2)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_and_newline_true(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1)")
        lines.append("AND(I1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_and_newline_false1(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=2)")
        lines.append("AND(I1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_and_newline_false2(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1)")
        lines.append("AND(I1=2)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_and_newline_false3(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=2)")
        lines.append("AND(I1=2)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_or_newline_true(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1)")
        lines.append("OR(I1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_or_newline_false1(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=2)")
        lines.append("OR(I1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_or_newline_false2(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1)")
        lines.append("OR(I1=2)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_or_newline_false3(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=2)")
        lines.append("OR(I1=2)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_andor_precedence(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=2)")
        lines.append("OR(I1=2)")
        lines.append("AND(P1=1)")
        lines.append("OR(I1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_nested1(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")

        lines.append("IF(P1=1)")
        lines.append("P2=222")
        # The nested if
        lines.append("IF(I1=1)")
        lines.append("P6=666")
        lines.append("ELSE")
        lines.append("P7=777")
        lines.append("ENDIF")
        # End of nested if
        lines.append("P4=444")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("P5=555")
        lines.append("ENDIF")

        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 7)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["P4"], 444)
        self.assertEqual(output_dict["P6"], 666)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_nested2(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")

        lines.append("IF(P1=1)")
        lines.append("P2=222")
        # The nested if
        lines.append("IF(I1=2)")
        lines.append("P6=666")
        lines.append("ELSE")
        lines.append("P7=777")
        lines.append("ENDIF")
        # End of nested if
        lines.append("P4=444")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("P5=555")
        lines.append("ENDIF")

        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 7)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["P4"], 444)
        self.assertEqual(output_dict["P7"], 777)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_nested3(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")

        lines.append("IF(P1=2)")
        lines.append("P2=222")
        # The nested if
        lines.append("IF(I1=1)")
        lines.append("P6=666")
        lines.append("ELSE")
        lines.append("P7=777")
        lines.append("ENDIF")
        # End of nested if
        lines.append("P4=444")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("P5=555")
        lines.append("ENDIF")

        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 6)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["P5"], 555)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_nested4(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")

        lines.append("IF(P1=2)")
        lines.append("P2=222")
        lines.append("P4=444")
        lines.append("ELSE")
        lines.append("P3=333")
        # The nested if
        lines.append("IF(I1=1)")
        lines.append("P6=666")
        lines.append("ELSE")
        lines.append("P7=777")
        lines.append("ENDIF")
        # End of nested if
        lines.append("P5=555")
        lines.append("ENDIF")

        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 7)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["P5"], 555)
        self.assertEqual(output_dict["P6"], 666)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_nested5(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")

        lines.append("IF(P1=2)")
        lines.append("P2=222")
        lines.append("P4=444")
        lines.append("ELSE")
        lines.append("P3=333")
        # The nested if
        lines.append("IF(I1=2)")
        lines.append("P6=666")
        lines.append("ELSE")
        lines.append("P7=777")
        lines.append("ENDIF")
        # End of nested if
        lines.append("P5=555")
        lines.append("ENDIF")

        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 7)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["P5"], 555)
        self.assertEqual(output_dict["P7"], 777)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_if_nested6(self):

        input_dict = {"P1": 1, "I1": 1}

        lines = []
        lines.append("Q1=1")

        lines.append("IF(P1=1)")
        lines.append("P2=222")
        lines.append("P4=444")
        lines.append("ELSE")
        lines.append("P3=333")
        # The nested if
        lines.append("IF(I1=1)")
        lines.append("P6=666")
        lines.append("ELSE")
        lines.append("P7=777")
        lines.append("ENDI")
        # End of nested if
        lines.append("P5=555")
        lines.append("ENDIF")

        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 6)
        self.assertEqual(output_dict["P1"], 1)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["P4"], 444)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)
        self.assertEqual(output_dict["I1"], 1)

    def test_while(self):

        input_dict = {"P1": 1, "P2": 2}

        lines = []
        lines.append("Q1=1")
        lines.append("Q2=2")
        lines.append("Q1=Q1+1")
        lines.append("WHILE(P1<10)")
        lines.append("P1=P1+1")
        lines.append("P2=P2+2")
        lines.append("ENDWHILE")
        lines.append("Q2=Q2+1")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 10)
        self.assertEqual(output_dict["P2"], 20)
        self.assertEqual(output_dict["Q1"], 2)
        self.assertEqual(output_dict["Q2"], 3)

    def test_while_endw(self):

        input_dict = {"P1": 1, "P2": 2}

        lines = []
        lines.append("Q1=1")
        lines.append("Q2=2")
        lines.append("Q1=Q1+1")
        lines.append("WHILE(P1<10)")
        lines.append("P1=P1+1")
        lines.append("P2=P2+2")
        lines.append("ENDW")
        lines.append("Q2=Q2+1")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 10)
        self.assertEqual(output_dict["P2"], 20)
        self.assertEqual(output_dict["Q1"], 2)
        self.assertEqual(output_dict["Q2"], 3)

    def test_while_nested(self):

        input_dict = {"P1": 1, "P2": 2, "P3": 0, "P4": 0}

        lines = []
        lines.append("Q1=1")
        lines.append("Q2=2")
        lines.append("Q1=Q1+1")
        lines.append("WHILE(P1<10)")
        lines.append("P1=P1+1")
        # Nested while
        lines.append("P3=0")
        lines.append("WHILE(P3<5)")
        lines.append("P3=P3+1")
        lines.append("P4=P4+2")
        lines.append("ENDWHILE")
        # End nested while
        lines.append("P2=P2+2")
        lines.append("ENDWHILE")
        lines.append("Q2=Q2+1")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 6)
        self.assertEqual(output_dict["P1"], 10)
        self.assertEqual(output_dict["P2"], 20)
        self.assertEqual(output_dict["P3"], 5)
        self.assertEqual(output_dict["P4"], 90)
        self.assertEqual(output_dict["Q1"], 2)
        self.assertEqual(output_dict["Q2"], 3)

    def test_parser_error(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("Q1=6")
        lines.append("TAN")

        parser = PMACParser(lines)

        self.assertRaises(Exception, parser.parse, input_dict)

    def test_unrecognised_token_exception(self):

        lines = []
        lines.append("Q1=5G+3")

        self.assertRaises(Exception, PMACParser, lines)

    def test_float_expected_error(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("IAND=Q1")

        parser = PMACParser(lines)

        self.assertRaises(ParserError, parser.parse, input_dict)

    def test_unexpected_i_error(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("Q1=ENDIF")

        parser = PMACParser(lines)

        self.assertRaises(Exception, parser.parse, input_dict)

    def test_bad_comparitor_error(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("IF(Q1COS44)")

        parser = PMACParser(lines)

        self.assertRaises(ParserError, parser.parse, input_dict)

    def test_bad_unclosed_bracket_error(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("IF(Q1>44COS(3)")

        parser = PMACParser(lines)

        self.assertRaises(ParserError, parser.parse, input_dict)

    def test_unexpected_endif_error(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("Q1=3")
        lines.append("ENDIF")
        lines.append("Q1=4")

        parser = PMACParser(lines)

        self.assertRaises(ParserError, parser.parse, input_dict)

    def test_unexpected_else_error(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("Q1=3")
        lines.append("ELSE")
        lines.append("Q1=4")

        parser = PMACParser(lines)

        self.assertRaises(ParserError, parser.parse, input_dict)

    def test_unexpected_endwhile_error(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("Q1=3")
        lines.append("ENDWHILE")
        lines.append("Q1=4")

        parser = PMACParser(lines)

        self.assertRaises(ParserError, parser.parse, input_dict)


    def test_multiple_runs(self):
        input_dict = {"P1": 42}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1=1)")
        lines.append("P2=222")
        lines.append("ELSE")
        lines.append("P3=333")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"], 42)
        self.assertEqual(output_dict["P3"], 333)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

        output_dict_2 = parser.parse(input_dict)

        self.assertEqual(len(output_dict_2), 4)
        self.assertEqual(output_dict_2["P1"], 42)
        self.assertEqual(output_dict_2["P3"], 333)
        self.assertEqual(output_dict_2["Q1"], 1)
        self.assertEqual(output_dict_2["Q2"], 2)

        input_dict = {"P1": 1}
        output_dict_3 = parser.parse(input_dict)

        self.assertEqual(len(output_dict_3), 4)
        self.assertEqual(output_dict_3["P1"], 1)
        self.assertEqual(output_dict_3["P2"], 222)
        self.assertEqual(output_dict_3["Q1"], 1)
        self.assertEqual(output_dict_3["Q2"], 2)

    def test_real_example1(self):

        input_dict = {"P5": 2, "P6": 4, "P4805": 8, "P4905": 16, "P4806": 32, "P4906": 64}

        lines = []
        lines.append("Q7=((P(4800+5)*P5+P(4900+5))+(P(4800+6)*P6+P(4900+6)))/2")
        lines.append("Q8=(P(4800+5)*P5+P(4900+5))-(P(4800+6)*P6+P(4900+6))")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 8)
        self.assertEqual(output_dict["P5"], 2)
        self.assertEqual(output_dict["P6"], 4)
        self.assertEqual(output_dict["P4805"], 8)
        self.assertEqual(output_dict["P4905"], 16)
        self.assertEqual(output_dict["P4806"], 32)
        self.assertEqual(output_dict["P4906"], 64)
        self.assertEqual(output_dict["Q7"], 112)
        self.assertEqual(output_dict["Q8"], -160)

    def test_real_example2(self):

        input_dict = {"P1": 21, "P2": 21.5, "P3": 22, "P4": 22.5, "P5": 23, "P6": 23.5, "P7": 24, "P8": 24.5,
                      "P17": 26, "P4801": 1, "P4802": 2, "P4803": 3, "P4804": 4, "P4805": 5, "P4806": 6, "P4807": 7,
                      "P4808": 8, "P4817": 9, "P4901": 10, "P4902": 11, "P4903": 12, "P4904": 13, "P4905": 14,
                      "P4906": 15, "P4907": 16, "P4908": 17, "P4917": 18, "Q21": 31, "Q22": 32, "Q23": 33, "Q24": 34,
                      "Q25": 35, "Q26": 36, "Q27": 37, "Q28": 38, "Q29": 3900, "Q30": 40}

        lines = []
        lines.append("Q1=(P(4800+1)*P1+P(4900+1))")
        lines.append("Q5=(P(4800+2)*P2+P(4900+2))")
        lines.append("Q9=(P(4800+7)*P7+P(4900+7))")
        lines.append("IF(Q27=0)")
        lines.append("Q2=(P(4800+3)*P3+P(4900+3))")
        lines.append("Q3=(P(4800+5)*P5+P(4900+5))")
        lines.append("Q4=(P(4800+3)*P3+P(4900+3))+(P(4800+8)*P8+P(4900+8))")
        lines.append("Q6=(P(4800+4)*P4+P(4900+4))")
        lines.append("Q7=(P(4800+6)*P6+P(4900+6))")
        lines.append("Q8=(P(4800+4)*P4+P(4900+4))+(P(4800+17)*P17+P(4900+17))")
        lines.append("ELSE")
        lines.append("Q130=SQRT((Q24+Q29)*(Q24+Q29)-(Q28+(P(4800+17)*P17+P(4900+17))-Q30)*"
                     "(Q28+(P(4800+17)*P17+P(4900+17))-Q30))")
        lines.append("Q128=TAN(Q26)*(Q130+Q21)")
        lines.append("Q131=(P(4800+3)*P3+P(4900+3))-(P(4800+1)*P1+P(4900+1))-Q128")
        lines.append("Q6=(ATAN(Q131/(Q130+Q22))+Q26)/2")
        lines.append("Q133=(P(4800+5)*P5+P(4900+5))-(P(4800+1)*P1+P(4900+1))-Q128")
        lines.append("Q7=(ATAN(Q133/(Q130+Q23))+Q26)/2")
        lines.append("Q4=(P(4800+1)*P1+P(4900+1))+(P(4800+8)*P8+P(4900+8))")
        lines.append("Q129=TAN(Q25)*(Q130+Q21)")
        lines.append("Q132=(P(4800+4)*P4+P(4900+4))-(P(4800+2)*P2+P(4900+2))-Q129")
        lines.append("Q2=(ATAN(Q132/(Q130+Q22))+Q25)/2")
        lines.append("Q134=(P(4800+6)*P6+P(4900+6))-(P(4800+2)*P2+P(4900+2))-Q129")
        lines.append("Q3=(ATAN(Q134/(Q130+Q23))+Q25)/2")
        lines.append("Q8=(P(4800+2)*P2+P(4900+2))+(P(4800+17)*P17+P(4900+17))")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 53)

        self.assertEqual(output_dict["P1"], 21)
        self.assertEqual(output_dict["P2"], 21.5)
        self.assertEqual(output_dict["P3"], 22)
        self.assertEqual(output_dict["P4"], 22.5)
        self.assertEqual(output_dict["P5"], 23)
        self.assertEqual(output_dict["P6"], 23.5)
        self.assertEqual(output_dict["P7"], 24)
        self.assertEqual(output_dict["P8"], 24.5)

        self.assertEqual(output_dict["P17"], 26)
        self.assertEqual(output_dict["P4801"], 1)
        self.assertEqual(output_dict["P4802"], 2)
        self.assertEqual(output_dict["P4803"], 3)
        self.assertEqual(output_dict["P4804"], 4)
        self.assertEqual(output_dict["P4805"], 5)
        self.assertEqual(output_dict["P4806"], 6)
        self.assertEqual(output_dict["P4807"], 7)

        self.assertEqual(output_dict["P4808"], 8)
        self.assertEqual(output_dict["P4817"], 9)
        self.assertEqual(output_dict["P4901"], 10)
        self.assertEqual(output_dict["P4902"], 11)
        self.assertEqual(output_dict["P4903"], 12)
        self.assertEqual(output_dict["P4904"], 13)
        self.assertEqual(output_dict["P4905"], 14)

        self.assertEqual(output_dict["P4906"], 15)
        self.assertEqual(output_dict["P4907"], 16)
        self.assertEqual(output_dict["P4908"], 17)
        self.assertEqual(output_dict["P4917"], 18)
        self.assertEqual(output_dict["Q21"], 31)
        self.assertEqual(output_dict["Q22"], 32)
        self.assertEqual(output_dict["Q23"], 33)
        self.assertEqual(output_dict["Q24"], 34)

        self.assertEqual(output_dict["Q25"], 35)
        self.assertEqual(output_dict["Q26"], 36)
        self.assertEqual(output_dict["Q27"], 37)
        self.assertEqual(output_dict["Q28"], 38)
        self.assertEqual(output_dict["Q29"], 3900)
        self.assertEqual(output_dict["Q30"], 40)

        self.assertEqual(output_dict["Q1"], 31)
        self.assertEqual(output_dict["Q5"], 54)
        self.assertEqual(output_dict["Q9"], 184)
        self.assertAlmostEqual(output_dict["Q130"], 3926.048395015)
        self.assertAlmostEqual(output_dict["Q128"], 2874.963944354)
        self.assertAlmostEqual(output_dict["Q131"], -2827.963944354)
        self.assertAlmostEqual(output_dict["Q6"], 0.227391949)
        self.assertAlmostEqual(output_dict["Q133"], -2776.963944354)
        self.assertAlmostEqual(output_dict["Q7"], 0.476666233)
        self.assertEqual(output_dict["Q4"], 244)
        self.assertAlmostEqual(output_dict["Q129"], 2770.75511525)
        self.assertAlmostEqual(output_dict["Q132"], -2721.75511525)
        self.assertAlmostEqual(output_dict["Q2"], 0.242805324)
        self.assertAlmostEqual(output_dict["Q134"], -2668.75511525)
        self.assertAlmostEqual(output_dict["Q3"], 0.508241199)
        self.assertEqual(output_dict["Q8"], 306)

    def test_numpy_add(self):
        p1 = np.array([1, 2, 3, 4])

        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=P1+4")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 1)
        self.assertEqual(output_dict["P1"][1], 2)
        self.assertEqual(output_dict["P1"][2], 3)
        self.assertEqual(output_dict["P1"][3], 4)
        self.assertEqual(output_dict["Q1"][0], 5)
        self.assertEqual(output_dict["Q1"][1], 6)
        self.assertEqual(output_dict["Q1"][2], 7)
        self.assertEqual(output_dict["Q1"][3], 8)

    def test_numpy_subtract(self):
        p1 = np.array([10, 20, 30])
        p2 = np.array([1, 2, 3])

        input_dict = {"P1": p1, "P2": p2}

        lines = []
        lines.append("Q1=P1-P2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 10)
        self.assertEqual(output_dict["P1"][1], 20)
        self.assertEqual(output_dict["P1"][2], 30)
        self.assertEqual(output_dict["P2"][0], 1)
        self.assertEqual(output_dict["P2"][1], 2)
        self.assertEqual(output_dict["P2"][2], 3)
        self.assertEqual(output_dict["Q1"][0], 9)
        self.assertEqual(output_dict["Q1"][1], 18)
        self.assertEqual(output_dict["Q1"][2], 27)

    def test_numpy_multiply(self):
        p1 = np.array([1, 2, 3, 4])

        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=P1*3")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 1)
        self.assertEqual(output_dict["P1"][1], 2)
        self.assertEqual(output_dict["P1"][2], 3)
        self.assertEqual(output_dict["P1"][3], 4)
        self.assertEqual(output_dict["Q1"][0], 3)
        self.assertEqual(output_dict["Q1"][1], 6)
        self.assertEqual(output_dict["Q1"][2], 9)
        self.assertEqual(output_dict["Q1"][3], 12)

    def test_numpy_divide(self):
        p1 = np.array([10, 20, 30])
        p2 = np.array([2, 3, 4])

        input_dict = {"P1": p1, "P2": p2}

        lines = []
        lines.append("Q1=P1/P2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 10)
        self.assertEqual(output_dict["P1"][1], 20)
        self.assertEqual(output_dict["P1"][2], 30)
        self.assertEqual(output_dict["P2"][0], 2)
        self.assertEqual(output_dict["P2"][1], 3)
        self.assertEqual(output_dict["P2"][2], 4)
        self.assertEqual(output_dict["Q1"][0], 5)
        self.assertAlmostEqual(output_dict["Q1"][1], 6.666666666)
        self.assertAlmostEqual(output_dict["Q1"][2], 7.5)

    def test_numpy_mod(self):
        p1 = np.array([8, 13])

        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=P1%3")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 8)
        self.assertEqual(output_dict["P1"][1], 13)
        self.assertEqual(output_dict["Q1"][0], 2)
        self.assertEqual(output_dict["Q1"][1], 1)

    def test_numpy_bitand(self):
        p1 = np.array([54254323, 92364])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=P1&213411")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 54254323)
        self.assertEqual(output_dict["P1"][1], 92364)
        self.assertEqual(output_dict["Q1"][0], 213155)
        self.assertEqual(output_dict["Q1"][1], 82048)

    def test_numpy_bitor(self):
        p1 = np.array([54254323, 92364])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=P1|213411")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 54254323)
        self.assertEqual(output_dict["P1"][1], 92364)
        self.assertEqual(output_dict["Q1"][0], 54254579)
        self.assertEqual(output_dict["Q1"][1], 223727)

    def test_numpy_bitxor(self):
        p1 = np.array([54254323, 92364])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=P1^213411")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 54254323)
        self.assertEqual(output_dict["P1"][1], 92364)
        self.assertEqual(output_dict["Q1"][0], 54041424)
        self.assertEqual(output_dict["Q1"][1], 141679)

    def test_numpy_abs(self):
        p1 = np.array([-3, 45])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=ABS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], -3)
        self.assertEqual(output_dict["P1"][1], 45)
        self.assertEqual(output_dict["Q1"][0], 3)
        self.assertEqual(output_dict["Q1"][1], 45)

    def test_numpy_int(self):
        p32 = np.array([3.141, -45.39])
        input_dict = {"P32": p32}

        lines = []
        lines.append("Q3=INT(P32)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P32"][0], 3.141)
        self.assertEqual(output_dict["P32"][1], -45.39)
        self.assertEqual(output_dict["Q3"][0], 3)
        self.assertEqual(output_dict["Q3"][1], -46)

    def test_numpy_sqrt(self):
        p45 = np.array([25, 2])
        input_dict = {"P45": p45}

        lines = []
        lines.append("Q2=SQRT(P45)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P45"][0], 25)
        self.assertEqual(output_dict["P45"][1], 2)
        self.assertEqual(output_dict["Q2"][0], 5)
        self.assertAlmostEqual(output_dict["Q2"][1], 1.414213562)

    def test_numpy_exp(self):
        p1 = np.array([33, 18])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=EXP(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 33)
        self.assertEqual(output_dict["P1"][1], 18)
        self.assertAlmostEqual(output_dict["Q1"][0], 214643579785916.06)
        self.assertAlmostEqual(output_dict["Q1"][1], 65659969.13733051)

    def test_numpy_ln(self):
        p1 = np.array([33, 18])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=LN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 33)
        self.assertEqual(output_dict["P1"][1], 18)
        self.assertAlmostEqual(output_dict["Q1"][0], 3.4965075614)
        self.assertAlmostEqual(output_dict["Q1"][1], 2.8903717578)

    def test_numpy_sin_deg(self):
        p1 = np.array([30, -66])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=SIN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 30)
        self.assertEqual(output_dict["P1"][1], -66)
        self.assertAlmostEqual(output_dict["Q1"][0], 0.5)
        self.assertAlmostEqual(output_dict["Q1"][1], -0.913545457)

    def test_numpy_sin_rad(self):
        p1 = np.array([30, -66])
        input_dict = {"P1": p1, "I15": 1}

        lines = []
        lines.append("Q1=SIN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 30)
        self.assertEqual(output_dict["P1"][1], -66)
        self.assertAlmostEqual(output_dict["Q1"][0], -0.988031624)
        self.assertAlmostEqual(output_dict["Q1"][1], 0.026551154)
        self.assertEqual(output_dict["I15"], 1)

    def test_numpy_cos_deg(self):
        p1 = np.array([60, -63])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=COS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 60)
        self.assertEqual(output_dict["P1"][1], -63)
        self.assertAlmostEqual(output_dict["Q1"][0], 0.5)
        self.assertAlmostEqual(output_dict["Q1"][1], 0.453990499)

    def test_numpy_cos_rad(self):
        p1 = np.array([60, -63])
        input_dict = {"P1": p1, "I15": 1}

        lines = []
        lines.append("Q1=COS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 60)
        self.assertEqual(output_dict["P1"][1], -63)
        self.assertAlmostEqual(output_dict["Q1"][0], -0.95241298)
        self.assertAlmostEqual(output_dict["Q1"][1], 0.985896581)
        self.assertEqual(output_dict["I15"], 1)

    def test_numpy_tan_deg(self):
        p1 = np.array([60, -63])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=TAN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 60)
        self.assertEqual(output_dict["P1"][1], -63)
        self.assertAlmostEqual(output_dict["Q1"][0], 1.732050808)
        self.assertAlmostEqual(output_dict["Q1"][1], -1.96261050)

    def test_numpy_tan_rad(self):
        p1 = np.array([60, -63])
        input_dict = {"P1": p1, "I15": 1}

        lines = []
        lines.append("Q1=TAN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 60)
        self.assertEqual(output_dict["P1"][1], -63)
        self.assertAlmostEqual(output_dict["Q1"][0], 0.320040389)
        self.assertAlmostEqual(output_dict["Q1"][1], -0.169749752)
        self.assertEqual(output_dict["I15"], 1)

    def test_numpy_asin_deg(self):
        p1 = np.array([0.5, -0.213])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=ASIN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 0.5)
        self.assertEqual(output_dict["P1"][1], -0.213)
        self.assertAlmostEqual(output_dict["Q1"][0], 30)
        self.assertAlmostEqual(output_dict["Q1"][1], -12.298218098055672)

    def test_numpy_asin_rad(self):
        p1 = np.array([0.5, -0.213])
        input_dict = {"P1": p1, "I15": 1}

        lines = []
        lines.append("Q1=ASIN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 0.5)
        self.assertEqual(output_dict["P1"][1], -0.213)
        self.assertAlmostEqual(output_dict["Q1"][0], 0.523598776)
        self.assertAlmostEqual(output_dict["Q1"][1], -0.214644397)
        self.assertEqual(output_dict["I15"], 1)

    def test_numpy_acos_deg(self):
        p1 = np.array([0.5, -0.213])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=ACOS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 0.5)
        self.assertEqual(output_dict["P1"][1], -0.213)
        self.assertAlmostEqual(output_dict["Q1"][0], 60)
        self.assertAlmostEqual(output_dict["Q1"][1], 102.298218098)

    def test_numpy_acos_rad(self):
        p1 = np.array([0.5, -0.213])
        input_dict = {"P1": p1, "I15": 1}

        lines = []
        lines.append("Q1=ACOS(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 0.5)
        self.assertEqual(output_dict["P1"][1], -0.213)
        self.assertAlmostEqual(output_dict["Q1"][0], 1.047197551)
        self.assertAlmostEqual(output_dict["Q1"][1], 1.7854407247)
        self.assertEqual(output_dict["I15"], 1)

    def test_numpy_atan_deg(self):
        p1 = np.array([0.5, -0.213])
        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=ATAN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P1"][0], 0.5)
        self.assertEqual(output_dict["P1"][1], -0.213)
        self.assertAlmostEqual(output_dict["Q1"][0], 26.565051177)
        self.assertAlmostEqual(output_dict["Q1"][1], -12.02430666)

    def test_numpy_atan_rad(self):
        p1 = np.array([0.5, -0.213])
        input_dict = {"P1": p1, "I15": 1}

        lines = []
        lines.append("Q1=ATAN(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 0.5)
        self.assertEqual(output_dict["P1"][1], -0.213)
        self.assertAlmostEqual(output_dict["Q1"][0], 0.463647609)
        self.assertAlmostEqual(output_dict["Q1"][1], -0.209863741)
        self.assertEqual(output_dict["I15"], 1)

    def test_numpy_atan2_deg(self):
        p1 = np.array([0.5, -0.213])
        input_dict = {"P1": p1, "Q0": 2}

        lines = []
        lines.append("Q1=ATAN2(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 0.5)
        self.assertEqual(output_dict["P1"][1], -0.213)
        self.assertAlmostEqual(output_dict["Q1"][0], 14.036243467934)
        self.assertAlmostEqual(output_dict["Q1"][1], -6.079086119)
        self.assertEqual(output_dict["Q0"], 2)

    def test_numpy_atan2_rad(self):
        p1 = np.array([0.5, -0.213])
        input_dict = {"P1": p1, "I15": 1, "Q0": 2}

        lines = []
        lines.append("Q1=ATAN2(P1)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"][0], 0.5)
        self.assertEqual(output_dict["P1"][1], -0.213)
        self.assertAlmostEqual(output_dict["Q1"][0], 0.244978663127)
        self.assertAlmostEqual(output_dict["Q1"][1], -0.106100068)
        self.assertEqual(output_dict["I15"], 1)
        self.assertEqual(output_dict["Q0"], 2)

    def test_numpy_if_all_true(self):

        p1 = np.array([42, 45])

        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1>40)")
        lines.append("P2=222")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 4)
        self.assertEqual(output_dict["P1"][0], 42)
        self.assertEqual(output_dict["P1"][1], 45)
        self.assertEqual(output_dict["P2"], 222)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_numpy_if_all_false(self):

        p1 = np.array([42, 45])

        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1<40)")
        lines.append("P2=222")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 3)
        self.assertEqual(output_dict["P1"][0], 42)
        self.assertEqual(output_dict["P1"][1], 45)
        self.assertEqual(output_dict["Q1"], 1)
        self.assertEqual(output_dict["Q2"], 2)

    def test_numpy_if_all_different(self):

        p1 = np.array([42, 45])

        input_dict = {"P1": p1}

        lines = []
        lines.append("Q1=1")
        lines.append("IF(P1<43)")
        lines.append("P2=222")
        lines.append("ENDIF")
        lines.append("Q2=2")

        parser = PMACParser(lines)

        self.assertRaises(Exception, parser.parse, input_dict)

    def test_numpy_while_all_true(self):

        p1 = np.array([20, 40])
        p3 = np.array([1, 1])

        input_dict = {"P1": p1, "P2": 2, "P3": p3}

        lines = []
        lines.append("Q1=1")
        lines.append("Q2=2")
        lines.append("Q1=Q1+1")
        lines.append("WHILE(P3<10)")
        lines.append("P1=P1+1")
        lines.append("P2=P2+2")
        lines.append("P3=P3+1")
        lines.append("ENDWHILE")
        lines.append("Q2=Q2+1")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 5)
        self.assertEqual(output_dict["P1"][0], 29)
        self.assertEqual(output_dict["P1"][1], 49)
        self.assertEqual(output_dict["P2"], 20)
        self.assertEqual(output_dict["P3"][0], 10)
        self.assertEqual(output_dict["P3"][1], 10)
        self.assertEqual(output_dict["Q1"], 2)
        self.assertEqual(output_dict["Q2"], 3)

    def test_numpy_while_different(self):

        p1 = np.array([20, 40])
        p3 = np.array([1, 2])

        input_dict = {"P1": p1, "P2": 2, "P3": p3}

        lines = []
        lines.append("Q1=1")
        lines.append("Q2=2")
        lines.append("Q1=Q1+1")
        lines.append("WHILE(P3<10)")
        lines.append("P1=P1+1")
        lines.append("P2=P2+2")
        lines.append("P3=P3+1")
        lines.append("ENDWHILE")
        lines.append("Q2=Q2+1")

        parser = PMACParser(lines)

        self.assertRaises(Exception, parser.parse, input_dict)

    def test_real_example2_numpy(self):

        p1 = np.array([21, 41])
        p2 = np.array([21.5, 41.5])
        p3 = np.array([22, 42])
        p4 = np.array([22.5, 42.5])
        p5 = np.array([23, 43])
        p6 = np.array([23.5, 43.5])
        p7 = np.array([24, 44])
        p8 = np.array([24.5, 44.5])
        p17 = np.array([26, 46])

        input_dict = {"P1": p1, "P2": p2, "P3": p3, "P4": p4, "P5": p5, "P6": p6, "P7": p7, "P8": p8,
                      "P17": p17, "P4801": 1, "P4802": 2, "P4803": 3, "P4804": 4, "P4805": 5, "P4806": 6, "P4807": 7,
                      "P4808": 8, "P4817": 9, "P4901": 10, "P4902": 11, "P4903": 12, "P4904": 13, "P4905": 14,
                      "P4906": 15, "P4907": 16, "P4908": 17, "P4917": 18, "Q21": 31, "Q22": 32, "Q23": 33, "Q24": 34,
                      "Q25": 35, "Q26": 36, "Q27": 37, "Q28": 38, "Q29": 3900, "Q30": 40}

        lines = []
        lines.append("Q1=(P(4800+1)*P1+P(4900+1))")
        lines.append("Q5=(P(4800+2)*P2+P(4900+2))")
        lines.append("Q9=(P(4800+7)*P7+P(4900+7))")
        lines.append("IF(Q27=0)")
        lines.append("Q2=(P(4800+3)*P3+P(4900+3))")
        lines.append("Q3=(P(4800+5)*P5+P(4900+5))")
        lines.append("Q4=(P(4800+3)*P3+P(4900+3))+(P(4800+8)*P8+P(4900+8))")
        lines.append("Q6=(P(4800+4)*P4+P(4900+4))")
        lines.append("Q7=(P(4800+6)*P6+P(4900+6))")
        lines.append("Q8=(P(4800+4)*P4+P(4900+4))+(P(4800+17)*P17+P(4900+17))")
        lines.append("ELSE")
        lines.append("Q130=SQRT((Q24+Q29)*(Q24+Q29)-(Q28+(P(4800+17)*P17+P(4900+17))-Q30)*"
                     "(Q28+(P(4800+17)*P17+P(4900+17))-Q30))")
        lines.append("Q128=TAN(Q26)*(Q130+Q21)")
        lines.append("Q131=(P(4800+3)*P3+P(4900+3))-(P(4800+1)*P1+P(4900+1))-Q128")
        lines.append("Q6=(ATAN(Q131/(Q130+Q22))+Q26)/2")
        lines.append("Q133=(P(4800+5)*P5+P(4900+5))-(P(4800+1)*P1+P(4900+1))-Q128")
        lines.append("Q7=(ATAN(Q133/(Q130+Q23))+Q26)/2")
        lines.append("Q4=(P(4800+1)*P1+P(4900+1))+(P(4800+8)*P8+P(4900+8))")
        lines.append("Q129=TAN(Q25)*(Q130+Q21)")
        lines.append("Q132=(P(4800+4)*P4+P(4900+4))-(P(4800+2)*P2+P(4900+2))-Q129")
        lines.append("Q2=(ATAN(Q132/(Q130+Q22))+Q25)/2")
        lines.append("Q134=(P(4800+6)*P6+P(4900+6))-(P(4800+2)*P2+P(4900+2))-Q129")
        lines.append("Q3=(ATAN(Q134/(Q130+Q23))+Q25)/2")
        lines.append("Q8=(P(4800+2)*P2+P(4900+2))+(P(4800+17)*P17+P(4900+17))")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 53)

        self.assertEqual(output_dict["P1"][0], 21)
        self.assertEqual(output_dict["P2"][0], 21.5)
        self.assertEqual(output_dict["P3"][0], 22)
        self.assertEqual(output_dict["P4"][0], 22.5)
        self.assertEqual(output_dict["P5"][0], 23)
        self.assertEqual(output_dict["P6"][0], 23.5)
        self.assertEqual(output_dict["P7"][0], 24)
        self.assertEqual(output_dict["P8"][0], 24.5)

        self.assertEqual(output_dict["P17"][0], 26)
        self.assertEqual(output_dict["P4801"], 1)
        self.assertEqual(output_dict["P4802"], 2)
        self.assertEqual(output_dict["P4803"], 3)
        self.assertEqual(output_dict["P4804"], 4)
        self.assertEqual(output_dict["P4805"], 5)
        self.assertEqual(output_dict["P4806"], 6)
        self.assertEqual(output_dict["P4807"], 7)

        self.assertEqual(output_dict["P4808"], 8)
        self.assertEqual(output_dict["P4817"], 9)
        self.assertEqual(output_dict["P4901"], 10)
        self.assertEqual(output_dict["P4902"], 11)
        self.assertEqual(output_dict["P4903"], 12)
        self.assertEqual(output_dict["P4904"], 13)
        self.assertEqual(output_dict["P4905"], 14)

        self.assertEqual(output_dict["P4906"], 15)
        self.assertEqual(output_dict["P4907"], 16)
        self.assertEqual(output_dict["P4908"], 17)
        self.assertEqual(output_dict["P4917"], 18)
        self.assertEqual(output_dict["Q21"], 31)
        self.assertEqual(output_dict["Q22"], 32)
        self.assertEqual(output_dict["Q23"], 33)
        self.assertEqual(output_dict["Q24"], 34)

        self.assertEqual(output_dict["Q25"], 35)
        self.assertEqual(output_dict["Q26"], 36)
        self.assertEqual(output_dict["Q27"], 37)
        self.assertEqual(output_dict["Q28"], 38)
        self.assertEqual(output_dict["Q29"], 3900)
        self.assertEqual(output_dict["Q30"], 40)

        self.assertEqual(output_dict["Q1"][0], 31)
        self.assertEqual(output_dict["Q5"][0], 54)
        self.assertEqual(output_dict["Q9"][0], 184)
        self.assertAlmostEqual(output_dict["Q130"][0], 3926.048395015)
        self.assertAlmostEqual(output_dict["Q128"][0], 2874.963944354)
        self.assertAlmostEqual(output_dict["Q131"][0], -2827.963944354)
        self.assertAlmostEqual(output_dict["Q6"][0], 0.227391949)
        self.assertAlmostEqual(output_dict["Q133"][0], -2776.963944354)
        self.assertAlmostEqual(output_dict["Q7"][0], 0.476666233)
        self.assertEqual(output_dict["Q4"][0], 244)
        self.assertAlmostEqual(output_dict["Q129"][0], 2770.75511525)
        self.assertAlmostEqual(output_dict["Q132"][0], -2721.75511525)
        self.assertAlmostEqual(output_dict["Q2"][0], 0.242805324)
        self.assertAlmostEqual(output_dict["Q134"][0], -2668.75511525)
        self.assertAlmostEqual(output_dict["Q3"][0], 0.508241199)
        self.assertEqual(output_dict["Q8"][0], 306)

        self.assertEqual(output_dict["Q1"][1], 51)
        self.assertEqual(output_dict["Q5"][1], 94)
        self.assertEqual(output_dict["Q9"][1], 324)
        self.assertAlmostEqual(output_dict["Q130"][1], 3910.42913246104)
        self.assertAlmostEqual(output_dict["Q128"][1], 2863.6158858522203)
        self.assertAlmostEqual(output_dict["Q131"][1], -2776.6158858522203)
        self.assertAlmostEqual(output_dict["Q6"][1], 0.4216611736089426)
        self.assertAlmostEqual(output_dict["Q133"][1], -2685.6158858522203)
        self.assertAlmostEqual(output_dict["Q7"][1], 0.8718703770225602)
        self.assertEqual(output_dict["Q4"][1], 424)
        self.assertAlmostEqual(output_dict["Q129"][1], 2759.8183898685766)
        self.assertAlmostEqual(output_dict["Q132"][1], -2670.8183898685766)
        self.assertAlmostEqual(output_dict["Q2"][1], 0.4420632778826068)
        self.assertAlmostEqual(output_dict["Q134"][1], -2577.8183898685766)
        self.assertAlmostEqual(output_dict["Q3"][1], 0.9136837164306968)
        self.assertEqual(output_dict["Q8"][1], 526)


if __name__ == "__main__":
    unittest.main(2)
