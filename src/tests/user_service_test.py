import unittest

from services.user_service import UserService, PasswordsDontMatchError, UsernameAlreadyExistsError, UserNotFoundError, WrongPasswordError, InvalidUsernameOrPasswordError
from build import build


class TestBudgetService(unittest.TestCase):
    def setUp(self):
        build()
        self.user_service = UserService()
        self.user_service.create("antero", "password123", "password123")
        self.user_service.login("antero", "password123")

    def test_sign_up_with_used_username(self):
        self.assertRaises(UsernameAlreadyExistsError, self.user_service.create, "antero", "password456", "password456")

    def test_sign_up_with_empty_username(self):
        self.assertRaises(InvalidUsernameOrPasswordError, self.user_service.create, "", "password456", "password456")

    def test_sign_up_with_empty_password(self):
        self.assertRaises(InvalidUsernameOrPasswordError, self.user_service.create, "ilmari", " ", " ")

    def test_sign_up_with_wrong_password_confirmation(self):
        self.assertRaises(PasswordsDontMatchError, self.user_service.create, "ilmari", "password123", "password132")

    def test_log_in_if_user_does_not_exist(self):
        self.assertRaises(UserNotFoundError, self.user_service.login, "atnero", "password123")

    def test_log_in_if_password_is_wrong(self):
        self.assertRaises(WrongPasswordError, self.user_service.login, "antero", "pasword123")

    def test_log_out_when_logged_in(self):
        self.user_service.logout()
        self.assertEqual(self.user_service.user, None)

    def test_get_current_user_id(self):
        self.assertEqual(self.user_service.get_current_user_id(), 1)