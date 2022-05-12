from database_connection import get_database


class CategoryRepository:
    """Luokka, joka vastaa kategorioihin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, database):
        """Luokan konstruktori.

        Args:
            database: Tietokantayhteyden Connection-olio
        """

        self.database = database

    def get_categories(self, user_id=None, category_type=None):
        """Palauttaa kategoriat.

        Args:
            user_id:
                Vapaaehtoinen, oletuksena None, jolloin palautetaan kaikkien käyttäjien kategoriat.
                Jos arvo on annettu, palautetaan vain kyseisen käyttäjän kategoriat.
            category_type:
                Vapaaehtoinen, oletuksena None, jolloin palautetaan sekä meno- että tulokategoriat.
                Jos arvo on annettu, palautetaan vain joko meno- tai tulokategoriat.

        Returns:
            Lista kategorioista.
        """

        if not user_id:
            if not category_type:
                categories = self.database.execute(
                    "SELECT id, name, type FROM Categories ORDER BY id").fetchall()
            else:
                categories = self.database.execute(
                    "SELECT id, name, type FROM Categories WHERE type IN (?) ORDER BY id",
                    [category_type]).fetchall()
        else:
            if not category_type:
                categories = self.database.execute(
                    "SELECT C.id, C.name, C.type FROM Categories C, CategoryVisibilities V WHERE "
                    "C.id=V.category_id AND V.user_id=? ORDER BY C.id", [user_id]).fetchall()
            else:
                categories = self.database.execute(
                    "SELECT C.id, C.name, C.type FROM Categories C, CategoryVisibilities V WHERE "
                    "C.type IN (?) AND C.id=V.category_id AND V.user_id=? ORDER BY C.id",
                    [category_type, user_id]).fetchall()

        return categories

    def get_categories_in_use(self, user_id):
        """Hakee ne kategoriat, joissa käyttäjällä on vähintään yksi tapahtuma.

        Args:
            user_id: Sen käyttäjän id, jonka kategoriat haetaan.

        Returns:
            Lista kategorioista.
        """

        categories = self.database.execute(
            "SELECT DISTINCT C.id, C.name from Transactions T, Categories C WHERE T.user_id=? AND "
            "C.id=T.category_id ORDER BY C.name", [user_id]).fetchall()

        return categories

    def add(self, name, category_type, user_id):
        """Tallentaa uuden kategorian tietokantaan. Jos halutunniminen kategoria on jo olemassa,
        se vain lisätään käyttäjän näkemiin kategorioihin.

        Args:
            name: Kategorian nimi.
            category_type: Kategorian tyyppi ('expense' jos meno, 'income' jos tulo).
            user_id: Sen käyttäjän id, jolle uusi kategoria lisätään.
        """

        categories = self.get_categories(category_type=category_type)

        if not (self.get_category_id(name), name, category_type) in categories:
            self.database.execute(
                "INSERT INTO Categories (name, type) VALUES (?, ?)", [name, category_type])
        category_id = self.get_category_id(name, category_type)
        count = self.database.execute(
            "SELECT COUNT(*) FROM CategoryVisibilities WHERE category_id=? AND user_id=?",
            [category_id, user_id]).fetchone()[0]
        if count == 0:
            self.database.execute(
                "INSERT INTO CategoryVisibilities (category_id, user_id) VALUES (?, ?)",
                [category_id, user_id])

    def add_default_categories(self, user_id):
        """Lisää käyttäjälle näkyviin valmiiksi asetetut kategoriat.

        Args:
            user_id: Sen käyttäjän id, jolle kategoriat lisätään.
        """

        for i in range(1, 22):
            self.database.execute(
                "INSERT INTO CategoryVisibilities (category_id, user_id) VALUES (?, ?)",
                [i, user_id])

    def delete(self, category_id, user_id):
        """Poistaa käyttäjältä näkyvistä parametrina annetun kategorian.

        Args:
            category_id: Sen kategorian id, joka poistetaan näkyvistä.
            user_id: Sen käyttäjän id, jolta kategoria poistetaan näkyvistä.
        """

        self.database.execute(
            "DELETE FROM CategoryVisibilities WHERE category_id=? AND user_id=?",
            [category_id, user_id])

    def get_category_id(self, name, category_type=None):
        """Palauttaa haetun kategorian id:n.

        Args:
            name:
                Haetun kategorian nimi.
            category_type:
                Vapaaehtoinen, oletuksena None, jolloin haetaan kaikista kategorioista. Jos arvo
                on annettu, haetaan vain joko meno- tai tulokategorioista ('expense' jos meno,
                'income' jos tulo).

        Returns:
            Haetun kategorian id, jos kategoria on olemassa, muuten None.
        """

        if not category_type:
            category_id = self.database.execute(
                "SELECT id FROM Categories WHERE name=?", [name]).fetchone()
        else:
            category_id = self.database.execute(
                "SELECT id FROM Categories WHERE name=? AND type=?",
                [name, category_type]).fetchone()
        return category_id[0] if category_id else None


category_repository = CategoryRepository(get_database())
