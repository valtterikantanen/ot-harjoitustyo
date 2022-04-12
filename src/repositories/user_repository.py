from database_connection import get_database
from entities.user import User


class UserRepository:
    def __init__(self, database):
        self.database = database

    def create(self, user):
        username = user.username
        password = user.password

        try:
            self.database.execute("INSERT INTO Users (username, password) VALUES (?, ?)", [
                                  username, password])
            print(f"Käyttäjä {username} lisätty!")
        except:
            print("Käyttäjän lisäämisessä tapahtui virhe, yritä uudelleen.")

    def search_by_username(self, username):
        result = self.database.execute(
            "SELECT username, password FROM Users WHERE username=?", [username]).fetchone()
        if result:
            return User(result[0], result[1])
        return False

    def find_all_users(self):
        result = self.database.execute(
            "SELECT username, password FROM Users").fetchall()
        all_users = []
        for user in result:
            all_users.append(User(user[0], user[1]))
        return all_users


user_repository = UserRepository(get_database())
