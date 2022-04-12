from database_connection import get_database


def drop_tables(database):
    database.execute("DROP TABLE IF EXISTS Users")
    database.execute("DROP TABLE IF EXISTS Categories")
    database.execute("DROP TABLE IF EXISTS Transactions")


def create_tables(database):
    database.execute(
        "CREATE TABLE Users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    database.execute(
        "CREATE TABLE Categories (id INTEGER PRIMARY KEY, name TEXT, visible INTEGER DEFAULT 1)")
    database.execute(
        "CREATE TABLE Transactions (id INTEGER PRIMARY KEY, date TEXT, amount INTEGER, "
        "category_id INTEGER, description TEXT, user_id INTEGER)")


def insert_categories(database):
    categories = ["Ajoneuvot ja liikenne", "Asuminen", "Harrastukset", "Kauneus ja hyvinvointi",
                  "Kulttuuri ja viihde", "Lapset", "Lemmikit", "Luoton maksut", "Matkailu",
                  "Ostokset", "Palvelut", "Ravintolat ja kahvilat", "Ruoka ja päivittäistavarat",
                  "Säästöt ja sijoitukset", "Terveys", "Vaatteet", "Vakuutukset", "Muut menot",
                  "Palkka", "Tulonsiirrot", "Muut tulot"]
    for category in categories:
        database.execute(
            "INSERT INTO Categories (name) VALUES (?)", [category])


def initialize_database():
    database = get_database()

    drop_tables(database)
    create_tables(database)
    insert_categories(database)


if __name__ == "__main__":
    initialize_database()
