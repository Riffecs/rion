"""
Database Class
"""
import sqlite3


class Database:
    """
    Database Class
    """

    def __init__(self, db_name: str = "None"):
        """
        Konstruktor
        @param db_name:
        """
        self.db_name = db_name

    def create_database(self) -> None:
        """
        Creates a database with sqlite3
        @return:
        """
        # Creates the database via a Python Courser
        sqlite3.connect(f"{self.db_name}.db")

    def courser(self) -> sqlite3.Connection:
        """
        Creates a courser
        @return:
        """
        # Creates the database via a Python Courser
        return sqlite3.connect(f"{self.db_name}.db")

    def create_table(self, db_table: str, db_header: str) -> None:
        """
        Creates the corresponding tables via an SQL block.
        @param db_table:
        @param db_header:
        @return:
        """
        # Creates a connection to the database
        con = sqlite3.connect(f"{self.db_name}.db")
        # Creates a courser that points to the database
        cur = con.cursor()
        # Creates the SQL Command
        table = f"CREATE TABLE IF NOT EXISTS {db_table} ({db_header})"
        # Executes the SQL
        cur.execute(table)
        # "Save" the changes
        con.commit()
        # close
        con.close()
        # Destroys the Courser
        cur = None

    def input_value(self, db_table: str, db_content: str) -> None:
        """
        Creates the corresponding tables via an SQL block.
        @param self:
        @param db_table:
        @param db_content:
        @return:
        """
        # Creates a connection to the database
        con = sqlite3.connect(f"{self.db_name}.db")
        # Creates a courser that points to the database
        cur = con.cursor()
        # Creates the SQL Command
        table = f"INSERT INTO {db_table} VALUES {db_content}"
        print(f"\n\n{table}\n\n")
        # Executes the SQL
        cur.execute(table)
        # "Save" the changes
        con.commit()
        table = f"SELECT * FROM {db_table}"
        cur.execute(table)
        print(cur.execute(table))
        # close
        con.close()
        # Destroys the Courser
        cur = None
        con = None

    def list_table(self, db_table: str, db_header: str) -> list:
        """
        Return List of Table
        @param self:
        @param db_table:
        @param db_header:
        @return:
        """
        # Creates a connection to the database
        con = sqlite3.connect(f"{self.db_name}.db")
        # Creates a courser that points to the database
        cur = con.cursor()
        # Creates an empty list
        container = []
        for row in cur.execute(f"SELECT * FROM {db_table} ORDER BY {db_header}"):
            container.append(row)
        return container

    def print_table(self, db_table: str) -> None:
        """
        print List of Table
        @param self:
        @param db_table:
        @return:
        """
        for i in self.list_table(self.db_name, db_table):
            print(i)

    def db_handler(self, sql_expression: str) -> None:
        """
        A Simple SQL Handler for Primitive Queries
        @param self:
        @param sql_expression:
        @return:
        """
        # Creates a connection to the database
        con = sqlite3.connect(f"{self.db_name}.db")
        # Creates a courser that points to the database
        cur = con.cursor()
        # Executes the SQL
        cur.execute(sql_expression)
        # "Save" the changes
        con.commit()
        # close
        con.close()
        # Destroys the Courser
        cur = None

    def delete_package(self, db_table: str, db_content: str, db_ident: str) -> None:
        """
        Delete Packages from a SQL table
        @param self:
        @param db_table:
        @param db_content:
        @param content:
        @return:
        """
        # self, db_table: str, db_header: str
        # self.input_value(db_table, "('buddy-v100_0_3', 'buddy', '100_0_3', 'venv')")
        con = None
        cur = None
        # Creates a connection to the database
        con = sqlite3.connect(f"{self.db_name}.db")
        # Creates a courser that points to the database
        cur = con.cursor()
        # Creates the SQL DELETE Command
        # table = f"SELECT * FROM {db_table}"
        table = f"DELETE FROM {db_table} WHERE {db_ident}='{db_content}'"
        # table = "DELETE FROM xyz WHERE id='buddy-v100_0_4'"
        print(f"\n\n{table}\n\n")
        # Executes the SQL
        cur.execute(table)
        # "Save" the changes
        con.commit()
        # close
        con.close()
        # Destroys the Courser
        cur = None
        con = None
