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
        "CREATE TABLE IF NOT EXISTS destination(dest_id varchar(7) PRIMARY KEY, dest_name varchar(100) NOT NULL, dest_add varchar(300) NOT NULL, active boolean NOT NULL)",
        "CREATE TABLE IF NOT EXISTS pilot(pilot_id varchar(7) PRIMARY KEY, pilot_name varchar(100) NOT NULL, pilot_workday varchar(25) NOT NULL, active boolean NOT NULL)",
        "CREATE TABLE IF NOT EXISTS model_permitted_4_dest(model_id varchar(7) NOT NULL FOREIGN KEY REFERENCES aircraft_model(model_id), dest_id varchar(7) NOT NULL FOREIGN KEY REFERENCES destination(dest_id), UNIQUE(model_id, dest_id))",
        "CREATE TABLE IF NOT EXISTS pilot_trained_on_model(model_id varchar(7) NOT NULL FOREIGN KEY REFERENCES aircraft_model(model_id), pilot_id varchar(7) NOT NULL FOREIGN KEY REFERENCES pilot(pilot_id), UNIQUE(model_id, pilot_id))",
        "CREATE TABLE IF NOT EXISTS flight(flight_id varchar(7) PRIMARY KEY, model_id varchar(7) FOREIGN KEY REFERENCES aircraft_model(model_id), dest_id varchar(7) NOT NULL FOREIGN KEY REFERENCES destination(dest_id), pilot_id varchar(7) FOREIGN KEY REFERENCES pilot(pilot_id), dest_id varchar(7) NOT NULL FOREIGN KEY REFERENCES destination(dest_id), flight_schedule varchar(25), flight_status varchar(25) NOT NULL)"
    ]

    for creStmt in create_stmts:
        db_cursor.execute(creStmt)

    db_connection.commit() 


"""
The below function is to fill all the tables relevant for a design of flight management system
"""
def fill_tables(db_cursor, db_connection):

    data_model = [
        ("m_00001", "Boeing 747", True),
        ("m_00002", "Boeing 777", True),
        ("m_00003", "Boeing 787 Dreamliner", True),
        ("m_00004", "Airbus A320", True),
        ("m_00005", "Airbus A350", True),
        ("m_00006", "Airbus A380", True),
        ("m_00007", "Cessna 172", False),
        ("m_00008", "Bombardier CRJ", True),
        ("m_00009", "Boeing 737", False)
    ]

    db_cursor.executemany("INSERT INTO aircraft_model VALUES(?, ?, ?)", data_model)
    db_connection.commit() 

    data_destination = [
        ("d_00001", "Heathrow", "London, UK", True),
        ("d_00002", "London City", "London, UK", True),
        ("d_00003", "Tokyo Haneda", "Tokyo, Japan", True),
        ("d_00004", "Euro Airport", "Basel, Switzerland", True),
        ("d_00005", "Sydney", "Sydney, Australia", True),
        ("d_00006", "Munich", "Munich, Germany", True),
        ("d_00007", "San Francisco", "California, US", True),
        ("d_00008", "New Delhi", "Delhi, India", True),
        ("d_00009", "Santorini", "Santorini Islands, Greece", True),
        ("d_00010", "Changi", "Changi, Singapore", True)
    ]

    db_cursor.executemany("INSERT INTO destination VALUES(?, ?, ?, ?)", data_destination)
    db_connection.commit() 


    data_pilot = [
        ("p_00001", "Aaron Smith", "0,3,4", True),
        ("p_00002", "Adam Gilbert", "1.2.5", True),
        ("p_00003", "Jake Choo", "0,3,6", True),
        ("p_00004", "Minato", "2,5,6", True),
        ("p_00005", "Raghu Ram", "1,4,5", True),
        ("p_00006", "Rajneesh Singh", "2,5,6", True),
        ("p_00007", "Sam Fowler", "0,2,3", True),
        ("p_00008", "Jake Dhillon", "1,4,6", True),
        ("p_00009", "Jacob Doblinger", "3,5,6", True), 
        ("p_00010", "Ben Houghton", "0,2,4", True)
    ]

    db_cursor.executemany("INSERT INTO pilot VALUES(?, ?, ?, ?)", data_pilot)
    db_connection.commit() 

    data_pilotonmodel = [
        ("m_00003", "p_00009"),
        ("m_00003", "p_00004"),
        ("m_00003", "p_00003"),
        ("m_00006", "p_00006"),
        ("m_00006", "p_00010"),
        ("m_00006", "p_00009"),
        ("m_00001", "p_00004"),
        ("m_00001", "p_00003"),
        ("m_00005", "p_00010"), 
        ("m_00005", "p_00009"),
        ("m_00004", "p_00006")  
    ]

    db_cursor.executemany("INSERT INTO pilot_trained_on_model VALUES(?, ?)", data_pilotonmodel)
    db_connection.commit() 

    data_model4dest = [
        ("m_00003", "d_00009"),
        ("m_00003", "d_00004"),
        ("m_00003", "d_00003"),
        ("m_00006", "d_00006"),
        ("m_00006", "d_00010"),
        ("m_00006", "d_00009"),
        ("m_00001", "d_00004"),
        ("m_00001", "d_00003"),
        ("m_00005", "d_00010"), 
        ("m_00005", "d_00009"),
        ("m_00004", "d_00006")
    ]

    db_cursor.executemany("INSERT INTO model_permitted_4_dest VALUES(?, ?)", data_model4dest)
    db_connection.commit() 

    data_flight = [
        ("f_00001", None, "d_00009", None, None, "Planning"),
        ("f_00002", None, "d_00004", None, None, "Planning"),
        ("f_00003", None, "d_00003", None, None, "Planning"),
        ("f_00004", "m_00006", "d_00006", "p_00010", None, "To Schedule"),
        ("f_00005", "m_00005", "d_00010", "p_00009", "7/5/2025", "Scheduled"),
        ("f_00006", None, "d_00009", None, None, "Planning"),
        ("f_00007", None, "d_00004", None, None, "Planning"),
        ("f_00008", None, "d_00003", None, None, "Planning"),
        ("f_00009", None, "d_00010", None, None, "Planning"), 
        ("f_00010", None, "d_00009", None, None, "Planning"),
        ("f_00011", None, "d_00006", None, None, "Planning")
    ]

    db_cursor.executemany("INSERT INTO flight VALUES(?, ?, ?, ?, ?, ?)", data_flight)
    db_connection.commit() 

    db_connection.close()


