
from db_methods import DatabaseAccessor
import sys
import os
from validator import Validator
from datetime import datetime
from logFileIO import LogFileIO
from UI import UI
from table import Table


class MainMenu(UI):

    def __init__(self):
        super().__init__()
        self.dbConnection = DatabaseAccessor()
        self.setup()
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
        # Clone the database table structure. We perform read operations on the clone only.
        # And all other operations on both tables.
        # Validate according to the original table.
        self.dbConnection.clone_table()
        # Read all the records in the table.
        records = self.dbConnection.read()
        records.pop()
        # Validate all records, keeping a record of all invalid fields.
        errors = self.validator.table_validation(records)
        # Add all valid records into the clone.
        self.filter_erroneous(records, errors)
        self.write_errors(errors)

    def isReturn(self, input_value):
        return input_value == ";"

    # Setup table if it does not already exist.
    def setup(self):
        if not self.dbConnection.hasTable():
            self.dbConnection.create_table()
            self.dbConnection.populate()

    # Filter out invalid records, and add valid records to the cloned table
    def filter_erroneous(self, records, errors):
        invalid_records = errors.keys()

        valid_records = list(set(records) - set(invalid_records))
        self.dbConnection.insert_rows(valid_records, "CLONE")

    # Write the access time and the erroneous records as well as what errors have occurred in each record.
    def write_errors(self, errors):
        if errors:
            to_write = ""
            fileIO = LogFileIO()
            to_write = "Access Time: " + str(datetime.now())+"\n"
            for key in errors.keys():
                to_write += str(key)+"\n"
                to_write += errors[key]
            fileIO.append(to_write)

    # The main run loop of the application.
    def run(self):
        try:
            while True:
                # Select an option
                option_input = self.style_input("Select option " + str(self.options) + " :", "b")
                option_input = str.lower(option_input.strip())
                # Check if the option is valid and apply the correct routine
                if option_input == ";":
                    self.style_print("Already at main menu.", "g")
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
                elif option_input == ";":
                    self.style_print("Already at main menu.", "g")
                else:
                    self.style_print("Not an option", "r*")
        except EOFError:
            self.style_print("\nQuiting Application", "g")

    # Help to users
    def help(self):

        help_text = ""
        for key in self.options.keys():
            help_text += key + " : " + self.options[key] + "\n"
        self.style_print(help_text)

    # Quit the application
    def quit(self):
        confirm = self.style_input("Are you sure you want to quit? y for yes:\n", "y~")
        if self.isReturn(confirm.strip()):
            self.style_print("Returning to Main Menu", "g")
        elif str.lower(confirm.strip()) == 'y':
            self.style_print("Quiting Application", "g")
            self.__del__()
            os._exit(1)

    def __del__(self):
        # Destroy the cloned table for the next time the application is activated.
        self.dbConnection.destroy("CLONE")
        # Disconnect all database connections.
        self.dbConnection.disconnect()
        self.validator.disconnect()

    def create_row(self):
        # Create Row protocol
        newRecord = []
        fieldNames = self.dbConnection.get_field_names()
        index = 0
        error = False
        return_to_menu = False
        # Enter values for each field
        while index < len(fieldNames) and not error and not return_to_menu:
            field = fieldNames[index]
            value = self.style_input("Enter value for " + str.lower(field) + ":", "c")
            value = value.strip()
            return_to_menu = self.isReturn(value)
            if not return_to_menu:
                error = not self.validator.get_rule_map()[field](value)
                if not error:
                    newRecord.append(value)
                    index += 1
        # If there is an error display it, otherwise insert the new record.
        if return_to_menu:
            self.style_print("Returning to Main Menu", "g")
        elif error:
            self.style_print(self.validator.get_format_messages()[fieldNames[index]], "r")
        else:
            table_success = self.dbConnection.insert(tuple(newRecord))
            clone_success = self.dbConnection.insert(tuple(newRecord), "CLONE")
            if table_success and clone_success:
                self.style_print("Record added successfully", "g")

    def select_rows(self):
        # Selection of Rows Protocol
        invalid = False
        end = False
        firstIteration = True
        fieldNames = self.dbConnection.get_field_names()
        msg = "Enter field to be selected. \n"
        selected_fields = set()
        select = ''
        return_to_menu = False

        # Allow user to select multiple fields
        while not invalid and not end and not return_to_menu:
            # In the first iteration, not specifying a value selects all fields.
            # Otherwise it selects all previously chosen fields.
            if firstIteration:
                select = self.style_input(msg+"(Leave blank to select all fields):\n", "c")
            else:
                select = self.style_input(msg+"(Leave blank to stop selecting)\n", "c")
            # Remove leading and trailing whitespaces
            select = select.strip()
            return_to_menu = self.isReturn(select)
            if not return_to_menu:
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
                        self.style_print("No such field "+select+". Valid fields are: "+str(fieldNames), "r")
                    else:
                        selected_fields.add(select)
        # Only allow the input of a where clause if the selected fields are valid.
        if not invalid and not return_to_menu:
            where = self.style_input("Enter selection condition \n(Leave blank if you want all records):\n", "c")
            where = None if where.strip() == '' else where.strip()
            return_to_menu = self.isReturn(where)
            if not return_to_menu:
                if select == "*":
                    selected_records = self.dbConnection.read(select, where, "CLONE")
                else:
                    selected_records = self.dbConnection.read(",".join(list(selected_fields)), where, "CLONE")

                if selected_records:
                    self.table.set_fields(selected_records.pop())
                    self.table.set_records(selected_records)
                self.table.print_table()
                self.table.clear()
        if return_to_menu:
            self.style_print("Returning to Main Menu", "g")

    def update_rows(self):
        # Update rows protocol
        field_names = self.dbConnection.get_field_names()
        invalid = False
        end = False
        field_update = {}
        return_to_menu = False
        # While we still have values to add, or do not have an invalid input.
        while not invalid and not end and not return_to_menu:
            # Select the field of which the value should be changes
            set_field = self.style_input("Select field to change value:\n(Leave blank to end changes)\n", "c")
            set_field = set_field.strip()
            return_to_menu = self.isReturn(set_field)
            if not return_to_menu:
                # Check if the field is a fieldName
                if set_field in field_names:
                    # Set a value for the field
                    set_value = self.style_input("Select value to be changed to:\n", "c*")
                    set_value = set_value.strip()
                    if self.isReturn(set_value):
                        return_to_menu = True
                    else:
                        # Check the validity of the field
                        if self.validator.get_rule_map()[set_field](set_value):
                            field_update[set_field] = set_value
                        else:
                            self.style_print(self.validator.get_format_messages()[set_field], "r")
                            invalid = True
                elif set_field == '':
                    # If no fields were added stop execution
                    if len(field_update) == 0:
                        invalid = True
                        self.style_print("No fields added for update.","r")
                    else:
                        end = True
                else:
                    invalid = True
                    self.style_print(set_field+" field does not exist.\nValid fields: "+str(field_names), "r")
        # Choose update condition
        if not invalid and not return_to_menu:
            where = self.style_input("Enter update condition:\n", "c")
            where = where.strip()
            return_to_menu = self.isReturn(where)
            if not return_to_menu:
                table_success = False
                clone_success = False
                if where == '':
                    table_success = self.dbConnection.update(field_update)
                    clone_success = self.dbConnection.update(field_update, "CLONE")
                else:
                    table_success = self.dbConnection.update(field_update, where)
                    clone_success = self.dbConnection.update(field_update, where, "CLONE")
                if table_success and clone_success:
                    self.style_print("Records updated successfully", "g*")
        if return_to_menu:
            self.style_print("Returning to Main Menu", "g")

    def delete_rows(self):
        # Delete Rows protocol
        where = self.style_input("Specify condition for records to delete (Leave blank to delete all records):\n", "c")
        where = where.strip()
        return_to_menu = self.isReturn(where)
        if not return_to_menu:
            confirm = self.style_input("Are you sure you want to delete these records? y for yes:\n", "y")
            confirm = confirm.strip()
            return_to_menu = self.isReturn(confirm)
            if not return_to_menu:
                if str.lower(confirm).strip() == 'y':
                    table_success = False
                    clone_success = False
                    if where.strip() == '':
                        table_success = self.dbConnection.delete()
                        clone_success = self.dbConnection.delete("CLONE")
                    else:
                        table_success = self.dbConnection.delete(where)
                        clone_success = self.dbConnection.delete(where, "CLONE")
                    if table_success and clone_success:
                        self.style_print("Records deleted successfully", "g*")
        if return_to_menu:
            self.style_print("Returning to Main Menu", "g")


def main():
    a = MainMenu()
    a.run()


if __name__ == "__main__":
    main()
