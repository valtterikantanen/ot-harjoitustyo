from database_connection import get_database


class CategoryRepository:
    def __init__(self, database):
        self.database = database

    def find_all_expense_categories(self):
        categories = self.database.execute("SELECT id, name FROM Categories WHERE " \
                                           "visible=TRUE AND type='expense'").fetchall()

        return categories

    def find_all_income_categories(self):
        categories = self.database.execute("SELECT id, name FROM Categories WHERE " \
                                           "visible=TRUE AND type='income'").fetchall()

        return categories

    def add(self, name):
        if not self.find_one(name):
            self.database.execute(
                "INSERT INTO Categories (name) VALUES (?)", [name])
        else:
            self.database.execute(
                "UPDATE Categories SET visible=TRUE WHERE name=?", [name])

    def delete(self, name):
        self.database.execute(
            "UPDATE Categories SET visible=FALSE WHERE name=?", [name])

    def find_one(self, name):
        try:
            category_id = self.database.execute(
                "SELECT id FROM Categories WHERE name=?", [name]).fetchone()[0]
            return category_id
        except TypeError:
            return None


category_repository = CategoryRepository(get_database())
