# This file contains the class database that handles the transactions with the mysql database

import mysql.connector


class Database:
    """This class handles the transactions with the mysql database"""
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.mycursor = self.mydb.cursor()
