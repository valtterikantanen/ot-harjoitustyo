from database_connection import get_database


class CategoryRepository:
    def __init__(self, database):
        self.database = database

    def find_all_expense_categories(self, user_id=None):
        if not user_id:
            categories = self.database.execute(
                "SELECT id, name FROM Categories WHERE type='expense' ORDER BY id").fetchall()
        else:
            categories = self.database.execute(
                "SELECT C.id, C.name FROM Categories C, CategoryVisibilities V "
                "WHERE C.type='expense' AND C.id=V.category_id AND V.user_id=? ORDER BY C.id",
                [user_id]).fetchall()

        return categories

    def find_all_income_categories(self, user_id=None):
        if not user_id:
            categories = self.database.execute(
                "SELECT id, name FROM Categories WHERE type='income' ORDER BY id").fetchall()
        else:
            categories = self.database.execute(
                "SELECT C.id, C.name FROM Categories C, CategoryVisibilities V "
                "WHERE C.type='income' AND C.id=V.category_id AND V.user_id=? ORDER BY C.id",
                [user_id]).fetchall()

        return categories

    def find_all_categories(self, user_id=None):
        if not user_id:
            categories = self.database.execute(
                "SELECT id, name FROM Categories ORDER BY id").fetchall()
        else:
            categories = self.database.execute(
                "SELECT C.id, C.name, C.type FROM Categories C, CategoryVisibilities V "
                "WHERE C.id=V.category_id AND V.user_id=? ORDER BY C.id", [user_id]).fetchall()

        return categories

    def add(self, name, category_type, user_id):
        if category_type == "expense":
            categories = self.find_all_expense_categories()
        else:
            categories = self.find_all_income_categories()
        if not (self.get_category_id(name), name) in categories:
            self.database.execute(
                "INSERT INTO Categories (name, type) VALUES (?, ?)", [name, category_type])
        category_id = self.get_category_id(name, category_type)
        self.database.execute(
            "INSERT INTO CategoryVisibilities (category_id, user_id) VALUES (?, ?)",
            [category_id, user_id])

    def add_default_categories(self, user_id):
        for i in range(1, 22):
            self.database.execute(
                "INSERT INTO CategoryVisibilities (category_id, user_id) VALUES (?, ?)",
                [i, user_id])

    def delete(self, category_id, user_id):
        self.database.execute(
            "DELETE FROM CategoryVisibilities WHERE category_id=? AND user_id=?",
            [category_id, user_id])

    def get_category_id(self, name, category_type=None):
        if not category_type:
            category_id = self.database.execute(
                "SELECT id FROM Categories WHERE name=?", [name]).fetchone()
        else:
            category_id = self.database.execute(
                "SELECT id FROM Categories WHERE name=? AND type=?",
                [name, category_type]).fetchone()
        return category_id[0] if category_id else None


category_repository = CategoryRepository(get_database())
