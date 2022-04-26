from entities.user import User
from entities.transaction import Transaction
from repositories.user_repository import user_repository
from repositories.transaction_repository import transaction_repository
from repositories.category_repository import category_repository


class BudgetService:
    def __init__(self):
        self.user = None
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def create_user(self, username, password1, password2):
        if self.user_repository.search_by_username(username):
            print(f"Käyttäjätunnus {username} on jo käytössä!")
            return False
        if password1 != password2:
            print("Salasanat eivät täsmää!")
            return False

        self.user_repository.create(User(username, password1))
        return True

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

    def add_transaction(self, date, income_or_expense, amount, category, description):
        if not self.user:
            print("Et ole kirjautunut sisään!")
            return False

        amount = amount.replace(",", ".")
        if income_or_expense == "meno":
            amount = "-" + amount

        try:
            amount = int(100 * float(amount))
        except ValueError:
            print("Syöttämäsi määrä oli väärässä muodossa.")
            return False

        category_id = self.get_category_id(category)

        self.transaction_repository.add(Transaction(
            date, amount, category_id, description, self.user))
        return True

    def find_transactions(self):
        if not self.user:
            print("Et ole kirjautunut sisään!")
            return False

        return self.transaction_repository.find_all(self.user)

    def get_category_id(self, name):
        return self.category_repository.find_one(name)

    def get_categories(self, income_or_expense):
        if not self.user:
            print("Et ole kirjautunut sisään!")
            return False

        if income_or_expense.lower() == "meno":
            return self.category_repository.find_all_expense_categories()

        if income_or_expense.lower() == "tulo":
            return self.category_repository.find_all_income_categories()

        return False

    def delete_category(self, name):
        if not self.user:
            print("Et ole kirjautunut sisään!")
            return False

        if not self.category_repository.find_one(name):
            print("Kategoriaa ei löytynyt.")
            return False
        self.category_repository.delete(name)
        return True

    def add_category(self, name):
        if not self.user:
            print("Et ole kirjautunut sisään!")
            return False

        self.category_repository.add(name)
        return True


budget_service = BudgetService()
