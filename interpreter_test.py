import unittest
from interpreter import eval_expr, validate_input
import math


class TestMathInterpreter(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(eval_expr("1 + 2"), 3)
        self.assertEqual(eval_expr("5 - 3"), 2)
        self.assertEqual(eval_expr("2 * 3"), 6)
        self.assertEqual(eval_expr("8 / 2"), 4)

    def test_variables(self):
        self.assertEqual(eval_expr("a + b", {"a": 1, "b": 2}), 3)
        self.assertEqual(eval_expr("a - b", {"a": 5, "b": 3}), 2)

    def test_functions(self):
        self.assertAlmostEqual(eval_expr("sin(0)"), 0)
        self.assertAlmostEqual(eval_expr("cos(0)"), 1)
        self.assertAlmostEqual(eval_expr("sqrt(4)"), 2)

    def test_user_functions(self):
        user_functions = {"foo": lambda x: x * 42}
        self.assertEqual(eval_expr("foo(2)",
                                   user_functions=user_functions), 84)

    def test_complex_expression(self):
        expr = "a + 2 - sin(-0.3) * (b - c)"
        variables = {"a": 1, "b": 4, "c": 2}
        result = eval_expr(expr, variables)
        self.assertAlmostEqual(result, 1 + 2 - math.sin(-0.3) * (4 - 2))

    def test_error_handling(self):
        with self.assertRaises(NameError):
            eval_expr("a + b")
        with self.assertRaises(NameError):
            eval_expr("unknown_func(2)")
        with self.assertRaises(TypeError):
            eval_expr("2 + (1, 2)")

    def test_input_validation(self):
        self.assertTrue(
            validate_input("a + b",
                           {"a": 1, "b": 2},
                           {"foo": lambda x: x * 42})
        )
        with self.assertRaises(ValueError):
            validate_input("a + b",
                           {"1a": 1, "b": 2})
        with self.assertRaises(ValueError):
            validate_input("a + b",
                           {"a": 1, "b": 2},
                           {"1foo": lambda x: x * 42})
        with self.assertRaises(ValueError):
            validate_input("a + b",
                           {"a": 1, "b": 2},
                           {"foo": "not a function"})
