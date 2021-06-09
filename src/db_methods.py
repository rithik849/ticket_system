import sqlite3


class DatabaseAccessor:

    def __init__(self):
        self.conn = sqlite3.connect("test.db")

    # Create table
    def create_table(self):

        self.conn.execute('''CREATE TABLE TICKETS
        (ID CHAR(5) PRIMARY KEY,
        DAY DATE NOT NULL,
        START_TIME TIME NOT NULL,
        DURATION TIME NOT NULL,
        MOVIE_NAME VARCHAR(50) NOT NULL,
        PRICE FLOAT NOT NULL,
        THEATER CHAR(1) NOT NULL,
        SEAT CHAR(2) NOT NULL,
        RATING VARCHAR(3) NOT NULL
        );''')

        print("table created successfully")
        self.conn.commit()

    def hasTable(self, table_name="TICKETS"):
        table_exists = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"
                                         + table_name + "'")
        return bool(table_exists.fetchall())

    def clone_table(self):
        self.conn.execute('''CREATE TABLE CLONE AS SELECT * FROM TICKETS''')
        self.conn.execute('''DELETE FROM CLONE''')
        self.conn.commit()

    def insert_rows(self, records, table_name="TICKETS"):
        try:
            if records != []:
                self.conn.execute('''INSERT INTO ''' + table_name +
                                  '''(ID,DAY,START_TIME,DURATION,MOVIE_NAME,PRICE,THEATER,SEAT,RATING) 
                                  VALUES ''' + str(records)[1: -1])
                self.conn.commit()
        except Exception as e:
            print(e)
            print("read")

    # Insert operation in sql. Takes the tuple of parameters as a value
    def insert(self, values, table_name="TICKETS"):

        try:
            # conn = sqlite3.connect('test.db')
            self.conn.execute('''INSERT INTO ''' + table_name + \
                              ''' (ID,DAY,START_TIME,DURATION,MOVIE_NAME,PRICE,THEATER,SEAT,RATING)
            VALUES ''' + str(values))
            self.conn.commit()
            print("Record added successfully")
        except Exception as e:
            print(e)
        # finally:
        #     conn.close()

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
            print(statement)
            self.conn.execute(statement)
            self.conn.commit()
            print("Records updated successfully")
        except Exception as e:
            print(e)

    # Selection statements
    def read(self, select="*", condition=None, table_name="TICKETS"):
        records = None
        try:
            # conn = sqlite3.connect('test.db')

            statement = '''SELECT ''' + str(select) + ''' FROM ''' + table_name

            if condition:
                statement = statement + ''' WHERE ''' + str(condition)

            result = self.conn.execute(statement)

            # records = [list(rec) for rec in result.fetchall()]
            records = result.fetchall()
            records = records + [[element[0] for element in result.description]]
        except Exception as e:
            print(e)
        # finally:
        #     conn.close()

        return records

    # Delete statement
    def delete(self, condition=None, table_name="TICKETS"):
        try:
            # conn = sqlite3.connect('test.db')
            if condition:
                self.conn.execute('''DELETE FROM ''' + table_name + ''' WHERE''' + str(condition))
            else:
                self.conn.execute('''DELETE FROM ''' + table_name)
            self.conn.commit()
            # conn.close()
            print("Records deleted successfully")
        except Exception as e:
            print(e)
        # finally:
        #     conn.close()

    def get_number_of_rows(self, table_name="TICKETS"):
        result = [[0]]
        try:
            result = self.conn.execute('''SELECT COUNT(*) FROM ''' + table_name)
        except Exception as e:
            print(e)

        return result.fetchone()[0]

    # Returns the name of each field
    def get_field_names(self):

        # conn = sqlite3.connect('test.db')
        field_names = [str(rec[1]) for rec in self.conn.execute('''PRAGMA table_info(TICKETS);''')]
        # conn.close()
        return field_names

    # Returns the type of each corresponding field
    def get_field_types(self):
        # conn = sqlite3.connect('test.db')
        field_types = [str(rec[2]) for rec in self.conn.execute('''PRAGMA table_info(TICKETS);''')]
        # conn.close()
        return field_types

    # Populate table with test data
    def populate(self):
        # conn = sqlite3.connect('test.db')
        # date start_time duration name price theater seat rating
        population_data = [('A1323', '2021-03-01', '00:00', '02:23', 'A team', 15.00, 'A', 'A5', 'U'),
                           ('a2343', '2021-03-02', '04:00', '01:45', 'Random', 15.00, 'E', 'B3', 'PG'),
                           ('a1232', '2021-03-02', '04:00', '01:45', 'Random', 8.23, 'D', 'B3', 'PG'),
                           ('a9886', '2021-06-12', '16:30', '01:30', 'Expendables', 8.43, 'B', 'D5', '12'),
                           ('ade9r', '2021-05-22', '19:30', '02:00', 'A team', 9.50, 'C', 'E4', 'U'),
                           ('arfd0', '2021-04-02', '17:20', '01:45', 'Arrow', 15.00, 'E', 'D3', '18'),
                           ('awsd3', '2021-03-04', '23:00', '01:45', 'Random', 15.00, 'E', 'B2', 'U'),
                           ('asdf3', '2021-03-03', '04:00', '01:45', 'Random', 15.00, 'E', 'B3', 'U'),
                           ('wasd1', '2021-03-05', '04:00', '01:45', 'Random', 8.23, 'D', 'B3', '15'),
                           ('qer2W', '2021-06-11', '16:30', '01:41', 'John Wick', 8.43, 'B', 'D5', '18')]
        self.insert_rows(population_data)
        self.conn.commit()
        # conn.close()

    # Destroy table
    def destroy(self, table_name="TICKETS"):
        # conn = sqlite3.connect('test.db')
        self.conn.execute('DROP TABLE ' + table_name)
        # conn.close()

    def __del__(self):
        self.disconnect()

    # Called when quiting the application
    def disconnect(self):
        self.conn.close()
