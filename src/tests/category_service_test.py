import unittest

from services.category_service import CategoryService
from services.transaction_service import TransactionService
from services.user_service import user_service
from build import build


class TestCategoryService(unittest.TestCase):
    def setUp(self):
        build()
        self.category_service = CategoryService()
        self.transaction_service = TransactionService()
        self.user_service = user_service
        self.user_service.create("antero", "password123", "password123")
        self.user_service.login("antero", "password123")
        self.category_service.add_default_categories(1)

    def test_add_new_category(self):
        self.assertEqual(len(self.category_service.get_all(1)), 21)
        self.category_service.add("Testimeno", "Meno", 1)
        self.category_service.add("Testitulo", "Tulo", 1)
        self.assertEqual(len(self.category_service.get_all(1)), 23)

    def test_add_existing_category(self):
        self.category_service.add("Asuminen", "expense", 1)
        self.assertEqual(len(self.category_service.get_all(1)), 21)

    def test_delete_category(self):
        self.assertEqual(len(self.category_service.get_all(1)), 21)
        self.category_service.delete(1, 1)
        self.category_service.delete(2, 1)
        self.assertEqual(len(self.category_service.get_all(1)), 19)

    def test_show_all_categories(self):
        self.assertEqual(len(self.category_service.get_all(1)), 21)

    def test_show_expense_categories(self):
        self.assertEqual(len(self.category_service.get_all(1, "expense")), 18)

    def test_show_income_categories(self):
        self.assertEqual(len(self.category_service.get_all(1, "income")), 3)

    def test_get_categories_in_use(self):
        self.transaction_service.create("03.05.2022", "expense", "32.87", 13, 1)
        self.transaction_service.create("03.05.2022", "income", "2132.87", 19, 1)
        self.transaction_service.create("04.05.2022", "expense", "4.91", 13, 1)
        self.assertEqual(len(self.category_service.get_categories_in_use(1)), 2)

    def test_get_category_id(self):
        id = self.category_service.get_category_id("Asuminen", "expense")
        self.assertEqual(id, 2)