"""
The below function is to retrieve ddata from the flight table based on conditions
"""

def retrive_flight(db_cursor, dest, status, depDate):
    selectQuery = "SELECT * FROM flight"
    addAnd = False
    if dest is not "" or status is not "" or depDate is not "":
        selectQuery = selectQuery + " where "
    if dest is not "":
        if addAnd == True:
            selectQuery = selectQuery + " and dest_id = " + dest
        else:
            selectQuery = selectQuery + " dest_id = " + dest
        addAnd = True
    if status is not "":
        if addAnd == True:
            selectQuery = selectQuery + " and flight_status = " + status
        else:
            selectQuery = selectQuery + " flight_status = " + status
        addAnd = True
    if depDate is not "":
        if addAnd == True:
            selectQuery = selectQuery + " and flight_schedule = " + depDate
        else:
            selectQuery = selectQuery + " flight_schedule = " + depDate
        addAnd = True
    res = db_cursor.execute(selectQuery)
    res.fetchall()
    print(res.fetchall())


"""
The below function is to retrieve ddata from the flight table based on conditions
"""
def modify_flight_schedule(db_cursor, flightId, depDate, status):
    res = db_cursor.execute("SELECT * FROM flight")
    res.fetchall()

    

"""
The below function is to retrieve ddata from the flight table based on conditions
"""
def assign_pilot(db_cursor, flightId, pilotId, random):
    res = db_cursor.execute("SELECT * FROM flight")
    res.fetchall()

    
  

"""
The below function is to retrieve ddata from the flight table based on conditions
"""
def manage_destination(db_cursor, destId, destName, destAdd, destStatus):
    res = db_cursor.execute("SELECT * FROM flight")
    res.fetchall()

    


"""
The below function is to retrieve ddata from the flight table based on conditions
"""
def view_report(db_cursor, reportType):
    res = db_cursor.execute("SELECT * FROM flight")
    res.fetchall()

    
    

"""
The below function is to retrieve ddata from the flight table based on conditions
"""
db_connection = sqlite3.connect(db_file)
db_cursor = db_connection.cursor()

"""
The below function is to retrieve ddata from the flight table based on conditions
"""
end_program = False

while not end_program:
    print('''
          Welcome to the flight management system!! Please choose your operation

          1. Retrieve Flight details
          2. Modify Schedule
          3. Pilot Assignment
          4. Destination Management
          5. Generate Report
          6. Exit

          ''')
    
    response = input("Your selection : ")
    try:
        selected_option = int(response)
        if selected_option == 1:
            print('''
                Please choose your filter condition or enter empty string to not filter based on that column
            ''')
            resDestination = input("Which destination to filter by : ")
            resStatus = input("Which status to filter by : ")
            resDepDate = input("Which departure date to filter by : ")

            retrive_flight(db_cursor, resDestination, resStatus, resDepDate)

        elif selected_option == 2:
            print('''
                Please fill the new schedule and/or status for the flight you want to update
            ''')
            resFlight = input("Which flight do you want to update : ")
            resDepDate = input("Which departure date to filter by : ")
            resStatus = input("Which status to filter by : ")
            
            modify_flight_schedule(db_cursor, resFlight, resStatus, resDepDate)

        elif selected_option == 3:
            print('''
                Please fill the pilot id or choose random pilot for the flight you want to update
            ''')
            resFlight = input("Which flight do you want to update : ")
            resRandom = input("Would you like to randomly choose a pilot(Y/N) : ")
            if resRandom == "N":
                resPilot = input("Which pilot to add to flight : ")
            else:
                resPilot = ""
            
            assign_pilot(db_cursor, resFlight, resPilot, resRandom)

        elif selected_option == 4:
            print('''
                Please fill the destination details to create or update or inactivate
            ''')
            resDestId = input("Which destination do you want to update. If left blank it will create a new destination : ")
            resDestName = input("Destination Name : ")
            resDestAddress = input("Destination Address : ")
            resDestStatus = input("Would you like to randomly choose a pilot(Y/N) : ")
                        
            manage_destination(db_cursor, resDestId, resDestName, resDestAddress, resDestStatus)

        elif selected_option == 5:
            print('''
                Please choose the type of report to generate!
                  
                1. Destination Based
                2. Pilot Based
                3. OverAll 
               
            ''')
            resReportType = input("Report type : ")
            
            view_report(db_cursor, resReportType)

        elif selected_option == 6:
            end_program = True
            break
    except:
        print('''Wrong Selection! Exiting!''')
        end_program = True
        break

    db_connection.close()
