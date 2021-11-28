import sqlite3
import os

os.chdir('./database')
connection = sqlite3.connect('voting_system.db')

with open('db_config.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()

