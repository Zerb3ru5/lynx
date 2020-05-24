#
# date: 23.05.2020
# author: Zerb3ru5
# description: The control class for the lynx programme
#

import os
import sqlite3
import cryptography


class Locker():
    def __init__(self):
        self.path = 'C:\\Users\\Nutzer\\AppData\\Local\\lynx'

        self.conn = sqlite3.connect(self.path + '\\data.db')
        self.c = self.conn.cursor()

        # create the database if it doesn not exist
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY, path text, shortcut text, password text, locked INTEGER)''')
        self.conn.commit()

    # hide a directory by adding the HIDDEN attribute and mark it in the database
    def hide(self, path, password, shortcut=''):
        if os.path.exists(path):

            # hide the path
            os.system('attrib +h %s' % path)

            # mark it as hidden in the database and create a new entry if it is the first one with that path
            self.c.execute('''SELECT id FROM data WHERE path = ?''', (path,))
            similar_entries = self.c.fetchall()
            if len(similar_entries) != 0:
                self.c.execute(
                    '''UPDATE data SET locked = 1 WHERE path = ?''', (path,))
                self.conn.commit()
                print('update old entry')
            elif len(similar_entries) == 0:
                self.writeRow(path, shortcut, password, 1)
                print('create new entry')

    # reveal a directory by removing the HIDDEN attribute and mark that in the database by checking the password
    def reveal(self, path, password):

        # check if the given path even exists and if it does get the corresponding password
        if path in self.unravelList(self.readColumn('path'), 2):

            # the password we get is nested, so we need to unravel it
            cpw = self.unravelList(self.getItem(
                'password', 'path', path), 2)[0]

            # compare the password
            right_password = password == cpw

            # reveal the folder
            if right_password:
                os.system('attrib -h %s' % path)

                # mark it as revealed in database
                self.c.execute('''UPDATE data SET locked = 0 WHERE path = ?''', (path,))
                self.conn.commit()

    def readData(self):
        self.c.execute('''SELECT * FROM data''')
        data = self.c.fetchall()

        return data

    def readColumn(self, column):

        # check if this column exists
        exists = True
        try:
            self.c.execute('''SELECT %s from data''' % column)
        except (Exception):
            exists = False

        # read in the column
        if exists:
            column = self.c.fetchall()
            return column

    def getItem(self, column, column_row_identifier, value):

        # check if this column exists
        exists = True
        try:
            self.c.execute('''SELECT %s from data''' % column)
        except (Exception):
            exists = False

        # read in the row
        if exists:
            self.c.execute(
                f'''SELECT {column} FROM data WHERE {column_row_identifier} = "{value}"''')
            item = self.c.fetchall()    

            return item

    def writeRow(self, path, shortcut, password, locked):
        self.c.execute(
            '''INSERT INTO data (path, shortcut, password, locked) VALUES (?, ?, ?, ?)''', (path, shortcut, password, locked))
        self.conn.commit()

    # unravel a nested list
    def unravelList(self, work_list, depth):

        unravelled = list()

        for sublist in work_list:
            for item in sublist:
                unravelled.append(item)

        depth -= 2

        if not depth <= 0:
            self.unravelList(unravelled, depth)

        return unravelled
