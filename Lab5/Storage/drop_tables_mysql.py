import mysql.connector
db_conn = mysql.connector.connect(host="localhost", user="root",
password="TTA271137", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
DROP TABLE rented_car, returned_car
''')

db_conn.commit()
db_conn.close()