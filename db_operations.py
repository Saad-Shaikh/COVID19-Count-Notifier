import sqlite3

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('covidinfo.db')
    except:
        print("Could not connect to database!")

    return conn


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS state_info")
    cursor.execute("""CREATE TABLE state_info(
                    state TEXT PRIMARY KEY,
                    total INT,
                    active INT,
                    deceased INT
                    )""")

    cursor.execute("DROP TABLE IF EXISTS city_info")
    cursor.execute("""CREATE TABLE city_info(
                    city TEXT PRIMARY KEY,
                    total INT,
                    active INT,
                    deceased INT
                    )""")
    
    conn.commit()


def close_connection(conn):
    if(conn is not None):
        conn.close()


def delete_state_data(conn, state):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM state_info WHERE state = '" + state + "'")
    conn.commit()


def delete_city_data(conn, city):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM city_info WHERE city = '" + city + "'")
    conn.commit()


def read_city_data(conn, city):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM city_info WHERE city = '" + city + "'")
    result = cursor.fetchone()
    if(result is None):
        return (city, 0, 0, 0)
    
    return result


def read_state_data(conn, state):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM state_info WHERE state = '" + state + "'")
    result = cursor.fetchone()
    if(result is None):
        return (state, 0, 0, 0)
    
    return result


def write_city_data(conn, city_data):
    cursor = conn.cursor()    
    cursor.execute(("INSERT INTO city_info(city, total, active, deceased) " +
                    "VALUES('" + city_data[0] + "'" +
                    ", " + str(city_data[1]) +
                    ", " + str(city_data[2]) +
                    ", " + str(city_data[3]) +
                    ")"
                    ))
    conn.commit()


def write_state_data(conn, state_data):
    cursor = conn.cursor()    
    cursor.execute(("INSERT INTO state_info(state, total, active, deceased) " +
                    "VALUES('" + state_data[0] + "'" +
                    ", " + state_data[1] +
                    ", " + state_data[2] +
                    ", " + state_data[3] +
                    ")"
                    ))
    conn.commit()


# only run this file when creating the database for the first time
# it will create a new db file with blank tables
if __name__ == '__main__':
    conn = create_connection()
    create_tables(conn)
    close_connection(conn)
