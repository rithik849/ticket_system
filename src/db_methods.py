import sqlite3

tableName = ""

# Create table
def create_table():

    conn = sqlite3.connect('test.db')

    conn.execute('''CREATE TABLE TICKETS
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATE DATE NOT NULL,
    START_TIME TIME NOT NULL,
    DURATION TIME NOT NULL,
    MOVIE_NAME VARCHAR(50) NOT NULL,
    PRICE decimal(15,2) NOT NULL,
    SEAT CHAR(2) NOT NULL,
    RATING VARCHAR(2) NOT NULL
    );''')

    print("table created successfully")
    conn.commit()
    conn.close()

# Insert operation in sql. Takes the tuple of parameters as a value
def insert(values):

    conn = sqlite3.connect('test.db')

    conn.execute('''INSERT INTO TICKETS (DATE,START_TIME,DURATION,MOVIE_NAME,PRICE,SEAT,RATING)
    VALUES''' + str(values))
    conn.commit()
    conn.close()
    print("Record added successfully")

# Add updates to records
def update(set_fields,condition):

    conn = sqlite3.connect('test.db')
    conn.execute('''UPDATE TICKETS SET ''' + set_fields + '''WHERE ''' + condition)
    conn.close()
    print("Records updated successfully")

# Selection statements
def read(select, condition=None):

    conn = sqlite3.connect('test.db')

    if condition:
        statement = '''SELECT ''' + str(select) + '''FROM TICKETS WHERE ''' + str(condition)
    else:
        statement = '''SELECT ''' + str(select) + '''FROM TICKETS'''

    result = conn.execute(statement)
    result = [rec for rec in result]

    conn.close()

    return result

# Delete statement
def delete(condition):

    conn = sqlite3.connect('test.db')
    conn.execute('''DELETE FROM TICKETS WHERE''' + str(condition))
    conn.close()
    print("Records deleted successfully")

# Returns the name of each field and their type in sql
def get_fields():

    conn = sqlite3.connect('test.db')
    field_names = [(rec[1], rec[2]) for rec in conn.execute('''PRAGMA table_info(TICKETS);''')]
    conn.close()
    return field_names
