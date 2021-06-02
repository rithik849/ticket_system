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
    PRICE NUMERIC(15,2) NOT NULL,
    STUDIO CHAR(1),
    SEAT CHAR(2) NOT NULL,
    RATING VARCHAR(2) NOT NULL
    );''')

    print("table created successfully")
    conn.commit()
    conn.close()


# Insert operation in sql. Takes the tuple of parameters as a value


def insert(values):

    conn = sqlite3.connect('test.db')

    conn.execute('''INSERT INTO TICKETS (DATE,START_TIME,DURATION,MOVIE_NAME,PRICE,STUDIO,SEAT,RATING)
    VALUES ''' + str(values))
    conn.commit()
    conn.close()
    print("Record added successfully")

# Add updates to records


def update(set_fields, condition=None):

    conn = sqlite3.connect('test.db')
    statement = '''UPDATE TICKETS SET ''' + set_fields
    if condition:
        statement = statement + ''' WHERE ''' + condition
    conn.execute(statement)
    conn.close()
    print("Records updated successfully")

# Selection statements


def read(select="*", condition=None):

    conn = sqlite3.connect('test.db')

    statement = '''SELECT ''' + str(select) + '''FROM TICKETS'''

    if condition:
        statement = statement + ''' WHERE ''' + str(condition)

    result = conn.execute(statement)
    result = [tuple(str(element) if isinstance(element, unicode) else element for element in rec) for rec in result]

    conn.close()

    return result

# Delete statement


def delete(condition):

    conn = sqlite3.connect('test.db')
    if condition:
        conn.execute('''DELETE FROM TICKETS WHERE''' + str(condition))
    else:
        conn.execute('''DELETE FROM TICKETS''')
    conn.close()
    print("Records deleted successfully")

# Returns the name of each field


def get_field_names():

    conn = sqlite3.connect('test.db')
    field_names = [str(rec[1]) for rec in conn.execute('''PRAGMA table_info(TICKETS);''')]
    conn.close()
    return field_names

# Returns the type of each corresponding field


def get_field_types():
    conn = sqlite3.connect('test.db')
    field_types = [str(rec[2]) for rec in conn.execute('''PRAGMA table_info(TICKETS);''')]
    conn.close()
    return field_types

# Populate table with test data


def populate():
    conn = sqlite3.connect('test.db')
    # date start_time duration name price studio seat rating
    population_data = [('2021-03-01', '00:00', '2:23', 'A team', 15.00, 'A', 'A5', '3'),
                       ('2021-03-02', '4:00', '1:45', 'Random', 15, 'E', 'B3', '3'),
                       ('2021-03-02', '4:00', '1:45', 'Random', 8, 'I', 'B3', '6')]
    for rec in population_data:
        insert(rec)
    conn.commit()
    conn.close()

# Destroy table


def destroy():
    conn = sqlite3.connect('test.db')
    conn.execute('DROP TABLE TICKETS')
    conn.close()
