import sqlite3

db = sqlite3.connect("expensetracker.db")
db.isolation_level = None

def get_database():
    return db