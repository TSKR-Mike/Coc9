import unittest
from ScienceExpressions import Root, Fraction


class TestRootClass(unittest.TestCase):
    def test_root_initialization(self):
        """测试根式初始化"""
        r = Root(8, 3)
        self.assertEqual(str(r), "2.0")  # 8的立方根=2

    def test_root_addition(self):
        """测试根式加法"""
        r1 = Root(2, 2, 2)  # 2√2
        r2 = Root(2, 2, 3)  # 3√2
        result = r1 + r2
        self.assertEqual(str(result), "5√2")


class TestFractionClass(unittest.TestCase):
    def test_fraction_simplify(self):
        """测试分数化简"""
        f = Fraction(4, 6)
        self.assertEqual(str(f), "2/3")

    def test_fraction_addition(self):
        """测试分数加法"""
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        result = f1 + f2
        self.assertEqual(str(result), "5/6")


from MathsCalculation import Calculation, turn_normal_expr_to_internal_expr, ReversedPolishNotation
import math
from decimal import Decimal


class TestMathExpressionParser(unittest.TestCase):

    # 基础运算测试
    def test_basic_operations(self):
        test_cases = [
            ('1 + 1', Decimal('2')),
            ('2 - 3', Decimal('-1')),
            ('4 * 5', Decimal('20')),
            ('6 / 2', Decimal('3')),
            ('2 ^ 3', Decimal('8')),
            ('(2 + 3) * 4', Decimal('20')),
            ('3 + 4 * 2', Decimal('11')),
            ('3 * (4 + 5)', Decimal('27')),
            ('10%', Decimal('0.1')),
            ('5!', Decimal('120')),
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                processed = turn_normal_expr_to_internal_expr(expr)
                result = Calculation(processed)
                self.assertEqual(result, expected)

    # 函数运算测试
    def test_functions(self):
        test_cases = [
            ('sin[0]', math.sin(0)),
            ('cos[0]', math.cos(0)),
            ('tan[0]', math.tan(0)),
            ('2log[8]', 3),
            ('ln[2.718281828]', 1),
            ('2√4', 2),
            ('3√27', 3),
            ('arcsin[0.5]', math.asin(0.5)),
            ('arccos[0.5]', math.acos(0.5)),
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                processed = turn_normal_expr_to_internal_expr(expr)
                print(processed)
                result = Calculation(processed)
                self.assertAlmostEqual(float(result), expected, delta=1e-9)


    # RPN转换测试
    def test_reversed_polish_notation(self):
        test_cases = [
            ('1 + 2 * 3', ['1', '2', '3', '*', '+']),
            ('(1 + 2) * 3', ['1', '2', '+', '3', '*']),
            ('2 ^ 3 ^ 2', ['2', '3', '2', '^', '^']),
            ('3 + 4 * 2 / (1 - 5)', ['3', '4', '2', '*', '1', '5', '-', '/', '+']),
        ]

        for expr, expected_rpn in test_cases:
            with self.subTest(expr=expr):
                processed = turn_normal_expr_to_internal_expr(expr).split()
                rpn = ReversedPolishNotation(processed)
                self.assertEqual(rpn, expected_rpn)

    # 格式转换测试
    def test_expression_formatting(self):
        test_cases = [
            ('1+2*3', '1 + 2 * 3'),
            ('(1+2)*3', ' ( 1 + 2 )  * 3'),
            ('-5+-3', ' - 5 + -3'),
            ('2√4', '2√4'),
            ('sin[30]', 'sin[30]'),
        ]

        for input_expr, expected in test_cases:
            with self.subTest(expr=input_expr):
                formatted = turn_normal_expr_to_internal_expr(input_expr)
                self.assertEqual(formatted, expected)

if __name__ == '__main__':
    unittest.main()