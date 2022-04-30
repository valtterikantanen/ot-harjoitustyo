import unittest
from services.budget_service import BudgetService
from build import build


class TestBudgetService(unittest.TestCase):
    def setUp(self):
        build()
        self.budget_service = BudgetService()
        self.budget_service.create_user("antero", "password123", "password123")

    def test_sign_up_with_used_username(self):
        self.assertEqual(self.budget_service.create_user("antero", "password456", "password456"), False)

    def test_sign_up_with_wrong_password_confirmation(self):
        self.assertEqual(self.budget_service.create_user("ilmari", "password123", "password456"), False)

    def test_log_in_if_user_is_already_logged_in(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.login_user("antero", "password123"), False)

    def test_log_in_if_another_user_is_already_logged_in(self):
        self.budget_service.create_user("ilmari", "password123", "password123")
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.login_user("ilmari", "password123"), False)

    def test_log_in_if_user_does_not_exist(self):
        self.assertEqual(self.budget_service.login_user("atnero", "password123"), False)

    def test_log_in_if_password_is_wrong(self):
        self.assertEqual(self.budget_service.login_user("antero", "pasword123"), False)

    def test_log_out_without_being_logged_in(self):
        self.assertEqual(self.budget_service.logout_user(), False)

    def test_log_out_when_logged_in(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.logout_user(), True)

    def test_add_transaction_when_not_logged_in(self):
        self.assertEqual(self.budget_service.add_transaction("12.4.2022", "meno", "5.12", "Asuminen"), False)

    def test_add_income_saves_the_amount_in_right_format(self):
        self.budget_service.login_user("antero", "password123")
        self.budget_service.add_transaction("12.4.2022", "tulo", "253.69", "Tulonsiirrot", "Opintotuki")
        transaction = self.budget_service.find_transactions()[0]
        self.assertEqual(transaction[1], 25369)

    def test_add_expense_saves_the_amount_in_right_format(self):
        self.budget_service.login_user("antero", "password123")
        self.budget_service.add_transaction("12.4.2022", "meno", "648.23", "Asuminen", "Vuokra")
        transaction = self.budget_service.find_transactions()[0]
        self.assertEqual(transaction[1], -64823)

    def test_add_transaction_with_wrong_type_of_amount(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.add_transaction("12.4.2022", "meno", "5,12 €", "Asuminen", "Vuokra"), False)

    def test_find_transactions_when_not_logged_in(self):
        self.assertEqual(self.budget_service.find_transactions(), False)

    def test_find_transactions_when_logged_in(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(len(self.budget_service.find_transactions()), 0)

    def test_add_category_when_not_logged_in(self):
        self.assertEqual(self.budget_service.add_category("Testi"), False)

    def test_add_category_when_logged_in(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.add_category("Testi"), True)

    def test_delete_category_when_not_logged_in(self):
        self.assertEqual(self.budget_service.delete_category("Asuminen"), False)

    def test_delete_category_when_logged_in(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.delete_category("Asuminen"), True)

    def test_delete_category_that_does_not_exist(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.delete_category("Asumien"), False)

    def test_show_categories_when_not_logged_in(self):
        self.assertEqual(self.budget_service.get_categories("meno"), False)

    def test_show_expense_categories_when_logged_in(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(len(self.budget_service.get_categories("meno")), 18)

    def test_show_income_categories_when_logged_in(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(len(self.budget_service.get_categories("tulo")), 3)

    def test_show_categories_that_are_not_income_or_expense_categories(self):
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.get_categories("muu"), False)