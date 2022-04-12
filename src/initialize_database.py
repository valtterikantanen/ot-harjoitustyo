from database_connection import get_database


def drop_tables(db):
    db.execute("DROP TABLE IF EXISTS Users")
    db.execute("DROP TABLE IF EXISTS Categories")
    db.execute("DROP TABLE IF EXISTS Transactions")


def create_tables(db):
    db.execute("CREATE TABLE Users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    db.execute("CREATE TABLE Categories (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("CREATE TABLE Transactions (id INTEGER PRIMARY KEY, date TEXT, amount INTEGER, category_id INTEGER, description TEXT, user_id INTEGER)")

def insert_categories(db):
    db.execute("INSERT INTO Categories (name) VALUES ('Ajoneuvot ja liikenne'), ('Asuminen'), ('Harrastukset'), ('Kauneus ja hyvinvointi'), ('Kulttuuri ja viihde'), ('Lapset'), ('Lemmikit'), ('Luoton maksut'), ('Matkailu'), ('Ostokset'), ('Palvelut'), ('Ravintolat ja kahvilat'), ('Ruoka ja päivittäistavarat'), ('Säästöt ja sijoitukset'), ('Terveys'), ('Vaatteet'), ('Vakuutukset'), ('Muut menot'), ('Palkka'), ('Tulonsiirrot'), ('Muut tulot')")


def initialize_database():
    db = get_database()

    drop_tables(db)
    create_tables(db)
    insert_categories(db)


if __name__ == "__main__":
    initialize_database()
