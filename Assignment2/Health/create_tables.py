import sqlite3

conn = sqlite3.connect('health.sqlite')

c = conn.cursor()

c.execute('''
        CREATE TABLE stats
        (id INTEGER PRIMARY KEY ASC,
        storage VARCHAR(200) NOT NULL,
        receiver VARCHAR(200) NOT NULL,
        processor VARCHAR(200) NOT NULL,
        audit VARCHAR(200) NOT NULL,
        last_updated VARCHAR(100) NOT NULL)
        ''')
        
conn.commit()
conn.close()