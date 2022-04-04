from database_connection import get_database

def drop_tables(db):
    db.execute("DROP TABLE IF EXISTS Users")
    db.execute("DROP TABLE IF EXISTS Categories")
    db.execute("DROP TABLE IF EXISTS Expenses")

def create_tables(db):
    db.execute("CREATE TABLE Users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    db.execute("CREATE TABLE Categories (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("CREATE TABLE Expenses (id INTEGER PRIMARY KEY, date TEXT, amount INTEGER, category_id INTEGER, description TEXT)")

def initialize_database():
    db = get_database()

    drop_tables(db)
    create_tables(db)

if __name__ == "__main__":
    initialize_database()