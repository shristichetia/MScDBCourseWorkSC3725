import sqlite3
import datetime
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
        "CREATE TABLE IF NOT EXISTS aircraft_model(model_id INTEGER PRIMARY KEY, model_name varchar(100) NOT NULL, in_use boolean NOT NULL)",
        "CREATE TABLE IF NOT EXISTS destination(dest_id INTEGER PRIMARY KEY, dest_name varchar(100) NOT NULL, dest_add varchar(300) NOT NULL, active boolean NOT NULL)",
        "CREATE TABLE IF NOT EXISTS pilot(pilot_id INTEGER PRIMARY KEY, pilot_name varchar(100) NOT NULL, pilot_workday varchar(25) NOT NULL, active boolean NOT NULL)",
        "CREATE TABLE IF NOT EXISTS model_permitted_4_dest(model_id INTEGER NOT NULL FOREIGN KEY REFERENCES aircraft_model(model_id), dest_id INTEGER NOT NULL FOREIGN KEY REFERENCES destination(dest_id), UNIQUE(model_id, dest_id))",
        "CREATE TABLE IF NOT EXISTS pilot_trained_on_model(model_id INTEGER NOT NULL FOREIGN KEY REFERENCES aircraft_model(model_id), pilot_id INTEGER NOT NULL FOREIGN KEY REFERENCES pilot(pilot_id), UNIQUE(model_id, pilot_id))",
        "CREATE TABLE IF NOT EXISTS flight(flight_id INTEGER PRIMARY KEY, model_id INTEGER FOREIGN KEY REFERENCES aircraft_model(model_id), dest_id INTEGER NOT NULL FOREIGN KEY REFERENCES destination(dest_id), pilot_id INTEGER FOREIGN KEY REFERENCES pilot(pilot_id), flight_schedule varchar(25), flight_status varchar(25) NOT NULL)"
    ]

    for creStmt in create_stmts:
        db_cursor.execute(creStmt)

    db_connection.commit() 


"""
The below function is to fill all the tables relevant for a design of flight management system
"""
def fill_tables(db_cursor, db_connection):

    data_model = [
        ("1", "Boeing 747", True),
        ("2", "Boeing 777", True),
        ("3", "Boeing 787 Dreamliner", True),
        ("4", "Airbus A320", True),
        ("5", "Airbus A350", True),
        ("6", "Airbus A380", True),
        ("7", "Cessna 172", False),
        ("8", "Bombardier CRJ", True),
        ("9", "Boeing 737", False)
    ]

    db_cursor.executemany("INSERT INTO aircraft_model VALUES(?, ?, ?)", data_model)
    db_connection.commit() 

    data_destination = [
        ("1", "Heathrow", "London, UK", True),
        ("2", "London City", "London, UK", True),
        ("3", "Tokyo Haneda", "Tokyo, Japan", True),
        ("4", "Euro Airport", "Basel, Switzerland", True),
        ("5", "Sydney", "Sydney, Australia", True),
        ("6", "Munich", "Munich, Germany", True),
        ("7", "San Francisco", "California, US", True),
        ("7", "New Delhi", "Delhi, India", True),
        ("9", "Santorini", "Santorini Islands, Greece", True),
        ("10", "Changi", "Changi, Singapore", True)
    ]

    db_cursor.executemany("INSERT INTO destination VALUES(?, ?, ?, ?)", data_destination)
    db_connection.commit() 


    data_pilot = [
        ("1", "Aaron Smith", "0,3,4", True),
        ("2", "Adam Gilbert", "1.2.5", True),
        ("3", "Jake Choo", "0,3,6", True),
        ("4", "Minato", "2,5,6", True),
        ("5", "Raghu Ram", "1,4,5", True),
        ("6", "Rajneesh Singh", "2,5,6", True),
        ("7", "Sam Fowler", "0,2,3", True),
        ("8", "Jake Dhillon", "1,4,6", True),
        ("9", "Jacob Doblinger", "3,5,6", True), 
        ("10", "Ben Houghton", "0,2,4", True)
    ]

    db_cursor.executemany("INSERT INTO pilot VALUES(?, ?, ?, ?)", data_pilot)
    db_connection.commit() 

    data_pilotonmodel = [
        ("3", "9"),
        ("3", "4"),
        ("3", "3"),
        ("6", "6"),
        ("6", "10"),
        ("6", "9"),
        ("1", "4"),
        ("1", "3"),
        ("5", "10"), 
        ("5", "9"),
        ("4", "6")  
    ]

    db_cursor.executemany("INSERT INTO pilot_trained_on_model VALUES(?, ?)", data_pilotonmodel)
    db_connection.commit() 

    data_model4dest = [
        ("3", "9"),
        ("3", "4"),
        ("3", "3"),
        ("6", "6"),
        ("6", "10"),
        ("6", "9"),
        ("1", "4"),
        ("1", "3"),
        ("5", "10"), 
        ("5", "9"),
        ("4", "6") 
    ]

    db_cursor.executemany("INSERT INTO model_permitted_4_dest VALUES(?, ?)", data_model4dest)
    db_connection.commit() 

    data_flight = [
        ("1", None, "9", None, None, "Planning"),
        ("2", None, "4", None, None, "Planning"),
        ("3", None, "3", None, None, "Planning"),
        ("4", "6", "6", "10", None, "To Schedule"),
        ("5", "5", "10", "9", "7 5 2025", "Scheduled"),
        ("6", None, "9", None, None, "Planning"),
        ("7", None, "4", None, None, "Planning"),
        ("8", None, "3", None, None, "Planning"),
        ("9", None, "10", None, None, "Planning"), 
        ("10", None, "9", None, None, "Planning"),
        ("11", None, "6", None, None, "Planning")
    ]

    db_cursor.executemany("INSERT INTO flight VALUES(?, ?, ?, ?, ?, ?)", data_flight)
    db_connection.commit() 

    db_connection.close()

