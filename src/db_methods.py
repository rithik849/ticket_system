import sqlite3


class DatabaseAccessor:

    def __init__(self):
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

    # Create table
    def create_table(self):

        self.conn.execute(self.table)

        print("table created successfully")
        self.conn.commit()

    def hasTable(self, table_name="TICKETS"):
        table_exists = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"
                                         + table_name + "'")
        return bool(table_exists.fetchall())

    def clone_table(self):
        self.conn.execute(self.table.replace("TICKETS", "CLONE"))
        self.conn.commit()

    def insert_rows(self, records, table_name="TICKETS"):
        try:
            if records:
                self.conn.execute('''INSERT INTO ''' + table_name +
                                  '''(INCIDENT_ID,DAY,INCIDENT_TIME,RAISED_BY,STATUS,TEAM,ASSIGNED_TO,PRIORITY) 
                                  VALUES ''' + str(records)[1: -1])
                self.conn.commit()
        except Exception as e:
            if table_name == "TICKETS":
                print(e)

    # Insert operation in sql. Takes the tuple of parameters as a value
    def insert(self, values, table_name="TICKETS"):

        try:
            # conn = sqlite3.connect('test.db')
            self.conn.execute('''INSERT INTO ''' + table_name +
                              ''' (INCIDENT_ID,DAY,INCIDENT_TIME,RAISED_BY,STATUS,TEAM,ASSIGNED_TO,PRIORITY)
            VALUES ''' + str(values))
            self.conn.commit()
            return True
        except Exception as e:
            if table_name == "TICKETS":
                print(e)
            return False

    # Add updates to records
    def update(self, field_updates, condition=None, table_name="TICKETS"):

        try:
            setString = ""
            for key in field_updates.keys():
                setString += str(key)+"='"+str(field_updates[key])+"', "
            setString = setString[:-2]
            statement = '''UPDATE ''' + table_name + ''' SET ''' + setString
            if condition:
                statement = statement + ''' WHERE ''' + condition
            self.conn.execute(statement)
            self.conn.commit()
            return True
        except Exception as e:
            if table_name == "TICKETS":
                print(e)
            return False

    # Selection statements
    def read(self, select="*", condition=None, table_name="TICKETS"):
        records = None
        try:
            # conn = sqlite3.connect('test.db')

            statement = '''SELECT ''' + str(select) + ''' FROM ''' + table_name

            if condition:
                statement = statement + ''' WHERE ''' + str(condition)

            result = self.conn.execute(statement)

            records = result.fetchall()
            records = records + [[element[0] for element in result.description]]
        except Exception as e:
            if table_name == "TICKETS":
                print(e)

        return records

    # Delete statement
    def delete(self, condition=None, table_name="TICKETS"):
        try:
            # conn = sqlite3.connect('test.db')
            if condition:
                self.conn.execute('''DELETE FROM ''' + table_name + ''' WHERE ''' + str(condition))
            else:
                self.conn.execute('''DELETE FROM ''' + table_name)
            self.conn.commit()
            return True
        except Exception as e:
            if table_name == "TICKETS":
                print(e)
            return False

    def get_number_of_rows(self, table_name="TICKETS"):
        result = [[0]]
        try:
            result = self.conn.execute('''SELECT COUNT(*) FROM ''' + table_name)
        except Exception as e:
            if table_name == "TICKETS":
                print(e)

        return result.fetchone()[0]

    # Returns the name of each field
    def get_field_names(self):

        # conn = sqlite3.connect('test.db')
        field_names = [str(rec[1]) for rec in self.conn.execute('''PRAGMA table_info(TICKETS);''')]
        return field_names

    # Returns the type of each corresponding field
    def get_field_types(self):
        # conn = sqlite3.connect('test.db')
        field_types = [str(rec[2]) for rec in self.conn.execute('''PRAGMA table_info(TICKETS);''')]
        return field_types

    # Populate table with test data
    def populate(self):
        # conn = sqlite3.connect('test.db')
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
                           ('inc9', '2021-06-11', '16:30', 'emp66', "Complete", 'Linux Team', 'emp10', '1')]
        self.insert_rows(population_data)
        self.conn.commit()
        # conn.close()

    # Destroy table
    def destroy(self, table_name="TICKETS"):
        # conn = sqlite3.connect('test.db')
        self.conn.execute('DROP TABLE ' + table_name)
        # self.conn.commit()
        # conn.close()

    def __del__(self):
        self.disconnect()

    # Called when quiting the application
    def disconnect(self):
        self.conn.close()
