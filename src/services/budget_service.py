from entities.user import User
from repositories.user_repository import user_repository

class BudgetService:
    def __init__(self):
        self.user = None
        self.user_repository = user_repository

    def create_user(self, username, password):
        if self.user_repository.search_by_username(username):
            print(f"Käyttäjätunnus {username} on jo käytössä!")
        else:
            self.user_repository.create(User(username, password))

    def login_user(self, username, password):
        if self.user:
            print("Olet jo kirjautunut sisään!")
            return False

        result = self.user_repository.search_by_username(username)
        if not result:
            print(f"Käyttäjää {username} ei löytynyt.")
            return False

        if password != result.password:
            print("Väärä salasana.")
            return False

        self.user = result
        print("Olet kirjautunut sisään!")
        return True

    def logout_user(self):
        if not self.user:
            print("Et ole kirjautunut sisään.")
            return False
            
        self.user = None
        print("Olet kirjautunut ulos.")
        return True

budget_service = BudgetService()