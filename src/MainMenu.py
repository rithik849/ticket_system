from prettytable import PrettyTable
import db_methods
import sys
import os
from validator import Validator


class MainMenu:

    def __init__(self):
        self.validator = Validator()
        self.table = PrettyTable()
        self.options = {
            "c": "Create Row",
            "r": "Select Rows",
            "u": "Update Rows",
            "d": "Delete Rows",
            "h": "Help",
            "q": "Quit"
        }
        # self.methods = {
        #     "c": self.create_row(),
        #     "r": self.select_rows(),
        #     "u": self.update_rows(),
        #     "d": self.delete_rows(),
        #     "h": self.help(),
        #     "q": self.quit()
        # }

    def run(self):
        while True:
            option_input = input("Select option " + str(self.options) + " :")
            option_input = str.lower(option_input)
            if option_input not in self.options.keys():
                print("Not an option")
            elif option_input == "c":
                self.create_row()
            elif option_input == "r":
                self.select_rows()
            elif option_input == "u":
                self.update_rows()
            elif option_input == "d":
                self.delete_rows()
            elif option_input == "h":
                self.help()
            elif option_input == "q":
                self.quit()

    def help(self):
        for key in self.options.keys():
            print(key + " : " + self.options[key])

    def quit(self):
        confirm = input("Are you sure you want to quit?y for yes:\n")
        if str.lower(confirm.strip()) == 'y':
            print("Quiting Application")
            os._exit(1)

    def create_row(self):
        # Create Row protocol
        newRecord = []
        fieldNames = db_methods.get_field_names()[1:]
        index = 0
        error = False
        while index < len(fieldNames) and not error:
            field = fieldNames[index]
            value = input("Enter value for " + str.lower(field) + ":")
            value = value.strip()

            if value == "PRICE":
                value = float(value)

            if field == "MOVIE_NAME":
                print(value)

            error = not self.validator.get_rule_map()[field](value)
            if not error:
                newRecord.append(value)
                index += 1
        if error:
            print(self.validator.get_format_messages()[fieldNames[index]])
        else:
            db_methods.insert(tuple(newRecord))

    def select_rows(self):
        # Selection of Rows Protocol
        select = input("Enter fields to be selected separated by commas. \n(Leave blank to select all fields):\n")
        where = input("Enter selection condition \n(Leave blank if you want the whole table):\n")
        select = "*" if select.strip() == '' else str.upper(select.strip())

        where = None if where.strip() == '' else where.strip()

        selected_records = db_methods.read(select, where)

        if selected_records:
            self.table.field_names = selected_records.pop()
            self.table.add_rows(selected_records)
            self.print_table()
        self.table.clear()

    def update_rows(self):
        # Update rows protocol
        set_fields = input("Select which fields to assign to what values:\n")
        where = input("Enter update condition:\n")
        if set_fields.strip() == '':
            print("Error: Select which variables should be updated to which values.")
        else:
            if where.strip() == '':
                db_methods.update(set_fields)
            else:
                db_methods.update(set_fields, where)

    def delete_rows(self):
        # Delete Rows protocol
        where = input("Select records to delete (Leave blank to delete all records):\n")
        if where.strip() == '':
            confirm = input("Are you sure you want to delete all records? y for yes:\n")
            if str.lower(confirm).strip() == 'y':
                db_methods.delete()

    def print_table(self):
        print(self.table.get_string())


def main():
    a = MainMenu()
    a.run()


if __name__ == "__main__":
    main()
