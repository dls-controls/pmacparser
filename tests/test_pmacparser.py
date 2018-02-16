import unittest
from math import sqrt, exp, log

from pmacparser.pmac_parser import PMACParser


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

    def test_int_neg(self):

        input_dict = {"P32": -10.244}

        lines = []
        lines.append("Q3=INT(P32)")

        parser = PMACParser(lines)

        output_dict = parser.parse(input_dict)

        self.assertEqual(len(output_dict), 2)
        self.assertEqual(output_dict["P32"], -10.244)
        self.assertEqual(output_dict["Q3"], -10)

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
        lines.append("ENDIF")
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

    def test_float_expected_exception(self):

        input_dict = {"Q1": 42}

        lines = []
        lines.append("Q1=ENDIF")

        parser = PMACParser(lines)

        self.assertRaises(Exception, parser.parse, input_dict)


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

if __name__ == "__main__":
    unittest.main(2)
