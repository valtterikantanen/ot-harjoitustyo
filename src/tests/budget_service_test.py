import unittest

from services.budget_service import BudgetService, PasswordsDontMatchError, UsernameAlreadyExistsError, UserNotFoundError, WrongPasswordError, InvalidUsernameOrPasswordError, AmountInWrongFormatError, TooBigNumberError
from build import build


class TestBudgetService(unittest.TestCase):
    def setUp(self):
        build()
        self.budget_service = BudgetService()
        self.budget_service.create_user("antero", "password123", "password123")

    def test_sign_up_with_used_username(self):
        self.assertRaises(UsernameAlreadyExistsError, self.budget_service.create_user, "antero", "password456", "password456")

    def test_sign_up_with_empty_username(self):
        self.assertRaises(InvalidUsernameOrPasswordError, self.budget_service.create_user, "", "password456", "password456")

    def test_sign_up_with_empty_password(self):
        self.assertRaises(InvalidUsernameOrPasswordError, self.budget_service.create_user, "ilmari", " ", " ")

    def test_sign_up_with_wrong_password_confirmation(self):
        self.assertRaises(PasswordsDontMatchError, self.budget_service.create_user, "ilmari", "password123", "password132")

    def test_log_in_if_user_does_not_exist(self):
        self.assertRaises(UserNotFoundError, self.budget_service.login_user, "atnero", "password123")

    def test_log_in_if_password_is_wrong(self):
        self.assertRaises(WrongPasswordError, self.budget_service.login_user, "antero", "pasword123")

    def test_log_out_when_logged_in(self):
        self.budget_service.login_user("antero", "password123")
        self.budget_service.logout_user()
        self.assertEqual(self.budget_service.user, None)

    def test_add_income_saves_the_amount_in_right_format(self):
        self.budget_service.login_user("antero", "password123")
        self.budget_service.add_transaction("12.4.2022", "income", "253.69", "Tulonsiirrot", "Opintotuki")
        transaction = self.budget_service.find_transactions()[0]
        self.assertEqual(transaction[2], 25369)

    def test_add_expense_saves_the_amount_in_right_format(self):
        self.budget_service.login_user("antero", "password123")
        self.budget_service.add_transaction("12.4.2022", "expense", "648.23", "Asuminen", "Vuokra")
        transaction = self.budget_service.find_transactions()[0]
        self.assertEqual(transaction[2], -64823)

    def test_add_transaction_with_too_big_amount(self):
        self.budget_service.login_user("antero", "password123")
        self.assertRaises(TooBigNumberError, self.budget_service.add_transaction, "12.4.2022", "meno", "9223372036854775808", "Asuminen", "Vuokra")
        
    def test_add_transaction_with_wrong_type_of_amount(self):
        self.budget_service.login_user("antero", "password123")
        self.assertRaises(AmountInWrongFormatError, self.budget_service.add_transaction, "12.4.2022", "meno", "5,12 €", "Asuminen", "Vuokra")

    def test_add_category(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(len(self.budget_service.get_categories()), 21)
        self.budget_service.add_category("Testi", "Meno")
        self.assertEqual(len(self.budget_service.get_categories()), 22)

    def test_delete_category(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(len(self.budget_service.get_categories()), 21)
        self.budget_service.delete_category(1)
        self.assertEqual(len(self.budget_service.get_categories()), 20)

    def test_show_all_categories(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(len(self.budget_service.get_categories()), 21)

    def test_show_expense_categories(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(len(self.budget_service.get_categories("expense")), 18)

    def test_show_income_categories(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(len(self.budget_service.get_categories("income")), 3)