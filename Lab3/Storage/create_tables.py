import sqlite3

conn = sqlite3.connect('CarRenting.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE rented_car
          (id INTEGER PRIMARY KEY ASC, 
           carId VARCHAR(250) NOT NULL, 
           location VARCHAR(250) NOT NULL,
           mileage Integer(200) NOT NULL,
           passengerLimit Integer(200) NOT NULL,
           returnDate VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE return_car
          (id INTEGER PRIMARY KEY ASC, 
           carId VARCHAR(250) NOT NULL, 
           kilometers Integer(200) NOT NULL,
           gasUsed Integer(200) NOT NULL,
           cost Integer(200) NOT NULL,
           rentDuration Integer(200) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
