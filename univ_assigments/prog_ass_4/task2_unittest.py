import unittest


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


class TestMath(unittest.TestCase):
    def test_multiply_positive(self):
        self.assertEqual(multiply(3, 4), 12)

    def test_multiply_negative(self):
        self.assertEqual(multiply(-2, 5), -10)

    def test_divide_normal(self):
        self.assertEqual(divide(10, 2), 5.0)
        self.assertTrue(divide(10, 2) == 5.0)
        self.assertFalse(divide(10, 2) == 4.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)


if __name__ == '__main__':
    unittest.main()