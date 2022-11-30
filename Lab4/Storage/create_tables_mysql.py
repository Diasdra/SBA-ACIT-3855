import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="root",
password="TTA271137", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE rented_car
          (id INT NOT NULL AUTO_INCREMENT, 
           traceId VARCHAR(200) NOT NULL,
           carId VARCHAR(250) NOT NULL, 
           location VARCHAR(250) NOT NULL,
           mileage Integer(200) NOT NULL,
           passengerLimit Integer(200) NOT NULL,
           returnDate VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT rented_car_pk PRIMARY KEY(id))
          ''')


db_cursor.execute('''
          CREATE TABLE return_car
          (id INT NOT NULL AUTO_INCREMENT,
           traceId VARCHAR(200) NOT NULL, 
           carId VARCHAR(250) NOT NULL, 
           kilometers Integer(200) NOT NULL,
           gasUsed Integer(200) NOT NULL,
           cost Integer(200) NOT NULL,
           rentDuration Integer(200) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT return_car_pk PRIMARY KEY(id))
          ''')

db_conn.commit()
db_conn.close()
