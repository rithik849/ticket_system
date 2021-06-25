import sys
import unittest
import os
sys.path.append("../src")
from logFileIO import LogFileIO


class TestFileIO(unittest.TestCase):

    def setUp(self):
        self.fileIO = LogFileIO()

    def test_append(self):
        test = "Test String"
        self.fileIO.append(test)
        actual = self.fileIO.read()
        self.assertEqual([test+"\n"], actual)

    def tearDown(self):
        os.remove("log.txt")


if __name__ == '__main__':
    unittest.main()
