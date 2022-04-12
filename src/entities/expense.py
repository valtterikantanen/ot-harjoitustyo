class Expense:
    def __init__(self, date, amount, category_id, description, user):
        self.date = date
        self.amount = amount
        self.category_id = category_id
        self.description = description
        self.user = user
