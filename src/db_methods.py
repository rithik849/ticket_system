import sqlite3
from UI import UI


class DatabaseAccessor(UI):

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect("test.db")
        self.table = '''CREATE TABLE TICKETS
        (INCIDENT_ID VARCHAR(10) PRIMARY KEY,
        DAY DATE NOT NULL,
        INCIDENT_TIME TIME NOT NULL,
        RAISED_BY CHAR(5) NOT NULL,
        STATUS VARCHAR(11) NOT NULL,
        TEAM VARCHAR(50) NOT NULL,
        ASSIGNED_TO CHAR(5) NOT NULL,
        PRIORITY INTEGER NOT NULL);'''

    # Create a table
    def create_table(self, table_name=None):
        if table_name:
            table = self.table.replace("TICKETS", table_name)
        else:
            table = self.table

        self.conn.execute(table)

        self.style_print("table created successfully", "g")
        self.conn.commit()

    # Check if a table exists
    def hasTable(self, table_name):
        table_exists = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"
                                         + table_name + "'")
        return bool(table_exists.fetchall())

    # Insert a list of records into a table
    def insert_rows(self, records, table_name="TICKETS"):
        try:
            if records:
                self.conn.execute('''INSERT INTO ''' + table_name +
                                  '''(INCIDENT_ID,DAY,INCIDENT_TIME,RAISED_BY,STATUS,TEAM,ASSIGNED_TO,PRIORITY) 
                                  VALUES ''' + str(records)[1: -1])
                self.conn.commit()
        except Exception as e:
            if table_name == "TICKETS":
                self.style_print(e, "r")

    # Insert operation in sql. Takes the tuple of parameters as a value
    def insert(self, values, table_name="TICKETS"):

        try:
            self.conn.execute('''INSERT INTO ''' + table_name +
                              ''' (INCIDENT_ID,DAY,INCIDENT_TIME,RAISED_BY,STATUS,TEAM,ASSIGNED_TO,PRIORITY)
            VALUES ''' + str(values))
            self.conn.commit()
            return True
        except Exception as e:
            if table_name == "TICKETS":
                self.style_print(e, "r")
            return False

    # Add updates to records
    def update(self, field_updates, condition=None, error_ids=tuple(), table_name="TICKETS"):

        try:
            # Create the assignments for updates
            setString = [str(key)+"='"+str(field_updates[key])+"'" for key in field_updates.keys()]

            # Join the set strings.
            setString = ", ".join(setString)
            statement = '''UPDATE ''' + table_name + ''' SET ''' + setString
            statement = self.add_where_statement(statement, condition, error_ids)

            self.conn.execute(statement)
            self.conn.commit()
            return True
        except Exception as e:
            if table_name == "TICKETS":
                self.style_print(e, "r")
            return False

    # Selection statements
    def read(self, select="*", condition=None, error_ids=tuple(), table_name="TICKETS"):
        records = None
        try:
            statement = '''SELECT ''' + str(select) + ''' FROM ''' + table_name
            statement = self.add_where_statement(statement, condition, error_ids)
            statement += ''' ORDER BY INCIDENT_ID'''

            result = self.conn.execute(statement)

            records = result.fetchall()
            records = records + [[element[0] for element in result.description]]
        except Exception as e:
            if table_name == "TICKETS":
                self.style_print(e, "r")

        return records

    # Delete statement
    def delete(self, condition=None, error_ids=tuple(), table_name="TICKETS"):
        try:
            statement = '''DELETE FROM ''' + table_name
            statement = self.add_where_statement(statement, condition, error_ids)

            self.conn.execute(statement)
            self.conn.commit()
            return True
        except Exception as e:
            if table_name == "TICKETS":
                self.style_print(e, "r")
            return False

    # Where statement that takes a condition and adds the conditions to ignore a number of records.
    def add_where_statement(self, statement="", condition=None, error_ids=tuple()):
        # If there are erroneous records ignore them
        if len(error_ids) > 0:
            # Create collection of erroneous primary key values
            error_id_statement = "(" + ",".join(['\'' + err + '\'' for err in error_ids]) + ")"
            statement += ''' WHERE (INCIDENT_ID NOT IN ''' + error_id_statement + ''')'''
            # Add a condition if available
            if condition:
                statement += ''' AND (''' + condition + ''')'''
        elif condition:
            # Add condition if available
            statement = statement + ''' WHERE ''' + condition
        return statement

    # Returns the number of rows in a table.
    def get_number_of_rows(self, table_name="TICKETS"):
        result = 0
        try:
            result = self.conn.execute('''SELECT COUNT(*) FROM ''' + table_name)
            return result.fetchone()[0]
        except Exception as e:
            if table_name == "TICKETS":
                self.style_print(e, "r")

        return result

    # Returns the name of each field
    def get_field_names(self):
        field_names = [str(rec[1]) for rec in self.conn.execute('''PRAGMA table_info(TICKETS);''')]
        return field_names

    # Returns the type of each corresponding field
    def get_field_types(self):
        # conn = sqlite3.connect('test.db')
        field_types = [str(rec[2]) for rec in self.conn.execute('''PRAGMA table_info(TICKETS);''')]
        return field_types

    # Populate table with test data
    def populate(self):
        # incident_id, day, incident_time, raised_by, status, group, assigned_to, priority
        population_data = [('inc0', '2021-03-01', '00:00', 'emp00', "In Progress", 'Wintel Group', 'emp44', '2'),
                           ('inc1', '2021-03-02', '04:00', 'emp01', "In Progress", 'Linux Team', 'emp47', '3'),
                           ('inc2', '2021-03-02', '04:00', 'emp10', "New", 'Application Team', 'emp07', '1'),
                           ('inc3', '2021-06-12', '16:30', 'emp11', "Complete", 'Network Team', 'emp49', '2'),
                           ('inc4', '2021-05-22', '19:30', 'emp23', "New", 'Windows Team', 'emp99', '2'),
                           ('inc5', '2021-04-02', '17:20', 'emp34', "Complete", 'Mac/iOS Team', 'emp32', '3'),
                           ('inc6', '2021-03-04', '23:00', 'emp67', "Complete", 'Android Team', 'emp44', '3'),
                           ('inc7', '2021-03-03', '04:00', 'emp34', "New", 'Fullstack Team', 'emp12', '2'),
                           ('inc8', '2021-03-05', '04:00', 'emp43', "In Progress", 'All', 'emp43', '2'),
                           ('inc9', '2021-06-11', '16:30', 'emp66', "Complete", 'Linux Team', 'emp10', '2')]
        self.insert_rows(population_data)
        self.conn.commit()

    # Destroy table
    def destroy(self, table_name="TICKETS"):
        self.conn.execute('DROP TABLE ' + table_name)
        self.conn.commit()

    def __del__(self):
        self.disconnect()

    # Called when quiting the application
    def disconnect(self):
        self.conn.close()

    # Called during testing
    def reconnect(self):
        # Disconnect any previous connection safely, before reconnecting.
        self.disconnect()
        self.conn = sqlite3.connect("test.db")
