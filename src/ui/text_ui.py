from services.budget_service import budget_service


class TextUI:
    def __init__(self):
        self.budget_service = budget_service

    def start(self):
        self.print_guide()
        while True:
            answer = input("Komento: ")
            if answer == "0":
                break
            elif answer == "1":
                self.login_user()
            elif answer == "2":
                self.create_user()
            elif answer == "3":
                self.logout_user()
            elif answer == "4":
                self.add_transaction()
            elif answer == "5":
                self.show_transactions()
            elif answer == "6":
                self.print_categories()
            elif answer == "7":
                self.add_category()
            elif answer == "8":
                self.delete_category()
            else:
                self.print_guide()
            print()

    def print_guide(self):
        guide = {
            "0": "lopeta",
            "1": "kirjaudu sisään",
            "2": "luo uusi käyttäjätili",
            "3": "kirjaudu ulos",
            "4": "lisää uusi tapahtuma (vain sisäänkirjautuneena)",
            "5": "tarkastele tapahtumia (vain sisäänkirjautuneena)",
            "6": "listaa kategoriat (vain sisäänkirjautuneena)",
            "7": "lisää kategoria (vain sisäänkirjautuneena)",
            "8": "poista kategoria (vain sisäänkirjautuneena)"
        }

        print("Komennot:")
        for key, value in guide.items():
            print(f"{key}: {value}")

    def create_user(self):
        username = input("Käyttäjätunnus: ")
        password = input("Salasana: ")
        self.budget_service.create_user(username, password)

    def login_user(self):
        username = input("Käyttäjätunnus: ")
        password = input("Salasana: ")
        self.budget_service.login_user(username, password)

    def logout_user(self):
        self.budget_service.logout_user()

    def add_transaction(self):
        date = input("Päivämäärä: ")
        amount = input("Määrä (tulo positiivinen, meno negatiivinen): ")
        print("Kategoriat (menot 1–18, tulot 19–21):")
        self.print_categories()
        category_id = input("Valitse kategoria (luku 1-21): ")
        description = input("Syötä kuvaus (vapaaehtoinen): ")
        self.budget_service.add_transaction(
            date, amount, category_id, description)

    def show_transactions(self):
        transactions = self.budget_service.find_transactions()

        print("+------------+-------------+-----------------------------+--------------------------+")
        print("| Päivämäärä |    Summa    |          Kategoria          |          Kuvaus          |")
        print("+------------+-------------+-----------------------------+--------------------------+")

        for transaction in transactions:
            amount = "{0:.2f}".format(
                transaction[1] / 100).replace('.', ',') + " €"
            print(
                f"| {transaction[0]: <10} | {amount: <11} | {transaction[2]: <27} | {transaction[3]: <24} |")

        print("+------------+-------------+-----------------------------+--------------------------+")

    def print_categories(self):
        categories = self.budget_service.get_categories()
        if categories:
            for category in categories:
                print(f"{category[0]}: {category[1]}")

    def delete_category(self):
        name = input("Syötä sen kategorian nimi, jonka haluat poistaa: ")
        self.budget_service.delete_category(name)

    def add_category(self):
        name = input("Syötä lisättävän kategorian nimi: ")
        self.budget_service.add_category(name)
