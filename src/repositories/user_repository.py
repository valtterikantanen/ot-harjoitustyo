from database_connection import get_database
from entities.user import User


class UserRepository:
    def __init__(self, database):
        self.database = database

    def create(self, user):
        username = user.username
        password = user.password

        self.database.execute(
            "INSERT INTO Users (username, password) VALUES (?, ?)", [username, password])
        return self.get_user_id(username)

    def search_by_username(self, username):
        result = self.database.execute(
            "SELECT username, password FROM Users WHERE username=?", [username]).fetchone()
        return User(result[0], result[1]) if result else False

    def get_user_id(self, username):
        user_id = self.database.execute(
            "SELECT id FROM Users WHERE username=?", [username]).fetchone()
        return user_id[0] if user_id else None

    #def find_all_users(self):
        #result = self.database.execute("SELECT username, password FROM Users").fetchall()
        #all_users = []
        #for user in result:
            #all_users.append(User(user[0], user[1]))
        #return all_users

user_repository = UserRepository(get_database())
