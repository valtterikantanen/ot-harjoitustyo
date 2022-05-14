import unittest

from repositories.category_repository import CategoryRepository
from build import build
from database_connection import get_database


class TestCategoryRepository(unittest.TestCase):
    def setUp(self):
        build()
        self.category_repository = CategoryRepository(get_database())

    def test_get_all_categories_without_user_id(self):
        self.assertEqual(len(self.category_repository.get_categories()), 21)
