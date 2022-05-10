import unittest

from services.category_service import CategoryService
from services.user_service import UserService
from build import build


class TestCategoryService(unittest.TestCase):
    def setUp(self):
        build()
        self.category_service = CategoryService()
        self.user_service = UserService()
        self.user_service.create("antero", "password123", "password123")
        self.user_service.login("antero", "password123")

    def test_add_category(self):
        self.assertEqual(len(self.category_service.get_all(user_id=1)), 21)
        self.category_service.add("Testi", "Meno", 1)
        self.assertEqual(len(self.category_service.get_all(user_id=1)), 22)

    def test_delete_category(self):
        self.assertEqual(len(self.category_service.get_all(user_id=1)), 21)
        self.category_service.delete(1, 1)
        self.assertEqual(len(self.category_service.get_all(user_id=1)), 20)

    def test_show_all_categories(self):
        self.assertEqual(len(self.category_service.get_all(user_id=1)), 21)

    def test_show_expense_categories(self):
        self.assertEqual(len(self.category_service.get_all("expense", 1)), 18)

    def test_show_income_categories(self):
        self.assertEqual(len(self.category_service.get_all("income", 1)), 3)