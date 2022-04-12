import unittest
from services.budget_service import BudgetService
from repositories.user_repository import UserRepository
from initialize_database import initialize_database
from database_connection import get_database


class TestBudgetService(unittest.TestCase):
    def setUp(self):
        initialize_database()
        self.budget_service = BudgetService()
        self.budget_service.user_repository = UserRepository(get_database())

    def test_sign_up_with_used_username(self):
        self.budget_service.create_user("antero", "password123")
        self.budget_service.create_user("antero", "password456")
        all_users = self.budget_service.user_repository.find_all_users()
        self.assertEqual(len(all_users), 1)

    def test_log_in_if_user_is_already_logged_in(self):
        self.budget_service.create_user("antero", "password123")
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.login_user(
            "antero", "password123"), False)

    def test_log_in_if_user_does_not_exist(self):
        self.budget_service.create_user("antero", "password123")
        self.assertEqual(self.budget_service.login_user(
            "atnero", "password123"), False)

    def test_log_in_if_password_is_wrong(self):
        self.budget_service.create_user("antero", "password123")
        self.assertEqual(self.budget_service.login_user(
            "antero", "pasword123"), False)

    def test_log_out_without_being_logged_in(self):
        self.assertEqual(self.budget_service.logout_user(), False)

    def test_log_out_when_logged_in(self):
        self.budget_service.create_user("antero", "password123")
        self.budget_service.login_user("antero", "password123")
        self.assertEqual(self.budget_service.logout_user(), True)
