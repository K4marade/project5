from __future__ import print_function

import requests
import mysql.connector
from mysql.connector import errorcode
from constants import PARAMETERS as par, DB_NAME, TABLES
from model import Model


class Database:

    def __init__(self):
        self.cnx = mysql.connector.connect(user='leo', password=par['password'])
        self.cursor = self.cnx.cursor()
        self.create_database()
        self.create_tables()

    def create_database(self):

        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
            print("Database {} created successfully.".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

        try:
            self.cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                self.cnx.database = DB_NAME
            else:
                print(err)

    def create_tables(self):
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        self.cursor.close()
        self.cnx.close()


if __name__ == '__main__':
    Database()