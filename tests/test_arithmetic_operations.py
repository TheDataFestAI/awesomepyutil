import unittest
# import os, sys
# print(sys.path)
# print(os.getcwd())

from arithmetic_ops.arithmetic_operations import func_divide

class TestArithmeticOperations(unittest.TestCase):
    
    def test_func_divide(self):
        self.assertEqual(func_divide(5,2), 2.5)


if __name__ == "__main__":
    unittest.main()