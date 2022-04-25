from config import DB_NAME
import sqlite3

db = sqlite3.connect(DB_NAME)
db.isolation_level = None

def get_database():
    return db
