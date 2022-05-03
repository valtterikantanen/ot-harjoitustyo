from database_connection import get_database


def drop_tables(database):
    """Poistaa tietokantataulut.

    Args:
        database: Tietokantayhteyden Connection-olio.
    """

    database.execute("DROP TABLE IF EXISTS Users")
    database.execute("DROP TABLE IF EXISTS Transactions")
    database.execute("DROP TABLE IF EXISTS Categories")
    database.execute("DROP TABLE IF EXISTS CategoryVisibilities")


def create_tables(database):
    """Luo tietokantataulut.

    Args:
        database: Tietokantayhteyden Connection-olio.
    """

    database.execute(
        "CREATE TABLE Users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    database.execute(
        "CREATE TABLE Transactions (id INTEGER PRIMARY KEY, date TEXT, amount INTEGER, "
        "category_id INTEGER, description TEXT, user_id INTEGER)")
    database.execute("CREATE TABLE Categories (id INTEGER PRIMARY KEY, name TEXT, type TEXT)")
    database.execute("CREATE TABLE CategoryVisibilities (category_id INTEGER, user_id INTEGER)")


def insert_categories(database):
    """Syöttää oletuskategoriat tietokannan Categories-tauluun.

    Args:
        database: Tietokantayhteyden Connection-olio.
    """

    categories = [
        ("Ajoneuvot ja liikenne", "expense"), ("Asuminen", "expense"), ("Harrastukset", "expense"),
        ("Kauneus ja hyvinvointi", "expense"), ("Kulttuuri ja viihde", "expense"), ("Lapset",
        "expense"), ("Lemmikit", "expense"), ("Luoton maksut", "expense"), ("Matkailu", "expense"),
        ("Ostokset", "expense"), ("Palvelut", "expense"), ("Ravintolat ja kahvilat", "expense"),
        ("Ruoka ja päivittäistavarat", "expense"), ("Säästöt ja sijoitukset", "expense"),
        ("Terveys", "expense"), ("Vaatteet", "expense"), ("Vakuutukset", "expense"), ("Muut menot",
        "expense"), ("Palkka", "income"), ("Tulonsiirrot", "income"), ("Muut tulot", "income")
        ]
    database.executemany("INSERT INTO Categories (name, type) VALUES (?, ?)", categories)


def initialize_database():
    """Alustaa tietokantataulut.
    """

    database = get_database()

    drop_tables(database)
    create_tables(database)
    insert_categories(database)


if __name__ == "__main__":
    initialize_database()
