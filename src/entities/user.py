class User:
    """Luokka, joka kuvaa yksittäistä käyttäjää."""

    def __init__(self, username, password):
        """Luokan konstruktori.

        Args:
            username: Käyttäjään liitetty käyttäjätunnus.
            password: Käyttäjään liitetty salasana.
        """

        self.username = username
        self.password = password