"""
The below function is to create flight
"""
def create_flight(db_cursor, resDestination, resModel, resStatus, resDepDate, resPilot):
    FlightIdFetcher = db_cursor.execute("Select flight_id from flight ORDER BY flight_id DESC")
    flightIdFetcherRow = FlightIdFetcher.fetchone()
    lastflightId = flightIdFetcherRow["flight_id"]
    flightId = lastflightId+1
    db_cursor.execute("INSERT INTO flight VALUES(?, ?, ?, ?, ?, ?)", (flightId, resModel, resDestination, resPilot, resDepDate, resStatus))

    res = db_cursor.execute("SELECT * FROM flight WHERE flight_id = ?", flightId)
    res.fetchone()
    print(res.fetchone())

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
The below function is to update the departure date and status of a flight selected by the user
"""
def modify_flight_schedule(db_cursor, flightId, depDate, status):
    if depDate is not "" and status is not "":
        db_cursor.execute("UPDATE flight SET flight_schedule=?, flight_status=? WHERE flight_id=? ", (depDate, status, flightId))
    elif depDate is not "" and status is "":
        db_cursor.execute("UPDATE flight SET flight_schedule=? WHERE flight_id=? ", (depDate, flightId))
    elif depDate is "" and status is not "":
        db_cursor.execute("UPDATE flight SET flight_status=? WHERE flight_id=? ", (status, flightId))
    db_connection.commit() 

    res = db_cursor.execute("SELECT * FROM flight where flight_id = ?" , flightId) 
    res.fetchall()
    print(res.fetchall())

    

"""
The below function is to assign pilot to an entry in the flight table based on conditions
"""
def assign_pilot(db_cursor, flightId, pilotId, random):

    if pilotId == "" and random == "Y":
        flight_dets = db_cursor.execute("SELECT * FROM flight where flight_id = ?" , flightId) 
        flight_dets_row = flight_dets.fetchone()
        depDate = flight_dets_row["flight_schedule"]
        model = flight_dets_row["model_id"]

        dep_date = datetime.datetime.strptime(depDate, '%d %m %Y')
        # Use isoweekday() to get the weekday (Monday is 1 and Sunday is 7)
        day_of_week = (dep_date.weekday() + 1) % 7  # Convert Sunday from 6 to 0

        print(day_of_week)

        pilot_rec = db_cursor.execute("SELECT * FROM pilot LEFT JOIN pilot_trained_on_model where pilot.pilot_id = pilot_trained_on_model.pilot_id and pilot_trained_on_model.model_id = ? and pilot.pilot_workday LIKE ?" , (model,day_of_week)) 
        pilot_row = pilot_rec.fetchone()
        
        if pilot_row is None:
            print('There is no trained pilot on the scheduled departure date for the model of the flight. please try again after changing schedule or model of the flight')
        else:
            pilot = flight_dets_row["pilot_id"]
            db_cursor.execute("UPDATE flight SET pilot_id=? WHERE flight_id=? ", (pilot, flightId))
    elif pilotId is not "":
        #find_pilot = select pilot_id from pilot LEFT JOIN flight ON pilot.
        #db_cursor.execute("UPDATE flight SET flight_schedule=? WHERE flight_id=? ", (depDate, flightId))
        db_cursor.execute("UPDATE flight SET pilot_id=? WHERE flight_id=? ", (pilotId, flightId))
    db_connection.commit() 


    res = db_cursor.execute("SELECT * FROM flight where flight_id = ?" , flightId) 
    res.fetchall()
    print(res.fetchall())


"""
The below function is to view pilot schedule
"""
def view_pilot_schedule(db_cursor, resPilot):

    if resPilot != "All":
        pilot_rec = db_cursor.execute("SELECT * FROM pilot WHERE pilot_id = ?" , resPilot) 
    else:
        pilot_rec = db_cursor.execute("SELECT * FROM pilot") 
    pilot_row = pilot_rec.fetchall()

    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for pilotRec in pilot_row:
        pilotName = pilotRec["pilot_name"]
        rawSchedule = pilotRec["pilot_workday"]
        finalSchedule = ""
        for item in rawSchedule.split(','):
            r = item.strip()
            if finalSchedule == "":
                finalSchedule = finalSchedule + days[r]
            else:
                finalSchedule = finalSchedule + ", " + days[r]
        print(pilotName + " " + finalSchedule)
    
def view_destinations(db_curson):
    res = db_cursor.execute("SELECT * FROM destination")
    res.fetchall()
    print(res.fetchall())

"""
The below function is to retrieve ddata from the flight table based on conditions
"""
def manage_destination(db_cursor, destId, destName, destAdd, destStatus):

    if destId is not "":
        updateQuery = "UPDATE destination SET "
        addAnd = False
        if destName is not "":
            if addAnd == True:
                updateQuery = updateQuery + ", dest_name = " + destName
            else:
                updateQuery = updateQuery + " dest_name = " + destName
            addAnd = True
        if destAdd is not "":
            if addAnd == True:
                updateQuery = updateQuery + ", dest_add = " + destAdd
            else:
                updateQuery = updateQuery + " dest_add = " + destAdd
            addAnd = True
        if destStatus is not "":
            destActive = True
            if destStatus != "Y":
                destActive = False
            if addAnd == True:
                updateQuery = updateQuery + ", active = " + destActive
            else:
                updateQuery = updateQuery + " active = " + destActive
            addAnd = True
        updateQuery = updateQuery + " WHERE dest_id = " + destId
        res = db_cursor.execute(updateQuery)
    else:
        DestIdFetcher = db_cursor.execute("Select dest_id from destination ORDER BY dest_id DESC")
        DestIdFetcherRow = DestIdFetcher.fetchone()
        lastdestId = DestIdFetcherRow["dest_id"]
        destId = lastdestId+1
        destActive = True
        if destStatus != "Y":
            destActive = False
        db_cursor.execute("INSERT INTO destination VALUES(?, ?, ?, ?)", (destId, destName, destAdd, destActive))

    res = db_cursor.execute("SELECT * FROM destination WHERE dist_id = ?", destId)
    res.fetchone()
    print(res.fetchone())
    


"""
The below function is to retrieve ddata from the flight table based on conditions
"""
def view_report(db_cursor, reportType):
    """
    1. Destination Based
    2. Pilot Based
    3. OverAll 
    """
    if reportType == 1:
        res = db_cursor.execute("SELECT destination.dest_name, count(*) FROM flight LEFT JOIN destination ON flight.dest_id = destination.dest_id GROUP BY flight.dest_id")
    elif reportType == 2:
        res = db_cursor.execute("SELECT pilot.pilot_name, count(*) FROM flight LEFT JOIN pilot ON flight.pilot_id = pilot.pilot_id GROUP BY flight.pilot_id")
    else:
        res = db_cursor.execute("SELECT pilot.pilot_name, destination.dest_name, count(*) FROM flight LEFT JOIN pilot LEFT JOIN  ON flight.pilot_id = pilot.pilot_id LEFT JOIN destination ON flight.dest_id = destination.dest_id GROUP BY flight.pilot_id, flight.dest_id")

    
    res.fetchall()
    print(res.fetchall())

    
    

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

          1. Add a New Flight
          2. View Flights by Criteria
          3. Update Flight Information
          4. Assign Pilot to Flight
          5. View Pilot Schedule
          6. View/Update Destination Information
          7. Generate Report
          8. Exit

          ''')
    
    response = input("Your selection : ")
    try:
        selected_option = int(response)

        if selected_option == 1:
            print('''
                Please enter the flight details to insert
            ''')
            resDestination = input("Which destination : ")
            resModel = input("Which model : ")
            resStatus = input("What status : ")
            resDepDate = input("Which departure date : ")
            resPilot = input("Which pilot to add to flight ")

            create_flight(db_cursor, resDestination, resModel, resStatus, resDepDate, resPilot)

        elif selected_option == 2:
            print('''
                Please choose your filter condition or enter empty string to not filter based on that column
            ''')
            resDestination = input("Which destination to filter by : ")
            resStatus = input("Which status to filter by : ")
            resDepDate = input("Which departure date to filter by : ")

            retrive_flight(db_cursor, resDestination, resStatus, resDepDate)

        elif selected_option == 3:
            print('''
                Please fill the new schedule and/or status for the flight you want to update
            ''')
            resFlight = input("Which flight do you want to update : ")
            resDepDate = input("Which departure date to filter by : ")
            resStatus = input("Which status to filter by : ")
            
            modify_flight_schedule(db_cursor, resFlight, resStatus, resDepDate)

        elif selected_option == 4:
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

        elif selected_option == 5:
            print('''
                Please fill the pilot id or see all pilot's schedule
            ''')
            resPilot = input("Which pilot to add to flight or type All: ")
     
            view_pilot_schedule(db_cursor, resPilot)

        elif selected_option == 6:

            print('''
                Do you want to view or update destination?
                  
                  1. View
                  2. Update

            ''')

            resAction = input("Which Action would you like to perform?")
            try:
                resAction = int(response)
                if resAction == 1:
                    view_destinations(db_cursor)
                elif resAction == 2:
                    print('''
                        Please fill the destination details to create or update or inactivate
                    ''')
                    resDestId = input("Which destination do you want to update. If left blank it will create a new destination : ")
                    resDestName = input("Destination Name : ")
                    resDestAddress = input("Destination Address : ")
                    resDestStatus = input("Is it an active destination or would you like to activate it(Y/N) : ")
                                
                    manage_destination(db_cursor, resDestId, resDestName, resDestAddress, resDestStatus)

            except:
                print('''Wrong Selection of report type! Exiting!''')
                end_program = True
                break

            
        elif selected_option == 7:
            print('''
                Please choose the type of report to generate!
                  
                1. Destination Based
                2. Pilot Based
                3. OverAll 
               
            ''')
            resReportType = input("Report type : ")
            try:
                report_option = int(response)
                if report_option == 1 or report_option == 2 or report_option ==3:
                    view_report(db_cursor, report_option)
            except:
                print('''Wrong Selection of report type! Exiting!''')
                end_program = True
                break

        elif selected_option == 8:
            end_program = True
            break
    except:
        print('''Wrong Selection! Exiting!''')
        end_program = True
        break

    db_connection.close()
