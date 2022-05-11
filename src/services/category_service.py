from repositories.user_repository import user_repository
from repositories.category_repository import category_repository
from services.user_service import user_service


class CategoryService:
    """Sovelluslogiikasta vastaava luokka.
    """

    def __init__(self):
        """Luokan konstruktori.
        """

        self.user_repository = user_repository
        self.category_repository = category_repository
        self.user_service = user_service

    def get_all(self, category_type=None, user_id=None):
        """Hakee kategoriat.

        Args:
            category_type:
                Vapaaehtoinen, oletuksena None, jolloin haetaan sekä meno- että tulokategoriat.
                Jos halutaan vain toiset, niin parametrin arvo joko 'expense' tai 'income'.
            user_id:
                Vapaaehtoinen, oletuksena None, jolloin haetaan nykyisen käyttäjän kategoriat.
                Jos halutaan muun käyttäjän kategoriat, tulee parametrinä antaa käyttäjän id.

        Returns:
            Lista kategorioista.
        """

        if not user_id:
            user_id = self.user_repository.get_user_id(self.user_service.user.username)
        return self.category_repository.get_categories(user_id, category_type)

    def get_categories_in_use(self, user_id=None):
        """Hakee ne kategoriat, joissa käyttäjällä on vähintään yksi meno.

        Args:
            user_id:
                Vapaaehtoinen, oletuksena None, jolloin haetaan nykyisen käyttäjän kategoriat.
                Jos halutaan muun käyttäjän kategoriat, tulee parametrinä antaa käyttäjän id.

        Returns:
            Lista kategorioista.
        """

        if not user_id:
            user_id = self.user_repository.get_user_id(self.user_service.user.username)
        return self.category_repository.get_categories_in_use(user_id)

    def delete(self, category_id, user_id=None):
        """Poistaa kategorian näkyvistä.

        Args:
            category_id:
                Poistettavan kategorian id.
            user_id:
                Vapaaehtoinen, oletuksena None, jolloin poistetaan kategoria nykyiseltä
                käyttäjältä. Parametrina voidaan myös antaa sen käyttäjän id, jolta kategoria
                halutaan poistaa.
        """

        if not user_id:
            user_id = self.user_repository.get_user_id(self.user_service.user.username)
        self.category_repository.delete(category_id, user_id)

    def add(self, name, category_type, user_id=None):
        """Luo uuden kategorian.

        Args:
            name:
                Lisättävän kategorian nimi.
            category_type:
                Lisättävän kategorian tyyppi ('expense' jos meno, 'income' jos tulo).
            user_id:
                Vapaaehtoinen, oletuksena None, jolloin luodaan kategoria nykyiselle käyttäjälle.
                Voidaan myös antaa parametrina sen käyttäjän id, jolle kategoria lisätään.
        """

        if not user_id:
            user_id = self.user_repository.get_user_id(self.user_service.user.username)
        self.category_repository.add(name, category_type, user_id)


category_service = CategoryService()
