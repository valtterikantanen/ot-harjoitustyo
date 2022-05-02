class Transaction:
    """Luokka, joka kuvaa yksittäistä tapahtumaa.
    """

    def __init__(self, date, amount, category_id, user, description=None):
        """Luokan konstruktori.

        Args:
            date: Tapahtuman päivämäärä.
            amount: Tapahtuman summa.
            category_id: Tapahtuman kategorian id.
            user: User-olio, jolle tapahtuma kuuluu.
            description: Tapahtuman kuvaus. Vapaaehtoinen, oletuksena None.
        """

        self.date = date
        self.amount = amount
        self.category_id = category_id
        self.description = description
        self.user = user
