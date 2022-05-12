import unittest

from services.user_service import user_service
from services.transaction_service import TransactionService
from repositories.category_repository import CategoryRepository
from build import build
from database_connection import get_database


class TestCategoryRepository(unittest.TestCase):
    def setUp(self):
        build()
        self.user_service = user_service
        self.transaction_service = TransactionService()
        self.category_repository = CategoryRepository(get_database())
        self.user_service.create("antero", "password123", "password123")
        self.user_service.login("antero", "password123")
        self.category_repository.add_default_categories(1)

    def test_get_all_categories(self):
        self.assertEqual(len(self.category_repository.get_categories()), 21)

    def test_add_existing_category(self):
        self.category_repository.add("Asuminen", "expense", 1)
        self.assertEqual(len(self.category_repository.get_categories()), 21)

    def test_add_new_category(self):
        self.category_repository.add("Testimeno", "expense", 1)
        self.assertEqual(len(self.category_repository.get_categories()), 22)
