from database_connection import get_database


class TransactionRepository:
    """Luokka, joka vastaa tapahtumiin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, database):
        """Luokan konstruktori.

        Args:
            database: Tietokantayhteyden Connection-olio
        """

        self.database = database

    def add(self, date, amount, category_id, user_id, description=None):
        """Tallentaa uuden tapahtuman tietokantaan.

        Args:
            date: Päivämäärä merkkijonona (muodossa 'YYYY-MM-DD')
            amount: Summa kokonaislukuna (esim. summa 99,68 € esitetään muodossa 9968).
            category_id: Tapahtuman kategorian id.
            user_id: Sen käyttäjän id, jonka tapahtuma on kyseessä.
            description: Tapahtuman kuvaus. Vapaaehtoinen, oletuksena None.
        """

        self.database.execute(
            "INSERT INTO Transactions (date, amount, category_id, description, user_id) "
            "VALUES (?, ?, ?, ?, ?)", [date, amount, category_id, description, user_id])

    def update(self, transaction_id, date, amount, category_id, description):
        """Päivittää halutun tapahtuman tiedot tietokantaan.

        Args:
            transaction_id: Päivitettävän tapahtuman id.
            date: Päivämäärä merkkijonona (muodossa 'YYYY-MM-DD')
            amount: Summa kokonaislukuna (esim. summa 99,68 € esitetään muodossa 9968).
            category_id: Tapahtuman kategorian id.
            description: Tapahtuman kuvaus. Vapaaehtoinen, oletuksena None.
        """

        self.database.execute(
            "UPDATE Transactions SET date=?, amount=?, category_id=?, description=? WHERE id=?",
            [date, amount, category_id, description, transaction_id])

    def delete(self, transaction_id):
        """Poistaa tapahtuman tietokannasta.

        Args:
            transaction_id: Poistettavan tapahtuman id.
        """

        self.database.execute("DELETE FROM Transactions WHERE id=?", [transaction_id])

    def get_transaction(self, transaction_id):
        """Hakee yksittäisen tapahtuman.

        Args:
            transaction_id: Tapahtuman id.
        """

        transaction = self.database.execute(
            "SELECT T.date, T.amount, C.name AS category, T.description FROM Transactions T, "
            "Categories C WHERE T.id=? AND T.category_id=C.id", [transaction_id]).fetchone()

        return transaction

    def find_all(self, user_id, category_type=None):
        """Palauttaa kaikki käyttäjän tapahtumat.

        Args:
            user_id:
                Sen käyttäjän id, jonka tapahtumat haetaan.
            category_type:
                Vapaaehtoinen, oletuksena None, jolloin haetaan sekä menot että tulot. Jos halutaan
                vain menot, parametrin arvo on 'expense' ja jos vain menot, niin 'income'.

        Returns:
            Lista käyttäjän tapahtumista.
        """

        if not category_type:
            transactions = self.database.execute(
                "SELECT T.id, T.date, T.amount, C.name AS category, T.description FROM "
                "Transactions T, Categories C WHERE T.user_id=? AND T.category_id=C.id "
                "ORDER BY T.date DESC", [user_id]).fetchall()
        elif category_type == "expense":
            transactions = self.database.execute(
                "SELECT T.id, T.date, T.amount, C.name AS category, T.description FROM "
                "Transactions T, Categories C WHERE T.user_id=? AND T.category_id=C.id "
                "AND T.amount < 0 ORDER BY T.date DESC", [user_id]).fetchall()
        elif category_type == "income":
            transactions = self.database.execute(
                "SELECT T.id, T.date, T.amount, C.name AS category, T.description FROM "
                "Transactions T, Categories C WHERE T.user_id=? AND T.category_id=C.id "
                "AND T.amount >= 0 ORDER BY T.date DESC", [user_id]).fetchall()

        return transactions


transaction_repository = TransactionRepository(get_database())
