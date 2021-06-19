from db_methods import DatabaseAccessor
import re
from datetime import datetime


# Validates the date is in the format of year-month-day
def datetime_is_valid(datetime_to_check, datetime_format):
    try:

        res = bool(datetime.strptime(datetime_to_check, datetime_format))
    except ValueError:
        res = False
    return res


# Validates the date is in the format of year-month-day
def date_is_valid(date_to_check):
    try:
        res = bool(re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', str(date_to_check))) and \
              bool(datetime.strptime(date_to_check, "%Y-%m-%d"))
    except ValueError:
        res = False
    return res


# Validates the time is in the format hour-minute
def time_is_valid(time_to_check):
    try:
        res = bool(re.fullmatch(r'[0-9]{2}:[0-9]{2}', str(time_to_check))) and \
              bool(datetime.strptime(time_to_check, "%H:%M"))
    except ValueError:
        res = False
    return res


class Validator:

    def __init__(self):
        self.dbConn = DatabaseAccessor()
        self.ids = [rec[0] for rec in self.dbConn.read("INCIDENT_ID") if rec != ["INCIDENT_ID"]]
        self.formatMessages = {}
        self.fieldNames = self.dbConn.get_field_names()
        self.fieldTypes = self.dbConn.get_field_types()
        self.element_count = len(self.fieldTypes)
        self.ruleMap = dict()
        self.create_rule_map()
        self.format_messages()

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.dbConn.disconnect()

    def get_format_messages(self):
        return self.formatMessages

    # Returns the rule mapping.
    def get_rule_map(self):
        return self.ruleMap

    # Create a rule mapping for each field.
    def create_rule_map(self):
        # For each field, we add a validation rule.
        # Return False if invalid
        counter = 0
        for name, fieldType in zip(self.fieldNames, self.fieldTypes):
            counter += 1
            if name == 'INCIDENT_ID':
                # Check that all ids are unique
                self.ruleMap[name] = lambda x: x not in \
                                               [
                                                   rec[0] for rec in self.dbConn.read("INCIDENT_ID")
                                                   if rec != ['INCIDENT_ID']
                                               ] and re.fullmatch(r'inc(\d+)', x)
            elif name == 'STATUS':
                # Check the status is one from the group
                self.ruleMap[name] = lambda x: str.upper(str(x)) in ["NEW", "IN PROGRESS", "COMPLETE"]
            elif name == 'PRIORITY':
                # Check priority is either 1 2 or 3.
                self.ruleMap[name] = lambda x: str(x) in ["1", "2", "3"]
            elif name in ['RAISED_BY', 'ASSIGNED_TO']:
                # Check that and employee id format is used.
                self.ruleMap[name] = lambda x: re.fullmatch(r'emp([\d]{2})', x) is not None
            elif fieldType == 'DATE':
                # Check the date types conform to  year-month-day.
                self.ruleMap[name] = lambda x: date_is_valid(x)
            elif fieldType == 'TIME':
                # Check the time types conform to hour:minutes.
                self.ruleMap[name] = lambda x: time_is_valid(x)
            elif "VARCHAR" in fieldType:
                # Check the length of a string is in limits of the database constraints.
                temp_type = fieldType
                self.ruleMap[name] = lambda x: 1 <= len(x) <= int(temp_type[8:-1])
            elif "CHAR" in fieldType:
                # Check the length of the string is in limits of the database constraints.
                temp_type = fieldType
                self.ruleMap[name] = lambda x: len(x) == int(temp_type[5:-1])
            else:
                # Default returns true always.
                self.ruleMap[name] = lambda x: True

    def format_messages(self):

        for name in self.fieldNames:
            message = "Format of " + name + " should be "
            if name == "INCIDENT_ID":
                self.formatMessages[name] = message + \
                                            "a unique string starting with 'inc' " + \
                                            "and ending with 1 or more digits."
            if name == "DAY":
                self.formatMessages[name] = message + "YYYY-MM-DD"
            elif name in ["INCIDENT_TIME"]:
                self.formatMessages[name] = message + "HH:MM"
            elif name in ["RAISED_BY", "ASSIGNED_TO"]:
                self.formatMessages[name] = message + \
                                            "a unique 5 character string starting with 'emp' " + \
                                            "and ending with 2 digits."
            elif name == "STATUS":
                self.formatMessages[name] = message + "an option from {'New','In Progress','Complete'}"
            elif name == "TEAM":
                self.formatMessages[name] = message + "a name of a group resolving the incident."
            elif name == "PRIORITY":
                self.formatMessages[name] = message + "a number from and including 1 to 3, " + \
                                            "with 1 being the highest priority"

    # Used to validate the rows in a table
    def table_validation(self, records):
        def check_id(identifier): return [rec[0] for rec in self.dbConn.read()].count(identifier) == 1
        errors = {}
        for record in records:
            firstErrorOfRecord = True
            index = 0
            for field in self.fieldNames:
                cond = (index != 0 and not self.ruleMap[field](record[index])) or (index == 0 and not check_id(record[index]))
                if cond:

                    if firstErrorOfRecord:
                        errors[record] = ""

                    errors[record] += "\t" + self.formatMessages[field] + "\n"
                    firstErrorOfRecord = False
                index += 1
        return errors
