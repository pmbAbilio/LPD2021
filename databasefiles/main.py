import sqlite3
from sqlite3 import Error

class DataBaseFiles():
    file = 'data.db'


    @staticmethod
    def createdatabase():
        conn = DataBaseFiles.create_connection('data.db')

        sql_create_log_data_table = """ CREATE TABLE IF NOT EXISTS logdata (
                                        id integer PRIMARY KEY,
                                        logname text,
                                        ip text NOT NULL,
                                        timestamp text,
                                        message text
                                    ); """

        sql_create_ip_data_table = """ CREATE TABLE IF NOT EXISTS ipdata (
                                        id integer PRIMARY KEY,
                                        ip text NOT NULL,
                                        starttimestamp text,
                                        finishtimestamp text,
                                        location text,
                                        attemps integer
                                    ); """

        # create tables
        if conn is not None:
            # create projects table
            DataBaseFiles.create_table(conn, sql_create_log_data_table)
            DataBaseFiles.create_table(conn, sql_create_ip_data_table)
            return conn
        else:
            print("Error! cannot create the database connection.")

    @staticmethod
    def create_connection(db_file):
        conn = None
        """ create a database connection to a SQLite database """
        try:
            return sqlite3.connect(db_file)   
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def create_table(conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    @staticmethod
    def insertdata(conn, data):
        #data = ('ip','timestamp', 'message')
        sql = ''' INSERT INTO logdata (logname,ip,timestamp,message) VALUES (?,?,?,?);'''
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()

        return cur.lastrowid
    @staticmethod
    def insertipdata(conn, data):
        sql = ''' INSERT INTO ipdata (ip,starttimestamp, finishtimestamp,location, attempts) VALUES (?,?,?,?,?);'''
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()

        return cur.lastrowid

    @staticmethod
    def selectdata(self, conn, filter):
        if filter['atribute'] == 1:
            sql = "SELECT * FROM "+ filter['table']
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
        else:
            sql = "SELECT * FROM "+ filter['table'] +" WHERE "+ filter['atribute'] +"=?"
            cur = conn.cursor()
            cur.execute(sql, (filter['value'],))
            return cur.fetchall()
    


