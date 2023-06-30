import pyodbc


class Base_db:
    server = '127.0.0.1'
    database = 'SUEP'
    username = 'sa'
    password = 'password'
    conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};TrustServerCertificate=yes;SERVER={server};DATABASE={database};UID={username};PWD={password}'

    def connect(self, autocommit=True):
        conn = pyodbc.connect(self.conn_str, autocommit=autocommit)
        return conn

    def select(self, sql, *params):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()
        conn.close()
        return result

    def insert(self, sql, *params):
        self.exec(sql, *params)

    def update(self, sql, *params):
        self.exec(sql, *params)

    def delete(self, sql, *params):
        self.exec(sql, *params)

    def call(self, procudure, *params):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('{' + "CALL {} ({})".format(procudure, ('?, ' * len(params))[:-2]) + '}', params)
        result = cursor.fetchall()
        conn.close()
        return result

    def exec(self, sql, *params):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.close()

