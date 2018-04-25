# Óðinn Ben og Matthías Ólafur
# 25.04.2018
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
from iceconnect import DbConnector

class notendur(DbConnector):
    def __init__(self):
        DbConnector.__init__(self)

    def addUser(self, notendanafn, lykilord, admin = False):
        rows_affected = 0
        result = self.execute_procedure('addUser', [notendanafn,lykilord,admin])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def delUser(self, notendanafn):
        rows_affected = 0
        result = self.execute_procedure('delUser', [notendanafn])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def updateUserPass(self, notendanafn, lykilord):
        rows_affected = 0
        result = self.execute_procedure('updateUserPass', [notendanafn,lykilord])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def updateUserAdmin(self, notendanafn, admin):
        rows_affected = 0
        result = self.execute_procedure('updateUserAdmin', [notendanafn,admin])
        if result:
            rows_affected = int(result[0][0])
        return rows_affected

    def listUsers(self):
        result = self.execute_procedure('listUsers', [])
        if result:
            return result
        else:
            return list()

    def getUser(self, notendanafn):
        result = self.execute_procedure('getUser', [notendanafn])
        if result:
            return result[0]
        else:
            return list()

