from database_connection import get_database
from entities.user import User


class UserRepository:
    """Luokka, joka vastaa käyttäjiin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, database):
        """Luokan konstruktori.

        Args:
            database: Tietokantayhteyden Connection-olio
        """

        self.database = database

    def create(self, user):
        """Tallentaa uuden käyttäjän tietokantaan.

        Args:
            user: Tallennettava käyttäjä User-oliona.

        Returns:
            Tallennetun käyttäjän id.
        """
        
        username = user.username
        password = user.password

        self.database.execute(
            "INSERT INTO Users (username, password) VALUES (?, ?)", [username, password])
        return self.get_user_id(username)

    def search_by_username(self, username):
        """Hakee käyttäjän.

        Args:
            username: Haettavan käyttäjän käyttäjänimi.

        Returns:
            Haettu käyttäjä User-oliona, jos käyttäjä on olemassa, muuten None.
        """

        result = self.database.execute(
            "SELECT username, password FROM Users WHERE username=?", [username]).fetchone()
        return User(result[0], result[1]) if result else False

    def get_user_id(self, username):
        """Hakee käyttäjän id:n.

        Args:
            username: Haettavan käyttäjän käyttäjänimi.

        Returns:
            Haetun käyttäjän id, jos käyttäjä on olemassa, muuten None.
        """

        user_id = self.database.execute(
            "SELECT id FROM Users WHERE username=?", [username]).fetchone()
        return user_id[0] if user_id else None


user_repository = UserRepository(get_database())
