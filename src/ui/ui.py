from ui.login_view import LoginView
from ui.create_user_view import CreateUserView
from ui.budget_view import BudgetView
from ui.category_view import CategoryView
from ui.add_category_view import AddCategoryView
from ui.edit_transaction_view import EditTransactionView
from ui.add_transaction_view import AddTransactionView

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

        self._current_view = BudgetView(self._root, self._show_login_view, self._show_add_transaction_view, self._show_category_view, self._show_edit_transaction_view)

        self._current_view.pack()

    def _show_category_view(self):
        self._hide_current_view()

        self._current_view = CategoryView(self._root, self._show_budget_view, self._show_add_category_view)

        self._current_view.pack()

    def _show_add_category_view(self):
        self._hide_current_view()

        self._current_view = AddCategoryView(self._root, self._show_category_view)

        self._current_view.pack()

    def _show_create_user_view(self):
        self._hide_current_view()

        self._current_view = CreateUserView(self._root, self._show_budget_view, self._show_login_view)

        self._current_view.pack()

    def _show_add_transaction_view(self, category_type):
        self._hide_current_view()

        self._current_view = AddTransactionView(self._root, self._show_budget_view, category_type)

        self._current_view.pack()

    def _show_edit_transaction_view(self, selected_item):
        self._hide_current_view()

        self._current_view = EditTransactionView(self._root, self._show_budget_view, selected_item)

        self._current_view.pack()