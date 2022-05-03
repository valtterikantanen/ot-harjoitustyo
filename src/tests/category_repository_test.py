import unittest

from services.budget_service import BudgetService
from repositories.category_repository import CategoryRepository
from build import build
from database_connection import get_database


class TestCategoryRepository(unittest.TestCase):
    def setUp(self):
        build()
        self.budget_service = BudgetService()
        self.category_repository = CategoryRepository(get_database())
        self.budget_service.create_user("antero", "password123", "password123")
        self.budget_service.login_user("antero", "password123")

    def test_get_all_categories(self):
        self.assertEqual(len(self.category_repository.get_categories()), 21)

    def test_add_existing_category(self):
        self.category_repository.add("Asuminen", "expense", 1)
        self.assertEqual(len(self.category_repository.get_categories()), 21)
