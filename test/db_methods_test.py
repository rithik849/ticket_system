from unittest import TestCase
import sys

sys.path.append("../src")
from db_methods import DatabaseAccessor


class DBAccessorTestCase(TestCase):

    def __init__(self):
        super().__init__()
        self.DBConn = DatabaseAccessor()

    def setUp(self):
        self.DBConn.reconnect()

    def test_table_creation(self):
        self.create_table()
        self.assertEqual(self.DBConn.hasTable("TICKETS"), True)

    def test_has_table(self):
        self.assertEquals(self.DBConn.hasTable("TICKETS"), True)
        self.assertEquals(self.DBConn.hasTable("UNKNOWN_TABLE"), False)

    def test_clone_table(self):
        self.DBConn.clone_table()
        self.assertEquals(self.DBConn.hasTable("CLONE"), True)
        self.assertEquals(self.DBConn.get_number_of_rows("CLONE"), 0)
        self.destroy("CLONE")

    def test_insert_rows(self):
        test_rows = [("inc1", "2021-01-01", "00:00", "emp00", "Complete", "GROUP A", "emp45", '1'),
                     ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3')]
        self.DBConn.insert_rows(test_rows)
        self.assertEquals(self.DBConn.get_number_of_rows("TICKETS"), 2)
        self.DBConn.delete()

    def test_insert(self):
        test_row = ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3')
        self.assertTrue(self.DBConn.insert(test_row))
        self.assertEquals(self.DBConn.get_number_of_rows("TICKETS"), 1)
        self.DBConn.delete()

    def test_update(self):
        test_row = ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3')
        self.assertTrue(self.DBConn.insert(test_row))
        self.DBConn.update({"DAY": "2020-04-04"}, "INCIDENT_TIME = '5:30'")

        self.assertIn(("inc3", "2020-04-04", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3')
                      , self.DBConn.read())

    def test_read(self):
        test_rows = [("inc1", "2021-01-01", "00:00", "emp00", "Complete", "GROUP A", "emp45", '1'),
                     ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3'),
                     ("inc2", "2021-02-02", "02:30", "emp44", "New", "GROUP B", "emp44", "2"),
                     ("inc0", "2021-04-03", "04:30", "emp55", "New", "GROUP A", "emp32", "1")]
        expected_values = [('inc1', 'emp00'), ('inc2', '02:30'), ['INCIDENT_ID', 'RAISED_BY']]
        self.DBConn.insert_rows(test_rows)
        actual_values = self.DBConn.read("INCIDENT_ID, RAISED_BY", "INCIDENT_TIME < '03:00'")
        self.assertEquals(expected_values, actual_values)

    def test_delete(self):
        test_rows = [("inc1", "2021-01-01", "00:00", "emp00", "Complete", "GROUP A", "emp45", '1'),
                     ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3'),
                     ("inc2", "2021-02-02", "02:30", "emp44", "New", "GROUP B", "emp44", "2"),
                     ("inc0", "2021-04-03", "04:30", "emp55", "New", "GROUP A", "emp32", "1")
                     ]

        self.DBConn.insert_rows(test_rows)

        expected_values = {("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3'),
                           ("inc0", "2021-04-03", "04:30", "emp55", "New", "GROUP A", "emp32", "1")
                           }

        self.assertTrue(self.DBConn.delete("INCIDENT_DATE > '2021-03-01"))

        actual_values = self.DBConn.read()
        actual_values.pop()

        self.assertEquals(expected_values, set(actual_values))

    def test_get_number_of_rows(self):
        test_rows = [("inc1", "2021-01-01", "00:00", "emp00", "Complete", "GROUP A", "emp45", '1'),
                     ("inc3", "2021-03-23", "05:30", "emp33", "In Progress", "GROUP C", "emp66", '3'),
                     ("inc2", "2021-02-02", "02:30", "emp44", "New", "GROUP B", "emp44", "2"),
                     ("inc0", "2021-04-03", "04:30", "emp55", "New", "GROUP A", "emp32", "1")
                     ]

        self.DBConn.insert_rows(test_rows)
        self.assertEquals(self.DBConn.get_number_of_rows(), 4)

    def test_get_field_names(self):
        expected = ["INCIDENT_ID", "DAY", "INCIDENT_TIME", "RAISED_BY", "STATUS", "TEAM", "ASSIGNED_TO"
                    , "PRIORITY"]

        actual = self.DBConn.get_field_names()

        self.assertEquals(expected, actual)

    def test_get_field_types(self):
        expected = ["VARCHAR(10)", "DATE", "TIME", "CHAR(5)", "VARCHAR(11)", "VARCHAR(50)", "CHAR(5)"
                    , "INTEGER"]
        actual = self.DBConn.get_field_types()
        self.assertEquals(expected, actual)

    def test_table_population(self):
        self.populate()
        self.assertEquals(self.DBConn.get_number_of_rows(), 10)

    def test_destroy(self):
        self.DBConn.destroy()
        self.assertFalse(self.DBConn.hasTable("TICKETS"))

    def test_disconnect(self):
        self.DBConn.disconnect()
        self.assertEquals(self.DBConn.read(), None)

    def tearDown(self):
        self.DBConn.disconnect()


if __name__ == '__main__':
    unittest.main()
