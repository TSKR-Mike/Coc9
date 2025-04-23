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


if __name__ == '__main__':
    unittest.main()