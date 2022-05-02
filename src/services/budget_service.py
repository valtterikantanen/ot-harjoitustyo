from entities.user import User
from entities.transaction import Transaction
from repositories.user_repository import user_repository
from repositories.transaction_repository import transaction_repository
from repositories.category_repository import category_repository

class PasswordsDontMatchError(Exception):
    pass

class UsernameAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

class InvalidUsernameOrPasswordError(Exception):
    pass

class AmountInWrongFormatError(Exception):
    pass

class TooBigNumberError(Exception):
    pass


class BudgetService:
    def __init__(self):
        self.user = None
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def create_user(self, username, password1, password2):
        if self.user_repository.search_by_username(username):
            raise UsernameAlreadyExistsError()
        if password1 != password2:
            raise PasswordsDontMatchError()
        if len(username.strip()) == 0 or len(password1.strip()) == 0:
            raise InvalidUsernameOrPasswordError()

        user_id = self.user_repository.create(User(username, password1))
        self.category_repository.add_default_categories(user_id)

    def login_user(self, username, password):
        result = self.user_repository.search_by_username(username)
        if not result:
            raise UserNotFoundError()
        if password != result.password:
            raise WrongPasswordError()

        self.user = result

    def logout_user(self):
        self.user = None

    def add_transaction(self, date, income_or_expense, amount, category, description=None):
        amount = amount.replace(",", ".")
        if income_or_expense == "meno":
            amount = f"-{amount}"

        try:
            amount = int(100 * float(amount))
        except ValueError as exc:
            raise AmountInWrongFormatError() from exc

        if amount < -9223372036854775808 or amount > 9223372036854775807:
            raise TooBigNumberError()

        category_id = self.get_category_id(category)

        self.transaction_repository.add(Transaction(
            date, amount, category_id, description, self.user))

    def find_transactions(self):
        return self.transaction_repository.find_all(self.user)

    def get_category_id(self, name):
        return self.category_repository.get_category_id(name)

    def get_categories(self, income_or_expense):
        user_id = self.user_repository.get_user_id(self.user.username)

        if income_or_expense.lower() == "meno":
            return self.category_repository.find_all_expense_categories(user_id)

        if income_or_expense.lower() == "tulo":
            return self.category_repository.find_all_income_categories(user_id)

        return False

    def get_all_categories(self):
        user_id = self.user_repository.get_user_id(self.user.username)
        return self.category_repository.find_all_categories(user_id)

    def delete_category(self, category_id):
        user_id = self.user_repository.get_user_id(self.user.username)
        self.category_repository.delete(category_id, user_id)

    def add_category(self, name, category_type):
        user_id = self.user_repository.get_user_id(self.user.username)
        self.category_repository.add(name, category_type, user_id)


budget_service = BudgetService()
