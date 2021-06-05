import db_methods
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

        self.formatMessages = {}
        self.errors = set()
        self.fieldNames = db_methods.get_field_names()
        self.fieldTypes = db_methods.get_field_types()
        self.element_count = len(self.fieldTypes)
        self.ruleMap = dict()
        self.create_rule_map()
        self.format_messages()

    def get_format_messages(self):
        return self.formatMessages

    def format_messages(self):

        for name in self.fieldNames:
            message = "Format of " + name + " should be "
            if name == "DAY":
                self.formatMessages[name] = message + "YYYY-MM-DD"
            elif name in ["START_TIME", "DURATION"]:
                self.formatMessages[name] = message + "HH:MM"
            elif name == "MOVIE_NAME":
                self.formatMessages[name] = message + "of minimum length 1 and maximum length " + str(self.fieldTypes[4][8:-1])
            elif name == "PRICE":
                self.formatMessages[name] = message + "a decimal number at most 2 decimal places."
            elif name == "THEATER":
                self.formatMessages[name] = message + "a single capital character from A to Z."
            elif name == "SEAT":
                self.formatMessages[name] = message + "a 2 character sequence " + \
                                            "starting with a capital letter and ending with a digit."
            elif name == "RATING":
                self.formatMessages[name] = message + "an age rating option from U, PG, 12A, 12, 15 and 18"

    # Create a rule mapping for each field.
    def create_rule_map(self):
        # For each field, we add a validation rule.
        # Return False if invalid
        for name, fieldType in zip(self.fieldNames, self.fieldTypes):
            if name == 'PRICE':
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
                # Check the length of a string is in limits of the database constraints.
                self.ruleMap[name] = lambda x: 1 <= len(x) <= int(fieldType[8:-1])
            elif "CHAR" in fieldType:
                # Check the length of the string is in limits of the database constraints.
                self.ruleMap[name] = lambda x: len(x) == int(fieldType[5:-1])
            else:
                # Default returns true always.
                self.ruleMap[name] = lambda x: True

    # Returns the rule mapping.
    def get_rule_map(self):
        return self.ruleMap

    # Used to validate a record for input.
    def validate(self, record):
        # Check the value input is a tuple.
        if isinstance(record, tuple):
            # Check the length of the record.
            if len(record) == self.element_count:
                # Check the type of each field in the record using the rule map.
                for field, name in record, self.fieldNames:
                    # If there is an invalid data element, we add an error to the error set.
                    if not self.ruleMap[name](field):
                        self.errors.add("Invalid input for "+name)
            else:
                self.errors.add("The number of elements in this record do not match the number of fields.")
        else:
            self.errors.add("Inserted record must be a tuple.")
