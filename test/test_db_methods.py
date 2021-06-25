from unittest import TestCase
import unittest
import sys

sys.path.append("../src")
from db_methods import DatabaseAccessor


class TestDBAccessor(unittest.TestCase):

    def setUp(self):
        self.DBConn = DatabaseAccessor()
        self.DBConn.reconnect()
        for table in ["TICKETS"]:
            if self.DBConn.hasTable(table):
                self.DBConn.delete(table_name=table)
            else:

                print(table)
                self.DBConn.create_table(table)

    def test_table_creation(self):
        self.DBConn.destroy()
        self.assertEqual(self.DBConn.hasTable("TICKETS"), False)
        self.DBConn.create_table()
        self.assertEqual(self.DBConn.hasTable("TICKETS"), True)

    def test_has_table(self):
        self.assertEqual(self.DBConn.hasTable("TICKETS"), True)
        self.assertEqual(self.DBConn.hasTable("UNKNOWN_TABLE"), False)

    def test_insert_rows(self):
        test_rows = [("inc1", "2021-01-01", "00:00", "emp00", "Complete", "GROUP A", "emp45", '1'),
                     ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3')]
        self.DBConn.insert_rows(test_rows)
        self.assertEqual(self.DBConn.get_number_of_rows("TICKETS"), 2)
        self.DBConn.delete()

    def test_insert(self):
        test_row = ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3')
        self.assertTrue(self.DBConn.insert(test_row))
        self.assertEqual(self.DBConn.get_number_of_rows("TICKETS"), 1)
        self.DBConn.delete()

    def test_update(self):
        test_row = ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3')
        self.assertTrue(self.DBConn.insert(test_row))
        self.DBConn.update({"DAY": "2020-04-04"}, "INCIDENT_TIME == '05:30'")

        self.assertIn(("inc3", "2020-04-04", "05:30", "emp33", "In Progress", "GROUP C", "emp66", 3)
                      , self.DBConn.read())
        self.assertEqual(self.DBConn.get_number_of_rows(),1)
        self.DBConn.delete()

    def test_read(self):
        test_rows = [("inc1", "2021-01-01", "00:00", "emp00", "Complete", "GROUP A", "emp45", '1'),
                     ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3'),
                     ("inc2", "2021-02-02", "02:30", "emp44", "New", "GROUP B", "emp44", "2"),
                     ("inc0", "2021-04-03", "04:30", "emp55", "New", "GROUP A", "emp32", "1")]
        expected_values = [('inc1', 'emp00'), ('inc2', 'emp44'), ['INCIDENT_ID', 'RAISED_BY']]
        self.DBConn.insert_rows(test_rows)
        actual_values = self.DBConn.read("INCIDENT_ID, RAISED_BY", "INCIDENT_TIME < '03:00'")
        self.assertEqual(expected_values, actual_values)
        self.DBConn.delete()

    def test_delete(self):
        test_rows = [("inc1", "2021-01-01", "00:00", "emp00", "Complete", "GROUP A", "emp45", '1'),
                     ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3'),
                     ("inc2", "2021-02-02", "02:30", "emp44", "New", "GROUP B", "emp44", "2"),
                     ("inc0", "2021-04-03", "04:30", "emp55", "New", "GROUP A", "emp32", "1")
                     ]

        self.DBConn.insert_rows(test_rows)

        expected_values = {("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", 3),
                           ("inc0", "2021-04-03", "04:30", "emp55", "New", "GROUP A", "emp32", 1)
                           }

        self.assertTrue(self.DBConn.delete("DAY < '2021-03-01'"))

        actual_values = self.DBConn.read()
        actual_values.pop()

        self.assertEqual(expected_values, set(actual_values))

    def test_get_number_of_rows(self):
        test_rows = [("inc1", "2021-01-01", "00:00", "emp00", "Complete", "GROUP A", "emp45", '1'),
                     ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3'),
                     ("inc2", "2021-02-02", "02:30", "emp44", "New", "GROUP B", "emp44", "2"),
                     ("inc0", "2021-04-03", "04:30", "emp55", "New", "GROUP A", "emp32", "1")
                     ]

        self.DBConn.insert_rows(test_rows)
        self.assertEqual(self.DBConn.get_number_of_rows(), 4)

    def test_get_field_names(self):
        expected = ["INCIDENT_ID", "DAY", "INCIDENT_TIME", "RAISED_BY", "STATUS", "TEAM", "ASSIGNED_TO"
                    , "PRIORITY"]

        actual = self.DBConn.get_field_names()

        self.assertEqual(expected, actual)

    def test_get_field_types(self):
        expected = ["VARCHAR(10)", "DATE", "TIME", "CHAR(5)", "VARCHAR(11)", "VARCHAR(50)", "CHAR(5)"
                    , "INTEGER"]
        actual = self.DBConn.get_field_types()
        self.assertEqual(expected, actual)

    def test_table_population(self):
        self.DBConn.populate()
        self.assertEqual(self.DBConn.get_number_of_rows(), 10)

    def test_destroy(self):
        self.DBConn.conn.execute(self.DBConn.table.replace("TICKETS", "TEST_DELETION"))
        self.DBConn.destroy("TEST_DELETION")
        self.assertFalse(self.DBConn.hasTable("TEST_DELETION"))

    def test_disconnect(self):
        self.DBConn.disconnect()
        self.assertEqual(self.DBConn.read(), None)
        self.DBConn.reconnect()

    def tearDown(self):
        for table in ["TICKETS"]:
            if self.DBConn.hasTable(table_name=table):
                self.DBConn.delete(table_name=table)
        self.DBConn.disconnect()

    @classmethod
    def tearDownClass(cls):
        conn = DatabaseAccessor()
        for table in ["TICKETS"]:
            if conn.hasTable(table):
                conn.delete(table_name=table)
                conn.destroy(table)
        conn.disconnect()


if __name__ == '__main__':
    unittest.main()
