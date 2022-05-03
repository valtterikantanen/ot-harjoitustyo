from entities.user import User
from entities.transaction import Transaction
from repositories.user_repository import user_repository
from repositories.transaction_repository import transaction_repository
from repositories.category_repository import category_repository

class PasswordsDontMatchError(Exception):
    pass

class UsernameAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

class InvalidUsernameOrPasswordError(Exception):
    pass

class AmountInWrongFormatError(Exception):
    pass

class TooBigNumberError(Exception):
    pass


class BudgetService:
    """Sovelluslogiikasta vastaava luokka.
    """

    def __init__(self):
        """Luokan konstruktori.
        """

        self.user = None
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def create_user(self, username, password1, password2):
        """Luo uuden käyttäjän ja lisää hänen käyttöönsä oletuskategoriat.

        Args:
            username: Haluttu käyttäjätunnus.
            password1: Haluttu salasana.
            password2: Haluttu salasana toiseen kertaan.

        Raises:
            UsernameAlreadyExistsError: Virhe, joka tapahtuu, kun käyttäjätunnus on jo käytössä.
            PasswordsDontMatchError:
                Virhe, joka tapahtuu, kun ensimmäinen ja toinen salasana eivät vastaa toisiaan.
            InvalidUsernameOrPasswordError:
                Virhe, joka tapahtuu, kun käyttäjänimi tai salasana on tyhjä.
        """
        
        if self.user_repository.search_by_username(username):
            raise UsernameAlreadyExistsError()
        if password1 != password2:
            raise PasswordsDontMatchError()
        if len(username.strip()) == 0 or len(password1.strip()) == 0:
            raise InvalidUsernameOrPasswordError()

        user_id = self.user_repository.create(User(username, password1))
        self.category_repository.add_default_categories(user_id)

    def login_user(self, username, password):
        """Kirjaa käyttäjän sisään.

        Args:
            username (_type_): Käyttäjän käyttäjätunnus.
            password (_type_): Käyttäjän salasana.

        Raises:
            UserNotFoundError:
                Virhe, joka tapahtuu, kun käyttäjän antamaa käyttäjätunnusta vastaavaa käyttäjää
                ei ole olemassa.
            WrongPasswordError: Virhe, joka tapahtuu, kun käyttäjän antama salasana on väärä.
        """

        result = self.user_repository.search_by_username(username)
        if not result:
            raise UserNotFoundError()
        if password != result.password:
            raise WrongPasswordError()

        self.user = result

    def logout_user(self):
        """Kirjaa mahdollisesti sisäänkirjautuneen käyttäjän ulos.
        """

        self.user = None

    def validate_transaction_data(self, category_type, amount):
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
        if category_type == "expense":
            amount = f"-{amount}"

        try:
            amount = int(100 * float(amount))
        except ValueError as exc:
            raise AmountInWrongFormatError() from exc

        if amount < -9223372036854775808 or amount > 9223372036854775807:
            raise TooBigNumberError()

        return amount

    def add_transaction(self, date, category_type, amount, category, description=None):
        """Luo uuden tapahtuman.

        Args:
            date: Päivämäärä merkkijonona (muodossa 'YYYY-MM-DD')
            category_type: Tapahtumatyyppi ('expense' jos meno, 'income' jos tulo).
            amount: Summa merkkijonona (muodossa '0,00' tai '0.00').
            category: Tapahtuman kategoria
            description: Tapahtuman kuvaus. Vapaaehtoinen, oletuksena None.
        """

        amount = self.validate_transaction_data(category_type, amount)

        category_id = self.category_repository.get_category_id(category)

        self.transaction_repository.add(Transaction(
            date, amount, category_id, self.user, description))

    def update_transaction(self, transaction_id, date, category_type, amount, category, description=None):
        """Päivittää halutun tapahtuman tiedot.

        Args:
            transaction_id: Tapahtuman id.
            date: Päivämäärä merkkijonona (muodossa 'YYYY-MM-DD')
            category_type: Tapahtumatyyppi ('expense' jos meno, 'income' jos tulo).
            amount: Summa merkkijonona (muodossa '0,00' tai '0.00').
            category: Tapahtuman kategoria
            description: Tapahtuman kuvaus. Vapaaehtoinen, oletuksena None.
        """

        amount = self.validate_transaction_data(category_type, amount)
        category_id = self.category_repository.get_category_id(category)

        self.transaction_repository.update(transaction_id, Transaction(
            date, amount, category_id, self.user, description))

    def find_transactions(self):
        """Hakee nykyisen käyttäjän tapahtumat.

        Returns:
            Lista käyttäjän tapahtumista.
        """

        user_id = self.user_repository.get_user_id(self.user.username)
        return self.transaction_repository.find_all(user_id)

    def get_transaction(self, transaction_id):
        """Hakee yksittäisen tapahtuman.

        Args:
            transaction_id: Tapahtuman id.

        Returns:
            Tapahtuma tuplena, jonka kenttinä on päivämäärä, summa, kategoria ja kuvaus.
        """
        
        return self.transaction_repository.get_transaction(transaction_id)

    def delete_transaction(self, transaction_id):
        """Poistaa tapahtuman.

        Args:
            transaction_id: Poistettavan tapahtuman id.
        """

        self.transaction_repository.delete(transaction_id)

    def get_categories(self, category_type):
        """Hakee nykyisen käyttäjän kategoriat.

        Args:
            category_type:
                Haettavien kategorioiden tyyppi ('expense' jos meno, 'income' jos tulo).

        Returns:
            Lista kategorioista.
        """

        user_id = self.user_repository.get_user_id(self.user.username)
        return self.category_repository.get_categories(user_id, category_type)

    def delete_category(self, category_id):
        """Poistaa kategorian näkyvistä nykyiseltä käyttäjältä.

        Args:
            category_id: Poistettavan kategorian id.
        """

        user_id = self.user_repository.get_user_id(self.user.username)
        self.category_repository.delete(category_id, user_id)

    def add_category(self, name, category_type):
        """Luo uuden kategorian.

        Args:
            name: Lisättävän kategorian nimi.
            category_type: Lisättävän kategorian tyyppi ('expense' jos meno, 'income' jos tulo).
        """

        user_id = self.user_repository.get_user_id(self.user.username)
        self.category_repository.add(name, category_type, user_id)


budget_service = BudgetService()
