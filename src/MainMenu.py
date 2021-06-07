from table import Table
from db_methods import DatabaseAccessor
import sys
import os
from validator import Validator


class MainMenu:

    def __init__(self):
        self.dbConnection = DatabaseAccessor()
        self.validator = Validator()
        self.table = Table()
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
        confirm = input("Are you sure you want to quit? y for yes:\n")
        if str.lower(confirm.strip()) == 'y':
            print("Quiting Application")
            self.dbConnection.disconnect()
            self.validator.disconnect()
            os._exit(1)

    def create_row(self):
        # Create Row protocol
        newRecord = []
        fieldNames = self.dbConnection.get_field_names()
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
            self.dbConnection.insert(tuple(newRecord))

    def select_rows(self):
        # Selection of Rows Protocol
        invalid = False
        end = False
        firstIteration = True
        fieldNames = self.dbConnection.get_field_names()
        msg = "Enter field to be selected. \n"
        selected_fields = []

        # Allow user to select multiple fields
        while not invalid and not end:
            # In the first iteration, not specifying a value selects all fields.
            # Otherwise it selects all previously chosen fields.
            if firstIteration:
                select = input(msg+"(Leave blank to select all fields):\n")
            else:
                select = input(msg+"(Leave blank to stop selecting)\n")
            # Remove leading and trailing whitespaces
            select = select.strip()
            if select == '':
                if firstIteration:
                    select = "*"
                end = True
            else:
                firstIteration = False
                # If the input does not match a field we give an error.
                # Otherwise add the field to a list of selected fields.
                if select not in fieldNames:
                    invalid = True
                    print("No such field "+select+". Valid fields are: "+str(fieldNames))
                else:

                    selected_fields = selected_fields + [select]
        # Only allow the input of a where clause if the selected fields are valid.
        if not invalid:
            where = input("Enter selection condition \n(Leave blank if you want all records):\n")
            where = None if where.strip() == '' else where.strip()
            if select == "*":
                selected_records = self.dbConnection.read(select, where)
            else:
                selected_records = self.dbConnection.read(",".join(selected_fields), where)

            if selected_records:
                self.table.set_fields(selected_records.pop())
                self.table.set_records(selected_records)
            self.table.print_table()
            self.table.clear()

    def update_rows(self):
        # Update rows protocol
        field_names = self.dbConnection.get_field_names()
        invalid = False
        end = False
        field_update = {}
        # While we still have values to add, or do not have an invalid input.
        while not invalid and not end:
            # Select the field of which the value should be changes
            set_field = input("Select field to change value:\n(Leave blank to end changes)\n")
            set_field = set_field.strip()
            print(":'"+set_field+"'")
            # Check if the field is a fieldName
            if set_field in field_names:
                # Set a value for the field
                set_value = input("Select value to be changed to:\n")
                set_value = set_value.strip()
                # Check the validity of the field
                if self.validator.get_rule_map()[set_field](set_value):
                    field_update[set_field] = set_value
                else:
                    invalid = True
            elif set_field == '':
                # If no fields were added stop execution
                if len(field_update) == 0:
                    invalid = True
                    print("No fields added for update.")
                else:
                    end = True
            else:
                invalid = True
                print(set_field+" field does not exist.\nValid fields: "+str(field_names))
        # Choose update condition
        if not invalid:
            where = input("Enter update condition:\n")
            if where.strip() == '':
                self.dbConnection.update(field_update)
            else:
                self.dbConnection.update(field_update, where)

    def delete_rows(self):
        # Delete Rows protocol
        where = input("Specify condition for records to delete (Leave blank to delete all records):\n")
        confirm = input("Are you sure you want to delete these records? y for yes:\n")
        if str.lower(confirm).strip() == 'y':
            if where.strip() == '':
                self.dbConnection.delete()
            else:
                self.dbConnection.delete(where)



def main():
    a = MainMenu()
    a.run()


if __name__ == "__main__":
    main()
