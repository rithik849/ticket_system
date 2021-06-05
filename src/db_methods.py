import sqlite3


# Create table
def create_table():

    conn = sqlite3.connect('test.db')

    conn.execute('''CREATE TABLE TICKETS
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DAY DATE NOT NULL,
    START_TIME TIME NOT NULL,
    DURATION TIME NOT NULL,
    MOVIE_NAME VARCHAR(50) NOT NULL,
    PRICE NUMERIC NOT NULL,
    THEATER CHAR(1) NOT NULL,
    SEAT CHAR(2) NOT NULL,
    RATING VARCHAR(3) NOT NULL
    );''')

    print("table created successfully")
    conn.commit()
    conn.close()


# Insert operation in sql. Takes the tuple of parameters as a value
def insert(values):

    try:
        conn = sqlite3.connect('test.db')
        conn.execute('''INSERT INTO TICKETS (DAY,START_TIME,DURATION,MOVIE_NAME,PRICE,THEATER,SEAT,RATING)
        VALUES ''' + str(values))
        conn.commit()
        conn.close()
        print("Record added successfully")
    except Exception as e:
        print(e)
    finally:
        conn.close()


# Add updates to records
def update(set_fields, condition=None):

    try:
        conn = sqlite3.connect('test.db')
        statement = '''UPDATE TICKETS SET ''' + set_fields
        if condition:
            statement = statement + ''' WHERE ''' + condition
        conn.execute(statement)
        conn.commit()
        conn.close()
        print("Records updated successfully")
    except Exception as e:
        print(e)
    finally:
        conn.close()


# Selection statements
def read(select="*", condition=None):
    records = None
    try:
        conn = sqlite3.connect('test.db')

        statement = '''SELECT ''' + str(select) + ''' FROM TICKETS'''

        if condition:
            statement = statement + ''' WHERE ''' + str(condition)

        result = conn.execute(statement)

        records = [list(rec) for rec in result.fetchall()]
        records = records + [[element[0] for element in result.description]]
    except Exception as e:
        print(e)
    finally:
        conn.close()

    return records


# Delete statement
def delete(condition=None):
    try:
        conn = sqlite3.connect('test.db')
        if condition:
            conn.execute('''DELETE FROM TICKETS WHERE''' + str(condition))
        else:
            conn.execute('''DELETE FROM TICKETS''')
        conn.commit()
        conn.close()
        print("Records deleted successfully")
    except Exception as e:
        print(e)
    finally:
        conn.close()


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
    # date start_time duration name price theater seat rating
    population_data = [('2021-03-01', '00:00', '02:23', 'A team', 15.00, 'A', 'A5', '3'),
                       ('2021-03-02', '04:00', '01:45', 'Random', 15.00, 'E', 'B3', '6'),
                       ('2021-03-02', '04:00', '01:45', 'Random', 8.23, 'D', 'B3', '6'),
                       ('2021-06-12', '16:30', '01:30', 'Expendables', 8.43, 'B', 'D5', '4'),
                       ('2021-05-22', '19:30', '02:00', 'A team', 9.50, 'C', 'E4', '3'),
                       ('2021-04-02', '17:20', '01:45', 'Arrow', 15.00, 'E', 'D3', '18'),
                       ('2021-03-04', '23:00', '01:45', 'Random', 15.00, 'E', 'B2', '6'),
                       ('2021-03-03', '04:00', '01:45', 'Random', 15.00, 'E', 'B3', '6'),
                       ('2021-03-05', '04:00', '01:45', 'Random', 8.23, 'D', 'B3', '6'),
                       ('2021-06-11', '16:30', '01:41', 'John Wick', 8.43, 'B', 'D5', '4')]
    for rec in population_data:
        insert(rec)
    conn.commit()
    conn.close()


# Destroy table
def destroy():
    conn = sqlite3.connect('test.db')
    conn.execute('DROP TABLE TICKETS')
    conn.close()
