import unittest

from services.transaction_service import TransactionService, AmountInWrongFormatError, TooBigNumberError
from services.user_service import UserService
from build import build


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        build()
        self.transaction_service = TransactionService()
        self.user_service = UserService()
        self.user_service.create("antero", "password123", "password123")
        self.user_service.login("antero", "password123")

    def test_add_income_saves_the_amount_in_right_format(self):
        self.transaction_service.create("2022-04-12", "income", "253.69", "Tulonsiirrot", "Opintotuki", 1)
        transaction = self.transaction_service.get_one(1)
        self.assertEqual(transaction, ("2022-04-12", 25369, "Tulonsiirrot", "Opintotuki"))

    def test_add_expense_saves_the_amount_in_right_format(self):
        self.transaction_service.create("2022-04-12", "expense", "648.23", "Asuminen", "Vuokra", 1)
        transaction = self.transaction_service.get_all(1)[0]
        self.assertEqual(transaction[2], -64823)

    def test_add_transaction_with_too_big_amount(self):
        self.assertRaises(TooBigNumberError, self.transaction_service.create, "2022-04-12", "expense", "9223372036854775808", "Asuminen", "Vuokra")
        
    def test_add_transaction_with_wrong_type_of_amount(self):
        self.assertRaises(AmountInWrongFormatError, self.transaction_service.create, "2022-04-12", "expense", "648,23 €", "Asuminen", "Vuokra")

    def test_add_transaction_with_a_minus_sign(self):
        self.assertRaises(AmountInWrongFormatError, self.transaction_service.create, "2022-04-12", "expense", "-648.23", "Asuminen", "Vuokra")

    def test_get_transaction(self):
        self.transaction_service.create("2022-05-03", "expense", "32.87", "Ruoka ja päivittäistavarat", user_id=1)
        transaction = self.transaction_service.get_one(1)
        self.assertEqual(transaction, ("2022-05-03", -3287, "Ruoka ja päivittäistavarat", None))

    def test_update_transaction(self):
        self.transaction_service.create("2022-05-03", "expense", "32.87", "Ruoka ja päivittäistavarat", user_id=1)
        self.transaction_service.update(1, "2022-05-03", "expense", "32.85", "Ruoka ja päivittäistavarat")
        transaction = self.transaction_service.get_one(1)
        self.assertEqual(transaction, ("2022-05-03", -3285, "Ruoka ja päivittäistavarat", None))

    def test_delete_transaction(self):
        self.transaction_service.create("2022-05-03", "expense", "32.87", "Ruoka ja päivittäistavarat", user_id=1)
        self.transaction_service.delete(1)
        self.assertEqual(len(self.transaction_service.get_all(1)), 0)