import sys
import unittest
import os
sys.path.append("../src")

from unittest.mock import patch
from db_methods import DatabaseAccessor
from MainMenu import MainMenu


class TestMainMenu(unittest.TestCase):

    def setUp(self):
        self.menu = MainMenu()
        self.conn = DatabaseAccessor()
        self.menu.dbConnection.populate()

    def test_isReturn(self):
        self.assertFalse(self.menu.isReturn("DAY = '2020-03-03'"))
        self.assertTrue(self.menu.isReturn(";"))

    def test_setup(self):
        if self.conn.hasTable("TICKETS"):
            self.conn.destroy("TICKETS")
        self.menu.setup()
        self.assertTrue(self.conn.hasTable("TICKETS"))
        self.assertEqual(self.conn.get_number_of_rows(), 10)

    def test_write_errors(self):
        test_errors = {
            ('inc1', '2021-02-03', '12:30', 'emp44', 'In Progress', 'All', 'em32', 2):
                "\tASSIGNED_TO should be of format emp followed by 2 digits\n",
            ('inc2', '2021-02-03', '12:31', 'emp44', 'Almost Done', 'All', 'emp32', 2):
                "\tSTATUS should be one of 'New','In Progress' or 'Complete'\n"
        }

        self.menu.write_errors(test_errors)
        actual = ""
        with open('log.txt', 'r') as log:
            actual = log.readlines()
        actual = "".join(actual[1:])
        expected = ""
        for rec in test_errors.keys():
            expected += str(rec)+"\n"
            expected += test_errors[rec]
        expected = expected + "\n"

        os.remove("log.txt")
        self.assertEqual(actual, expected)

    def test_create_row(self):
        self.conn.delete()
        user_input = ['inc1', '2021-03-02', '10:20', 'emp33', 'new', 'New', 'Team C', 'emp42', '1']
        with patch('builtins.input', side_effect=user_input):
            self.menu.create_row()
        actual = self.conn.read()
        actual.pop()
        expected = ('inc1', '2021-03-02', '10:20', 'emp33', 'New', 'Team C', 'emp42', 1)
        expected = [expected]
        self.assertEqual(actual, expected)

    def test_create_row_return_to_menu(self):
        self.conn.delete()
        user_inputs = [['inc1', '2021-03-02', '10:20', 'emp33', 'New', 'Team C', 'emp42', ';'], [';']]
        for user_input in user_inputs:
            with patch('builtins.input', side_effect=user_input):
                self.menu.create_row()
            actual = self.conn.get_number_of_rows()
            expected = 0
            self.assertEqual(actual, 0)

    def test_select_rows(self):
        user_inputs = [["", ""],
                       ["", "INCIDENT_TIME == '04:00'"],
                       ["DAY", "STATUS", "", "PRIORITY < 3"],
                       ["INCIDENT_ID", "", "PRIORITY < 3 AND STATUS == 'New'"]]

        expected_outputs = [
            [
                ('inc0', '2021-03-01', '00:00', 'emp00', "In Progress", 'Wintel Group', 'emp44', 2),
                ('inc1', '2021-03-02', '04:00', 'emp01', "In Progress", 'Linux Team', 'emp47', 3),
                ('inc2', '2021-03-02', '04:00', 'emp10', "New", 'Application Team', 'emp07', 1),
                ('inc3', '2021-06-12', '16:30', 'emp11', "Complete", 'Network Team', 'emp49', 2),
                ('inc4', '2021-05-22', '19:30', 'emp23', "New", 'Windows Team', 'emp99', 2),
                ('inc5', '2021-04-02', '17:20', 'emp34', "Complete", 'Mac/iOS Team', 'emp32', 3),
                ('inc6', '2021-03-04', '23:00', 'emp67', "Complete", 'Android Team', 'emp44', 3),
                ('inc7', '2021-03-03', '04:00', 'emp34', "New", 'Fullstack Team', 'emp12', 2),
                ('inc8', '2021-03-05', '04:00', 'emp43', "In Progress", 'All', 'emp43', 2),
                ('inc9', '2021-06-11', '16:30', 'emp66', "Complete", 'Linux Team', 'emp10', 2),
                ['INCIDENT_ID', 'DAY', 'INCIDENT_TIME', 'RAISED_BY', 'STATUS', 'TEAM', 'ASSIGNED_TO', 'PRIORITY']
            ],
            [
                ('inc1', '2021-03-02', '04:00', 'emp01', "In Progress", 'Linux Team', 'emp47', 3),
                ('inc2', '2021-03-02', '04:00', 'emp10', "New", 'Application Team', 'emp07', 1),
                ('inc7', '2021-03-03', '04:00', 'emp34', "New", 'Fullstack Team', 'emp12', 2),
                ('inc8', '2021-03-05', '04:00', 'emp43', "In Progress", 'All', 'emp43', 2),
                ['INCIDENT_ID', 'DAY', 'INCIDENT_TIME', 'RAISED_BY', 'STATUS', 'TEAM', 'ASSIGNED_TO', 'PRIORITY']
            ],
            [
                ('2021-03-01', "In Progress"),
                ('2021-03-02', "New"),
                ('2021-06-12', "Complete"),
                ('2021-05-22', "New"),
                ('2021-03-03', "New"),
                ('2021-03-05', "In Progress"),
                ('2021-06-11', "Complete"),
                ["DAY", "STATUS"]
            ],
            [
                tuple(['inc2']),
                tuple(['inc4']),
                tuple(['inc7']),
                ["INCIDENT_ID"]
            ]
        ]

        for user_input, expected in zip(user_inputs, expected_outputs):

            with patch('builtins.input', side_effect=user_input):
                actual = self.menu.select_rows()
            self.assertEqual(actual, expected)

    def test_update_rows(self):

        original = [
            ('inc0', '2021-03-01', '00:00', 'emp00', "In Progress", 'Wintel Group', 'emp44', 2),
            ('inc1', '2021-03-02', '04:00', 'emp01', "In Progress", 'Linux Team', 'emp47', 3),
            ('inc2', '2021-03-02', '04:00', 'emp10', "New", 'Application Team', 'emp07', 1),
            ('inc3', '2021-06-12', '16:30', 'emp11', "Complete", 'Network Team', 'emp49', 2),
            ('inc4', '2021-05-22', '19:30', 'emp23', "New", 'Windows Team', 'emp99', 2),
            ('inc5', '2021-04-02', '17:20', 'emp34', "Complete", 'Mac/iOS Team', 'emp32', 3),
            ('inc6', '2021-03-04', '23:00', 'emp67', "Complete", 'Android Team', 'emp44', 3),
            ('inc7', '2021-03-03', '04:00', 'emp34', "New", 'Fullstack Team', 'emp12', 2),
            ('inc8', '2021-03-05', '04:00', 'emp43', "In Progress", 'All', 'emp43', 2),
            ('inc9', '2021-06-11', '16:30', 'emp66', "Complete", 'Linux Team', 'emp10', 2)
        ]

        user_inputs = [
            ["", "ind0", "STATUS", "In Progress", "INCIDENT_ID", "inc", "inc11", "", "PRIORITY == 1"],
            ["PRIORITY", "5", "1", "", "INCIDENT_TIME == '04:00'"]

        ]

        test_ignore_ids = [
            tuple([]),
            tuple(["inc0", "inc1", "inc7"])
                           ]
        # Records in the table
        expected_in = [
            [
                ('inc11', '2021-03-02', '04:00', 'emp10', "In Progress", 'Application Team', 'emp07', 1)
            ],
            [
                ('inc2', '2021-03-02', '04:00', 'emp10', "New", 'Application Team', 'emp07', 1),
                ('inc8', '2021-03-05', '04:00', 'emp43', "In Progress", 'All', 'emp43', 1)
            ]
        ]
        # Records out of the table
        expected_out = [
            [('inc2', '2021-03-02', '04:00', 'emp10', "New", 'Application Team', 'emp07', 1)],
            [('inc8', '2021-03-05', '04:00', 'emp43', "In Progress", 'All', 'emp43', 2)]
        ]
        # Records ignored during change
        expected_unchanged = [
            [
                ('inc0', '2021-03-01', '00:00', 'emp00', "In Progress", 'Wintel Group', 'emp44', 2),
                ('inc1', '2021-03-02', '04:00', 'emp01', "In Progress", 'Linux Team', 'emp47', 3),
                ('inc3', '2021-06-12', '16:30', 'emp11', "Complete", 'Network Team', 'emp49', 2),
                ('inc4', '2021-05-22', '19:30', 'emp23', "New", 'Windows Team', 'emp99', 2),
                ('inc5', '2021-04-02', '17:20', 'emp34', "Complete", 'Mac/iOS Team', 'emp32', 3),
                ('inc6', '2021-03-04', '23:00', 'emp67', "Complete", 'Android Team', 'emp44', 3),
                ('inc7', '2021-03-03', '04:00', 'emp34', "New", 'Fullstack Team', 'emp12', 2),
                ('inc8', '2021-03-05', '04:00', 'emp43', "In Progress", 'All', 'emp43', 2),
                ('inc9', '2021-06-11', '16:30', 'emp66', "Complete", 'Linux Team', 'emp10', 2)
             ],
            [
                ('inc0', '2021-03-01', '00:00', 'emp00', "In Progress", 'Wintel Group', 'emp44', 2),
                ('inc1', '2021-03-02', '04:00', 'emp01', "In Progress", 'Linux Team', 'emp47', 3),
                ('inc3', '2021-06-12', '16:30', 'emp11', "Complete", 'Network Team', 'emp49', 2),
                ('inc4', '2021-05-22', '19:30', 'emp23', "New", 'Windows Team', 'emp99', 2),
                ('inc5', '2021-04-02', '17:20', 'emp34', "Complete", 'Mac/iOS Team', 'emp32', 3),
                ('inc6', '2021-03-04', '23:00', 'emp67', "Complete", 'Android Team', 'emp44', 3),
                ('inc7', '2021-03-03', '04:00', 'emp34', "New", 'Fullstack Team', 'emp12', 2),
                ('inc9', '2021-06-11', '16:30', 'emp66', "Complete", 'Linux Team', 'emp10', 2)
            ]
        ]

        self.conn.delete()

        for user_input, ignored_ids, rec_in, rec_out, rec_unchanged in zip(user_inputs, test_ignore_ids, expected_in, expected_out, expected_unchanged):
            self.conn.populate()
            self.menu.error_ids = ignored_ids

            with patch('builtins.input', side_effect=user_input):
                self.menu.update_rows()
            actual = self.conn.read()
            actual.pop()
            self.assertEqual(self.conn.get_number_of_rows(),10)
            for rec in rec_in+rec_unchanged:
                self.assertIn(rec, actual)
            for rec in rec_out:
                self.assertNotIn(rec, actual)
            self.conn.delete()

    def test_delete(self):

        original = [
            ('inc0', '2021-03-01', '00:00', 'emp00', "In Progress", 'Wintel Group', 'emp44', 2),
            ('inc1', '2021-03-02', '04:00', 'emp01', "In Progress", 'Linux Team', 'emp47', 3),
            ('inc2', '2021-03-02', '04:00', 'emp10', "New", 'Application Team', 'emp07', 1),
            ('inc3', '2021-06-12', '16:30', 'emp11', "Complete", 'Network Team', 'emp49', 2),
            ('inc4', '2021-05-22', '19:30', 'emp23', "New", 'Windows Team', 'emp99', 2),
            ('inc5', '2021-04-02', '17:20', 'emp34', "Complete", 'Mac/iOS Team', 'emp32', 3),
            ('inc6', '2021-03-04', '23:00', 'emp67', "Complete", 'Android Team', 'emp44', 3),
            ('inc7', '2021-03-03', '04:00', 'emp34', "New", 'Fullstack Team', 'emp12', 2),
            ('inc8', '2021-03-05', '04:00', 'emp43', "In Progress", 'All', 'emp43', 2),
            ('inc9', '2021-06-11', '16:30', 'emp66', "Complete", 'Linux Team', 'emp10', 2)
        ]

        user_inputs = [
            ["", "y"],
            ["INCIDENT_TIME == '04:00'", "y"],
            ["INCIDENT_TIME == '04:00'", "n"],
            ["INCIDENT_TIME == '04:00'", ";"],
            [";"],
        ]

        test_ignored_ids = [
            tuple(["inc0", "inc9"]),
            tuple([]),
            tuple([]),
            tuple([]),
            tuple([])
        ]

        expected_remaining_records = [
            [
                ('inc0', '2021-03-01', '00:00', 'emp00', "In Progress", 'Wintel Group', 'emp44', 2),
                ('inc9', '2021-06-11', '16:30', 'emp66', "Complete", 'Linux Team', 'emp10', 2)
            ],
            [
                ('inc0', '2021-03-01', '00:00', 'emp00', "In Progress", 'Wintel Group', 'emp44', 2),
                ('inc3', '2021-06-12', '16:30', 'emp11', "Complete", 'Network Team', 'emp49', 2),
                ('inc4', '2021-05-22', '19:30', 'emp23', "New", 'Windows Team', 'emp99', 2),
                ('inc5', '2021-04-02', '17:20', 'emp34', "Complete", 'Mac/iOS Team', 'emp32', 3),
                ('inc6', '2021-03-04', '23:00', 'emp67', "Complete", 'Android Team', 'emp44', 3),
                ('inc9', '2021-06-11', '16:30', 'emp66', "Complete", 'Linux Team', 'emp10', 2)
            ],
            original,
            original,
            original
        ]

        self.conn.delete()

        for user_input, ignored_ids, expected in zip(user_inputs, test_ignored_ids, expected_remaining_records):
            print(user_input)
            self.conn.populate()
            self.menu.error_ids = ignored_ids

            with patch('builtins.input', side_effect=user_input):
                self.menu.delete_rows()

            actual = self.conn.read()
            actual.pop()

            for rec in expected:
                self.assertIn(rec, actual)

            self.conn.delete()

    def tearDown(self):
        self.conn.delete(table_name="CLONE")
        self.conn.delete()
        self.conn.disconnect()


if __name__ == "__main__":
    unittest.main()
