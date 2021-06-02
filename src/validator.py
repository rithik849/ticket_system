import db_methods
import decimal
import re
from datetime import datetime
# from prettytable import PrettyTable


# Validates the date is in the format of year-month-day
def datetime_validation(datetime_to_check, datetime_format):
    try:
        res = bool(datetime.strptime(datetime_to_check, datetime_format))
    except ValueError:
        res = False
    return res


class Validator:

    def __init__(self):

        self.errors = set()
        self.field_names = db_methods.get_field_names()
        self.field_types = db_methods.get_field_types()
        self.element_count = len(self.field_types)
        self.rule_map = dict()
        self.create_rule_map()

    # Create a rule mapping for each field.
    def create_rule_map(self):

        # For each field, we add a validation rule.
        for name, field_type in zip(self.field_names, self.field_types):
            if name == 'PRICE':
                self.rule_map[name] = lambda x: x*100 % 1 == 0
            elif name == 'THEATER':
                self.rule_map[name] = lambda x: re.search('[A-Z]', x) is None
            elif name == 'SEAT':
                self.rule_map[name] = lambda x: re.search('[A-Z][0-9]', x) is None
            elif name == 'RATING':
                self.rule_map[name] = lambda x: x in ["U", "PG", "12A", "12", "15", "18"]
            elif field_type == 'DATE':
                self.rule_map[name] = lambda x: datetime_validation(x, '%Y-%m-%d')
            elif field_type == 'TIME':
                self.rule_map[name] = lambda x: datetime_validation(x, '%H:%M')
            elif "VARCHAR" in field_type:
                self.rule_map[name] = lambda x: 1 <= len(x) <= int(field_type[8:-1])
            else:
                self.rule_map[name] = lambda x: True

    # Returns the rule mapping.
    def get_rule_map(self):
        return self.rule_map

    # Used to validate a record for input.
    def validate(self, record):
        # Check the value input is a tuple.
        if isinstance(record, tuple):
            # Check the length of the record.
            if len(record) == self.element_count:
                # Check the type of each field in the record using the rule map.
                for field, name in record, self.field_names:
                    # If there is an error, we add an error to the error set.
                    if not self.rule_map[name](field):
                        self.errors.add("Invalid input for "+name)
            else:
                self.errors.add("The number of elements in this record do not match the number of fields.")
        else:
            self.errors.add("Inserted record must be a tuple.")
