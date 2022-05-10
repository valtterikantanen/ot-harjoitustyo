from repositories.user_repository import user_repository
from repositories.transaction_repository import transaction_repository
from repositories.category_repository import category_repository
from services.user_service import user_service

class AmountInWrongFormatError(Exception):
    pass

class TooBigNumberError(Exception):
    pass


class TransactionService:
    """Tapahtumiin liittyvästä sovelluslogiikasta vastaava luokka.
    """

    def __init__(self):
        """Luokan konstruktori.
        """

        self.user_repository = user_repository
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self.user_service = user_service

    def validate_data(self, category_type, amount):
        """Validoi uuteen tai päivitettävään tapahtumaan liittyviä tietoja.

        Args:
            category_type: Tapahtumatyyppi ('expense' jos meno, 'income' jos tulo).
            amount: Summa merkkijonona (muodossa '0,00' tai '0.00').

        Raises:
            AmountInWrongFormatError: Virhe, joka tapahtuu, kun summa on väärässä muodossa.
            TooBigNumberError: Virhe, joka tapahtuu, kun summa on liian suuri.

        Returns:
            Summa kokonaislukuna (esim. summa 99,68 € esitetään muodossa 9968).
        """

        amount = amount.replace(",", ".")

        if "-" in amount:
            raise AmountInWrongFormatError()
        
        if category_type == "expense":
            amount = f"-{amount}"

        try:
            amount = round(100 * float(amount))
        except ValueError as exc:
            raise AmountInWrongFormatError() from exc

        if amount < -999_999_999 or amount > 999_999_999:
            raise TooBigNumberError()

        return amount

    def create(self, date, category_type, amount, category, description=None, user_id=None):
        """Luo uuden tapahtuman.

        Args:
            date:
                Päivämäärä merkkijonona (muodossa 'YYYY-MM-DD')
            category_type:
                Tapahtumatyyppi ('expense' jos meno, 'income' jos tulo).
            amount:
                Summa merkkijonona (muodossa '0,00' tai '0.00').
            category:
                Tapahtuman kategoria
            description: 
                Tapahtuman kuvaus. Vapaaehtoinen, oletuksena None.
            user_id:
                Sen käyttäjän id, jonka tapahtuma on kyseessä. Oletuksena None, jolloin tapahtuma
                lisätään nykyiselle käyttäjälle. 
        """

        amount = self.validate_data(category_type, amount)

        category_id = self.category_repository.get_category_id(category)

        if not user_id:
            user_id = self.user_repository.get_user_id(self.user_service.user.username)

        self.transaction_repository.add(date, amount, category_id, user_id, description)

    def update(self, transaction_id, date, category_type, amount, category, description=None):
        """Päivittää halutun tapahtuman tiedot.

        Args:
            transaction_id: Tapahtuman id.
            date: Päivämäärä merkkijonona (muodossa 'YYYY-MM-DD')
            category_type: Tapahtumatyyppi ('expense' jos meno, 'income' jos tulo).
            amount: Summa merkkijonona (muodossa '0,00' tai '0.00').
            category: Tapahtuman kategoria
            description: Tapahtuman kuvaus. Vapaaehtoinen, oletuksena None.
        """

        amount = self.validate_data(category_type, amount)
        category_id = self.category_repository.get_category_id(category)

        self.transaction_repository.update(transaction_id, date, amount, category_id, description)

    def get_all(self, user_id=None):
        """Hakee nykyisen käyttäjän tapahtumat.

        Args:
            user_id:
                Sen käyttäjän id, jonka tapahtumat haetaan. Vapaaehtoinen, oletuksen None, jolloin
                haetaan nykyisen käyttäjän tapahtumat.

        Returns:
            Lista käyttäjän tapahtumista.
        """
        if not user_id:
            user_id = self.user_repository.get_user_id(self.user_service.user.username)
        return self.transaction_repository.find_all(user_id)

    def get_one(self, transaction_id):
        """Hakee yksittäisen tapahtuman.

        Args:
            transaction_id: Tapahtuman id.

        Returns:
            Tapahtuma tuplena, jonka kenttinä on päivämäärä, summa, kategoria ja kuvaus.
        """

        return self.transaction_repository.get_transaction(transaction_id)

    def delete(self, transaction_id):
        """Poistaa tapahtuman.

        Args:
            transaction_id: Poistettavan tapahtuman id.
        """

        self.transaction_repository.delete(transaction_id)


transaction_service = TransactionService()
