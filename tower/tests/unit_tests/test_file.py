"""
This is a test file. Do not use this file. Define yours
"""

import unittest


class TestClass(unittest.TestCase):
    def setUp(self):
        self.message = 'hello world'

    def test_is_string(self):
        self.assertTrue(type(self.message), str)

    def test_message(self):
        self.assertEqual(self.message, "hello world")
