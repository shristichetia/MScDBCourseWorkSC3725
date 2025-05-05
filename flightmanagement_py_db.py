import sqlite3
#above statement is used to import the sqlite3 libraries

"""
The below 3 line of codes is to establish connection with the db file from the python file
"""
db_file = "flightmanagement.db"
db_connection = sqlite3.connect(db_file)
db_cursor = db_connection.cursor()

"""
The below function is to create all the tables relevant for a design of flight management system
"""

def create_tables(db_cursor):
    create_stmts = [
        "CREATE TABLE IF NOT EXISTS aircraft_model(model_id varchar(7) PRIMARY KEY, model_name varchar(100) NOT NULL, in_use boolean NOT NULL)",
        "CREATE TABLE IF NOT EXISTS destination(dest_id varchar(7) PRIMARY KEY, dest_name varchar(100) NOT NULL, dest_add varchar(300) NOT NULL)",
        "CREATE TABLE IF NOT EXISTS pilot(pilot_id varchar(7) PRIMARY KEY, pilot_name varchar(100) NOT NULL, pilot_workday varchar(25) NOT NULL, active boolean NOT NULL)",
        "CREATE TABLE IF NOT EXISTS model_permitted_4_dest(md_id varchar(8) PRIMARY KEY, model_id varchar(7) NOT NULL FOREIGN KEY REFERENCES aircraft_model(model_id), dest_id varchar(7) NOT NULL FOREIGN KEY REFERENCES destination(dest_id))",
        "CREATE TABLE IF NOT EXISTS pilot_trained_on_model(pm_id varchar(8) PRIMARY KEY, model_id varchar(7) NOT NULL FOREIGN KEY REFERENCES aircraft_model(model_id), pilot_id varchar(7) NOT NULL FOREIGN KEY REFERENCES pilot(pilot_id))",
        "CREATE TABLE IF NOT EXISTS flight(flight_id varchar(7) PRIMARY KEY, model_id varchar(7) FOREIGN KEY REFERENCES aircraft_model(model_id), pilot_id varchar(7) FOREIGN KEY REFERENCES pilot(pilot_id), dest_id varchar(7) NOT NULL FOREIGN KEY REFERENCES destination(dest_id), flight_schedule varchar(3), flight_status varchar(25) NOT NULL)"
    ]

    for creStmt in create_stmts:
        db_cursor.execute(creStmt)


def fill_tables(db_cursor, db_connection):

    data_model = [
        ("m_00001", "Boeing 747", True),
        ("m_00002", "Boeing 777", True),
        ("m_00003", "Boeing 787 Dreamliner", True),
        ("m_00004", "Airbus A320", True),
        ("m_00005", "Airbus A350", True),
        ("m_00006", "Airbus A380", True),
        ("m_00007", "Cessna 172", True),
        ("m_00008", "Bombardier CRJ", True),
        ("m_00009", "Boeing 737", False)
    ]

    db_cursor.executemany("INSERT INTO aircraft_model VALUES(?, ?, ?)", data_model)

    data_destination = [
        ("d_00001", "Heathrow", "London, UK"),
        ("d_00002", "London City", "London, UK"),
        ("d_00003", "Tokyo Haneda", "Tokyo, Japan"),
        ("d_00004", "Euro Airport", "Basel, Switzerland"),
        ("d_00005", "Sydney", "Sydney, Australia"),
        ("d_00006", "Munich", "Munich, Germany"),
        ("d_00007", "San Francisco", "California, US"),
        ("d_00008", "New Delhi", "Delhi, India"),
        ("d_00009", "Santorini", "Santorini Islands, Greece"),
        ("d_00010", "Changi", "Changi, Singapore")
    ]

    db_cursor.executemany("INSERT INTO destination VALUES(?, ?, ?)", data_destination)


    data_pilot = [
        ("p_00001", "Aaron Smith", "0,3,4", True),
        ("p_00002", "Adam Gilbert", "1.2.5", True),
        ("p_00003", "Jake Choo", "0,3,6", True),
        ("p_00004", "Minato", "2,5,6", True),
        ("p_00005", "Raghu Ram", "1,4,5", True),
        ("p_00006", "Rajneesh Singh", "2,5,6", True),
        ("p_00007", "Sam Fowler", "0,2,3", True),
        ("p_00008", "Jake Dhillon", "1,4,6", True),
        ("p_00009", "SantoriniJacob Doblinger", "3,5,6", True), 
        ("p_00010", "Ben Houghton", "0,2,4", True)
    ]

    db_cursor.executemany("INSERT INTO pilot VALUES(?, ?, ?, ?)", data_pilot)

    db_connection.commit() 

