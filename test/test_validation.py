import sys
import unittest

sys.path.append("../src")
from validator import *
from db_methods import DatabaseAccessor

class TestValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DBConn = DatabaseAccessor()
        if not DBConn.hasTable("TICKETS"):
            DBConn.create_table()
        DBConn.delete()
        DBConn.insert(('inc7', '2021-03-03', '04:00', 'emp34', "New", 'Fullstack Team', 'emp12', 2))

        DBConn.disconnect()

    def setUp(self):
        self.validator = Validator()

    def test_date_is_valid(self):
        test_value_correct = '2021-05-05'
        self.assertTrue(date_is_valid(test_value_correct))
        test_value_incorrect = '2021-5-5'
        self.assertFalse(date_is_valid(test_value_incorrect))
        test_value_incorrect = '2020-2-30'
        self.assertFalse(date_is_valid(test_value_incorrect))

    def test_time_is_valid(self):
        test_value_correct = '23:30'
        self.assertTrue(time_is_valid(test_value_correct))
        test_value_incorrect = '0:20'
        self.assertFalse(time_is_valid(test_value_incorrect))
        test_value_incorrect = '24:00'
        self.assertFalse(time_is_valid(test_value_incorrect))

    def test_rule_map(self):
        ruleMap = self.validator.get_rule_map()
        # INCIDENT_ID Test
        test_insert = 'inc7'
        self.assertFalse(ruleMap["INCIDENT_ID"](test_insert))
        test_format = 'incorrect format'
        self.assertFalse(ruleMap["INCIDENT_ID"](test_format))
        test_correct = 'inc70'
        self.assertTrue(ruleMap["INCIDENT_ID"](test_correct))

        # Assigned_to and Raised_by Test

        test_insert = 'emp46'
        self.assertTrue(ruleMap["ASSIGNED_TO"](test_insert))
        self.assertTrue(ruleMap["RAISED_BY"](test_insert))
        test_insert = 'emp'
        self.assertFalse(ruleMap["ASSIGNED_TO"](test_insert))
        self.assertFalse(ruleMap["RAISED_BY"](test_insert))
        test_insert = 'emp2'
        self.assertFalse(ruleMap["ASSIGNED_TO"](test_insert))
        self.assertFalse(ruleMap["RAISED_BY"](test_insert))

        # Status Test

        test_insert = 'In Progress'
        self.assertTrue(ruleMap["STATUS"](test_insert))
        test_insert = 'Complete'
        self.assertTrue(ruleMap["STATUS"](test_insert))
        test_insert = 'New'
        self.assertTrue(ruleMap["STATUS"](test_insert))
        test_insert = 'In '
        self.assertFalse(ruleMap["STATUS"](test_insert))

        # Team test
        test_insert = ''
        self.assertFalse(ruleMap["TEAM"](test_insert))
        test_insert = 't'*50
        self.assertTrue(ruleMap["TEAM"](test_insert))
        test_insert = 't'*51
        self.assertFalse(ruleMap["TEAM"](test_insert))
        test_insert = "Team test"
        self.assertTrue(ruleMap["TEAM"](test_insert))

        # Team Priority
        test_insert = 0
        self.assertFalse(ruleMap["PRIORITY"](test_insert))
        test_insert = 1
        self.assertTrue(ruleMap["PRIORITY"](test_insert))
        test_insert = 2
        self.assertTrue(ruleMap["PRIORITY"](test_insert))
        test_insert = 3
        self.assertTrue(ruleMap["PRIORITY"](test_insert))
        test_insert = 4
        self.assertFalse(ruleMap["PRIORITY"](test_insert))
        test_insert = '3'
        self.assertTrue(ruleMap["PRIORITY"](test_insert))
        test_insert = '4'
        self.assertFalse(ruleMap["PRIORITY"](test_insert))

    def test_table_validation(self):
        test_records = [('inc7', '2021-01-01', '02:00', 'emp32', "New", 'Fullstack Team', 'emp22', 1),
                        ('inc2', '2021-01-01', '02:00', 'emp32', "New", 'Fullstack Team', 'emp22', 1),
                        ('inc3', '2021-01-1', '2:00', 'emp20', "New", 'Fullstack Team', 'emp22', 1)]
        expected_error_count = 2
        actual = self.validator.table_validation(test_records)
        self.assertEqual(len(actual), expected_error_count)


if __name__ == '__main__':
    unittest.main()
