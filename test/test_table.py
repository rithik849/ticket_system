import sys
import unittest
import io
sys.path.append("../src")
from table import Table

class TestTable(unittest.TestCase):

    def setUp(self):
        self.table = Table()

    def test_set_fields(self):
        test_fields = ["Field1", "Field2", "Field3"]
        self.table.set_fields(test_fields)
        expected = ""
        for field in test_fields:
            expected += field + " "*10
        expected = "\x1b[92m\x1b[1m" + expected + "\x1b[0m\n"

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.table.print_table()
        sys.stdout = sys.__stdout__

        actual = capturedOutput.getvalue()
        self.assertEqual(expected, actual)

    def test_set_records(self):
        test_fields = ["A", "B", "FieldC"]
        test_records = [("inc23234324323", "21", "Test"),
                        ("inc32", "243", "Test2")]
        max_column_lengths = [len("inc23234324323"), len("243"), len("FieldC")]
        self.table.set_fields(test_fields)
        self.table.set_records(test_records)
        # Generate the table expected
        expected = ""
        for col_length, field in zip(max_column_lengths, test_fields):
            expected += field + " "*((col_length + 10) - len(field))
        expected = "\x1b[92m\x1b[1m" + expected + "\x1b[0m\n"

        for record in test_records:
            expected += "\033[32m"
            for col_length, element in zip(max_column_lengths, record):
                expected += element + " "*((col_length + 10) - len(element))
            expected += "\x1b[0m\n"

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.table.print_table()
        sys.stdout = sys.__stdout__

        actual = capturedOutput.getvalue()
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

