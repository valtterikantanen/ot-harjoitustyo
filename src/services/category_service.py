from repositories.category_repository import category_repository


class CategoryService:
    """Sovelluslogiikasta vastaava luokka.
    """

    def __init__(self):
        """Luokan konstruktori.
        """

        self.category_repository = category_repository

    def get_all(self, user_id, category_type=None):
        """Hakee kategoriat.

        Args:
            user_id:
                Sen käyttäjän id, jonka kategoriat haetaan.
            category_type:
                Vapaaehtoinen, oletuksena None, jolloin haetaan sekä meno- että tulokategoriat.
                Jos halutaan vain toiset, niin parametrin arvo joko 'expense' tai 'income'.

        Returns:
            Lista kategorioista.
        """

        return self.category_repository.get_categories(user_id, category_type)

    def get_categories_in_use(self, user_id):
        """Hakee ne kategoriat, joissa käyttäjällä on vähintään yksi meno.

        Args:
            user_id: Sen käyttäjän id, jonka kategoriat haetaan.

        Returns:
            Lista kategorioista.
        """

        return self.category_repository.get_categories_in_use(user_id)

    def delete(self, category_id, user_id):
        """Poistaa kategorian näkyvistä.

        Args:
            category_id: Poistettavan kategorian id.
            user_id: Sen käyttäjän id, jolta kategoria poistetaan.
        """

        self.category_repository.delete(category_id, user_id)

    def add(self, name, category_type, user_id):
        """Luo uuden kategorian.

        Args:
            name: Lisättävän kategorian nimi.
            category_type: Lisättävän kategorian tyyppi ('expense' jos meno, 'income' jos tulo).
            user_id: Sen käyttäjän id, jolle kategoria lisätään.
        """

        self.category_repository.add(name, category_type, user_id)

    def add_default_categories(self, user_id):
        """Lisää käyttäjälle näkyviin valmiiksi asetetut kategoriat.

        Args:
            user_id: Sen käyttäjän id, jolle kategoriat lisätään.
        """

        self.category_repository.add_default_categories(user_id)

    def get_category_id(self, name, category_type):
        """Hakee kategorian id:n nimen perusteella.

        Args:
            name: Kategorian nimi.
            category_type: Kategorian tyyppi ('expense' jos meno, 'income' jos tulo).

        Returns:
            Kategorian id, jos kategoria löytyi, muuten None.
        """

        return self.category_repository.get_category_id(name, category_type)


category_service = CategoryService()
