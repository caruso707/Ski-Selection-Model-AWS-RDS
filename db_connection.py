import pymysql


class Database:
    def __init__(self, hostname, username, password):
        self.db = pymysql.connect(host=hostname, user=username, password=password)
        self.cursor = self.db.cursor()

    def get_sql_version(self):
        self.cursor.execute("Select version()")
        return self.cursor.fetchone()

    def create_database(self, db_name):
        sql = "CREATE DATABASE " + db_name
        self.cursor.execute(sql)
        self.commit_to_db()

    def drop_database(self, db_name):
        sql = "DROP DATABASE " + db_name
        self.cursor.execute(sql)
        self.commit_to_db()

    def commit_to_db(self):
        self.cursor.connection.commit()

    def select_database(self, database):
        sql = "USE " + database
        self.cursor.execute(sql)

    def show_databases(self):
        sql = '''SHOW DATABASES'''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def show_tables(self):
        sql = '''SHOW TABLES'''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_columns(self, table_name):
        sql = '''DESCRIBE ''' + table_name
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_row(self, table, columns, values):
        sql = "INSERT INTO " + table + " " + columns + " VALUES " + values
        print(sql)
        self.cursor.execute(sql)
        self.commit_to_db()

    def delete_all_rows(self, table):
        sql = "DELETE FROM " + table
        self.cursor.execute(sql)
        self.commit_to_db()

    def delete_row(self, table, condition):
        sql = "DELETE FROM " + table + " WHERE " + condition
        self.cursor.execute(sql)
        self.commit_to_db()

    def get_table_length(self, table):
        sql = "SELECT COUNT(*) FROM " + table
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_value_from_table(self, table):
        pass

    def get_table(self, table):
        sql = "SELECT * FROM " + table
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def query(self, table, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()