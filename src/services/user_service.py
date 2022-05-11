from entities.user import User
from repositories.user_repository import user_repository
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


class UserService:
    """Käyttäjiin liittyvästä sovelluslogiikasta vastaava luokka.
    """

    def __init__(self):
        """Luokan konstruktori.
        """

        self.user = None
        self.user_repository = user_repository
        self.category_repository = category_repository

    def create(self, username, password1, password2):
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

    def login(self, username, password):
        """Kirjaa käyttäjän sisään.

        Args:
            username: Käyttäjän käyttäjätunnus.
            password: Käyttäjän salasana.

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

    def logout(self):
        """Kirjaa mahdollisesti sisäänkirjautuneen käyttäjän ulos.
        """

        self.user = None


user_service = UserService()
