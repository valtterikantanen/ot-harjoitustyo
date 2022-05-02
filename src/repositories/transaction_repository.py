from database_connection import get_database


class TransactionRepository:
    def __init__(self, database):
        self.database = database

    def add(self, transaction):
        date = transaction.date
        amount = transaction.amount
        category_id = transaction.category_id
        description = transaction.description
        user_id = self.database.execute(
            "SELECT id from Users WHERE username=?", [transaction.user.username]).fetchone()[0]

        self.database.execute(
            "INSERT INTO Transactions (date, amount, category_id, description, user_id) "
            "VALUES (?, ?, ?, ?, ?)", [date, amount, category_id, description, user_id])

    def find_all(self, user):
        user_id = self.database.execute(
            "SELECT id from Users WHERE username=?", [user.username]).fetchone()[0]

        transactions = self.database.execute(
            "SELECT T.date, T.amount, C.name AS category, T.description FROM Transactions T, "
            "Categories C WHERE T.user_id=? AND T.category_id=C.id ORDER BY T.date DESC",
            [user_id]).fetchall()

        return transactions


transaction_repository = TransactionRepository(get_database())
