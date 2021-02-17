import sqlite3
from sqlite3 import Error

class DataBaseFiles():
    file = 'data.db'


    @staticmethod
    def createdatabase():
        conn = DataBaseFiles.create_connection('data.db')

        sql_create_ufw_data_table = """ CREATE TABLE IF NOT EXISTS ufwdata (
                                        id integer PRIMARY KEY,
                                        ip text NOT NULL,
                                        date DATE NOT NULL,
                                        message text
                                    ); """

        sql_create_ssh_data_table = """ CREATE TABLE IF NOT EXISTS sshdata (
                                        id integer PRIMARY KEY,
                                        ip text NOT NULL,
                                        date DATE NOT NULL,
                                        user text,
                                        message text
                                    ); """

        sql_create_apache_data_table = """ CREATE TABLE IF NOT EXISTS apachedata (
                                        id integer PRIMARY KEY,
                                        ip text NOT NULL,
                                        date DATE NOT NULL,
                                        url text,
                                        resultcode text
                                    ); """

        sql_create_analisys_data_table = """ CREATE TABLE IF NOT EXISTS analisysdata (
                                        id integer PRIMARY KEY,
                                        date DATE NOT NULL
                                    ); """
        
        # create tables
        if conn is not None:
            # create projects table
            DataBaseFiles.create_table(conn, sql_create_ufw_data_table)
            DataBaseFiles.create_table(conn, sql_create_ssh_data_table)
            DataBaseFiles.create_table(conn, sql_create_apache_data_table)
            DataBaseFiles.create_table(conn, sql_create_analisys_data_table)
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
    def insertufwdata(conn, data):
        sql = '''INSERT INTO ufwdata (ip, date, message ) VALUES (?,?,?);'''
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()

        return cur.lastrowid
    @staticmethod
    def insertsshdata(conn, data):
        sql = ''' INSERT INTO sshdata (ip,date, user, message) VALUES (?,?,?,?);'''
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()

        return cur.lastrowid

    @staticmethod
    def insertapachedata(conn, data):
        sql = ''' INSERT INTO apachedata (ip,date, url, resultcode) VALUES (?,?,?,?);'''
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()

        return cur.lastrowid
    
    @staticmethod
    def insertanalisysdata(conn, data):
        sql = ''' INSERT INTO analisysdata (date) VALUES (?,?,?,?);'''
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()

        return cur.lastrowid

    @staticmethod
    def selectdata( conn, filter):
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
    


