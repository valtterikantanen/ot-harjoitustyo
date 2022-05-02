from database_connection import get_database
from repositories.user_repository import user_repository


class TransactionRepository:
    """Luokka, joka vastaa tapahtumiin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, database):
        """Luokan konstruktori.

        Args:
            database: Tietokantayhteyden Connection-olio
        """

        self.database = database

    def add(self, transaction):
        """Tallentaa uuden tapahtuman tietokantaan.

        Args:
            transaction: Tallennettava tapahtuma Transaction-oliona.
        """

        date = transaction.date
        amount = transaction.amount
        category_id = transaction.category_id
        description = transaction.description
        user_id = user_repository.get_user_id(transaction.user.username)

        self.database.execute(
            "INSERT INTO Transactions (date, amount, category_id, description, user_id) "
            "VALUES (?, ?, ?, ?, ?)", [date, amount, category_id, description, user_id])

    def find_all(self, user_id):
        """Palauttaa kaikki käyttäjän tapahtumat.

        Args:
            user_id: Sen käyttäjän id, jonka tapahtumat haetaan.

        Returns:
            Lista käyttäjän tapahtumista.
        """

        transactions = self.database.execute(
            "SELECT T.date, T.amount, C.name AS category, T.description FROM Transactions T, "
            "Categories C WHERE T.user_id=? AND T.category_id=C.id ORDER BY T.date DESC",
            [user_id]).fetchall()

        return transactions


transaction_repository = TransactionRepository(get_database())
