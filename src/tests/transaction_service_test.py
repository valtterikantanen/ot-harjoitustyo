import unittest

from services.transaction_service import TransactionService, AmountInWrongFormatError, TooBigNumberError, DateInWrongFormatError
from services.user_service import user_service
from build import build


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        build()
        self.transaction_service = TransactionService()
        self.user_service = user_service
        self.user_service.create("antero", "password123", "password123")
        self.user_service.login("antero", "password123")

    def test_add_income_saves_the_amount_in_right_format(self):
        self.transaction_service.create("12.04.2022", "income", "253.69", "Tulonsiirrot", "Opintotuki")
        transaction = self.transaction_service.get_one(1)
        self.assertEqual(transaction, ("2022-04-12", 25369, "Tulonsiirrot", "Opintotuki"))

    def test_add_expense_saves_the_amount_in_right_format(self):
        self.transaction_service.create("12.04.2022", "expense", "648.23", "Asuminen", "Vuokra")
        transaction = self.transaction_service.get_all(1)[0]
        self.assertEqual(transaction[2], -64823)

    def test_create_transaction_works_without_user_id(self):
        self.transaction_service.create("12.04.2022", "expense", "648.23", "Asuminen", "Vuokra", user_id=1)
        self.transaction_service.create("12.04.2022", "income", "253.69", "Tulonsiirrot", "Opintotuki")
        self.assertEqual(len(self.transaction_service.get_all()), 2)

    def test_get_all_works_with_category_type(self):
        self.transaction_service.create("12.04.2022", "expense", "648.23", "Asuminen", "Vuokra", user_id=1)
        self.transaction_service.create("12.04.2022", "income", "253.69", "Tulonsiirrot", "Opintotuki")
        self.assertEqual(len(self.transaction_service.get_all(category_type="expense")), 1)
        self.assertEqual(len(self.transaction_service.get_all(category_type="income")), 1)

    def test_get_all_returns_empty_list_with_false_category_type(self):
        self.transaction_service.create("12.04.2022", "expense", "648.23", "Asuminen", "Vuokra", user_id=1)
        self.transaction_service.create("12.04.2022", "income", "253.69", "Tulonsiirrot", "Opintotuki")
        self.assertEqual(len(self.transaction_service.get_all(category_type="expence")), 0)

    def test_add_transaction_with_too_big_amount(self):
        self.assertRaises(TooBigNumberError, self.transaction_service.create, "12.04.2022", "expense", "10000000", "Asuminen", "Vuokra")
        
    def test_add_transaction_with_wrong_type_of_amount(self):
        self.assertRaises(AmountInWrongFormatError, self.transaction_service.create, "12.04.2022", "expense", "648,23 €", "Asuminen", "Vuokra")

    def test_add_transaction_with_a_minus_sign(self):
        self.assertRaises(AmountInWrongFormatError, self.transaction_service.create, "12.04.2022", "expense", "-648.23", "Asuminen", "Vuokra")

    def test_add_transaction_with_a_date_in_wrong_fromat(self):
        self.assertRaises(DateInWrongFormatError, self.transaction_service.create, "2022-04-12", "expense", "648.23", "Asuminen", "Vuokra")

    def test_get_transaction(self):
        self.transaction_service.create("03.05.2022", "expense", "32.87", "Ruoka ja päivittäistavarat")
        transaction = self.transaction_service.get_one(1)
        self.assertEqual(transaction, ("2022-05-03", -3287, "Ruoka ja päivittäistavarat", None))

    def test_get_minimum_date(self):
        self.transaction_service.create("03.05.2022", "expense", "32.87", "Ruoka ja päivittäistavarat")
        self.transaction_service.create("03.02.2022", "income", "2132.87", "Palkka")
        self.transaction_service.create("03.04.2021", "expense", "4.91", "Ruoka ja päivittäistavarat")
        self.assertEqual(self.transaction_service.get_minimum_date(), "2021-04-03")
        self.assertEqual(self.transaction_service.get_minimum_date(1), "2021-04-03")

    def test_get_maximum_date(self):
        self.transaction_service.create("03.05.2022", "expense", "32.87", "Ruoka ja päivittäistavarat")
        self.transaction_service.create("03.02.2022", "income", "2132.87", "Palkka")
        self.transaction_service.create("03.04.2021", "expense", "4.91", "Ruoka ja päivittäistavarat")
        self.assertEqual(self.transaction_service.get_maximum_date(), "2022-05-03")
        self.assertEqual(self.transaction_service.get_maximum_date(1), "2022-05-03")

    def test_update_transaction(self):
        self.transaction_service.create("03.05.2022", "expense", "32.87", "Ruoka ja päivittäistavarat")
        self.transaction_service.update(1, "03.05.2022", "expense", "32.85", "Ruoka ja päivittäistavarat")
        transaction = self.transaction_service.get_one(1)
        self.assertEqual(transaction, ("2022-05-03", -3285, "Ruoka ja päivittäistavarat", None))

    def test_delete_transaction(self):
        self.transaction_service.create("03.05.2022", "expense", "32.87", "Ruoka ja päivittäistavarat")
        self.transaction_service.delete(1)
        self.assertEqual(len(self.transaction_service.get_all()), 0)