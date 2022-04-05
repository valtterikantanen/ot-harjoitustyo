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
            else:
                self.print_guide()
            print()

    def print_guide(self):
        guide = {
            "0": "lopeta",
            "1": "kirjaudu sisään",
            "2": "luo uusi käyttäjätili",
            "3": "kirjaudu ulos"
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