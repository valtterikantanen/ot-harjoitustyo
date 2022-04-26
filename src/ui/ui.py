from ui.login_view import LoginView
from ui.create_user_view import CreateUserView
from ui.budget_view import BudgetView
from ui.add_expense_view import AddExpenseView
from ui.add_income_view import AddIncomeView

class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_login_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_login_view(self):
        self._hide_current_view()

        self._current_view = LoginView(self._root, self._show_budget_view, self._show_create_user_view)

        self._current_view.pack()

    def _show_budget_view(self):
        self._hide_current_view()

        self._current_view = BudgetView(self._root, self._show_login_view, self._show_new_expense_view, self._show_new_income_view)

        self._current_view.pack()

    def _show_create_user_view(self):
        self._hide_current_view()

        self._current_view = CreateUserView(self._root, self._show_budget_view, self._show_login_view)

        self._current_view.pack()

    def _show_new_expense_view(self):
        self._hide_current_view()

        self._current_view = AddExpenseView(self._root, self._show_budget_view)

        self._current_view.pack()

    def _show_new_income_view(self):
        self._hide_current_view()

        self._current_view = AddIncomeView(self._root, self._show_budget_view)

        self._current_view.pack()