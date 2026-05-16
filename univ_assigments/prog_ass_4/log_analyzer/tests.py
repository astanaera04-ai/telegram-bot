import sys
import os

# Python-ға қазіргі папкадан (log_analyzer ішінен) модульдерді іздеуді бұйырамыз
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import unittest
import re
from parser import parse_line
from filters import ErrorIterator

def validate_password(pw):
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%]).{8,}$'
    return bool(re.search(pattern, pw))

class TestAnalyzer(unittest.TestCase):
    def test_parse_valid_line(self):
        line = "2024-01-15 09:32:11 ERROR 192.168.1.1 - Disk full"
        res = parse_line(line)
        self.assertIsNotNone(res)
        self.assertEqual(res['level'], 'ERROR')

    def test_parse_invalid_line(self):
        res = parse_line("Invalid format log")
        self.assertIsNone(res)

    def test_error_iterator(self):
        lines = ["INFO - OK", "ERROR - Bad", "WARNING - Hmm"]
        errors = list(ErrorIterator(lines))
        self.assertEqual(len(errors), 1)

    def test_password_validator(self):
        self.assertTrue(validate_password("Valid123!"))
        self.assertFalse(validate_password("weak"))

if __name__ == '__main__':
    unittest.main()