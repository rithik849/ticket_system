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
        self.ids = [rec[0] for rec in self.dbConn.read("ID") if rec != ["ID"]]
        self.formatMessages = {}
        self.errors = set()
        self.fieldNames = self.dbConn.get_field_names()
        self.fieldTypes = self.dbConn.get_field_types()
        self.element_count = len(self.fieldTypes)
        self.ruleMap = dict()
        self.create_rule_map()
        self.format_messages()

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
            if name == 'ID':
                # Check that all ids are unique
                self.ruleMap[name] = lambda x: x not in [rec[0] for rec in self.dbConn.read("ID") if rec != ['ID']] \
                                               and re.fullmatch(r'[A-Za-z0-9]{5}', x)
            elif name == 'PRICE':
                # Check if price is at most 2 decimal places.
                self.ruleMap[name] = lambda x: re.fullmatch(r'(^[\d]|(^[1-9](\d+)))\.[\d]{2}', str(x)) is not None
            elif name == 'THEATER':
                # Check the theater lettering.
                self.ruleMap[name] = lambda x: re.fullmatch(r'[A-Z]', x) is not None
            elif name == 'SEAT':
                # Check the seat coding.
                self.ruleMap[name] = lambda x: re.fullmatch(r'[A-Z][0-9]', x) is not None
            elif name == 'RATING':
                # Check the age rating.
                self.ruleMap[name] = lambda x: x in ["U", "PG", "12A", "12", "15", "18"]
            elif fieldType == 'DATE':
                # Check the date types conform to  year-month-day.
                self.ruleMap[name] = lambda x: date_is_valid(x)
            elif fieldType == 'TIME':
                # Check the time types conform to hour:minutes.
                self.ruleMap[name] = lambda x: time_is_valid(x)
            elif "VARCHAR" in fieldType:
                temp_type = fieldType
                # Check the length of a string is in limits of the database constraints.
                self.ruleMap[name] = lambda x: 1 <= len(x) <= int(temp_type[8:-1])
            elif "CHAR" in fieldType:
                temp_type = fieldType
                # Check the length of the string is in limits of the database constraints.
                self.ruleMap[name] = lambda x: len(x) == int(temp_type[5:-1])
            else:
                # Default returns true always.
                self.ruleMap[name] = lambda x: True

    def format_messages(self):

        for name in self.fieldNames:
            message = "Format of " + name + " should be "
            if name == "ID":
                self.formatMessages[name] = message + "a unique 5 character string of letters and/or numbers."
            if name == "DAY":
                self.formatMessages[name] = message + "YYYY-MM-DD"
            elif name in ["START_TIME", "DURATION"]:
                self.formatMessages[name] = message + "HH:MM"
            elif name == "MOVIE_NAME":
                self.formatMessages[name] = message + \
                                            "of minimum length 1 and maximum length " + str(self.fieldTypes[4][8:-1])
            elif name == "PRICE":
                self.formatMessages[name] = message + "a decimal number at most 2 decimal places."
            elif name == "THEATER":
                self.formatMessages[name] = message + "a single capital character from A to Z."
            elif name == "SEAT":
                self.formatMessages[name] = message + "a 2 character sequence " + \
                                            "starting with a capital letter and ending with a digit."
            elif name == "RATING":
                self.formatMessages[name] = message + "an age rating option from U, PG, 12A, 12, 15 and 18"

#    def table_validation(self):



