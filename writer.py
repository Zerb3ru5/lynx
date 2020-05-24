# 
# date: 22.05.2020
# author: Zerb3ru5
# description: writes the data of main.py into an encryptes csv
# top level project: lynx
#

import sqlite3
import cryptography
import os

class DataManager():
    def __init__(self):
        self.path = 'C:\\Users\\Nutzer\\AppData\\Local\\lynx'

        self.conn = sqlite3.connect(self.path + '\\data.db')
        self.c = self.conn.cursor()

        # create the database if it doesn not exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY, path text, shortcut text, password text)''')
        self.conn.commit()

    def readData(self ):
        self.c.execute('''SELECT * FROM data''')
        data = self.c.fetchall()

        return data

    def writeData(self, data):
        for row in data:
            self.c.execute('''INSERT INTO data (path, shortcut, password) VALUES (?, ?, ?)''', (row[0], row[1], row[2]))

        self.conn.commit()