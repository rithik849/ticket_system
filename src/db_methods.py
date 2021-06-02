import sqlite3

tableName = ""


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


def insert(values):

    conn = sqlite3.connect('test.db')

    conn.execute('''INSERT INTO TICKETS (DATE,START_TIME,DURATION,MOVIE_NAME,PRICE,SEAT,RATING)
    VALUES''' + str(values))
    conn.commit()
    conn.close()
    print("Record added successfully")


def update(condition):

    conn = sqlite3.connect('test.db')
    conn.execute('''UPDATE TICKETS WHERE ''' + condition)
    conn.close()
    print("Records updated successfully")


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


def delete(condition):

    conn = sqlite3.connect('test.db')
    conn.execute('''DELETE FROM TICKETS WHERE''' + str(condition))
    conn.close()
    print("Records deleted successfully")


def get_fields():

    conn = sqlite3.connect('test.db')
    field_names = [(rec[1], rec[2]) for rec in conn.execute('''PRAGMA table_info(TICKETS);''')]
    conn.close()
    return field_names
