from datetime import datetime

import tkinter as tk
from tkinter import ttk

from services.budget_service import budget_service

class BudgetView:
    def __init__(self, root, show_login_view, show_new_expense_view, show_new_income_view):
        self._root = root
        self._show_login_view = show_login_view
        self._show_new_expense_view = show_new_expense_view
        self._show_new_income_view = show_new_income_view
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=tk.X, ipadx=5, ipady=5)

    def destroy(self):
        self._frame.destroy()

    def _initialize_username_label(self):
        username = budget_service.user.username
        lbl_username = tk.Label(master=self._frame, text=f"Käyttäjätunnus: {username}")
        lbl_username.grid(sticky=tk.constants.EW)

    def _initialize_transaction_list(self):
        transactions = budget_service.find_transactions()

        transaction_list = ttk.Treeview(self._frame)

        transaction_list["columns"] = ("date", "amount", "category", "description")

        transaction_list.column("#0", width=0, stretch=tk.NO)
        transaction_list.column("date", anchor=tk.CENTER, width=100)
        transaction_list.column("amount", anchor=tk.CENTER, width=100)
        transaction_list.column("category", anchor=tk.CENTER, width=200)
        transaction_list.column("description", anchor=tk.CENTER, width=200)

        transaction_list.heading("#0", text="", anchor=tk.CENTER)
        transaction_list.heading("date", text="Päivämäärä", anchor=tk.CENTER)
        transaction_list.heading("amount", text="Summa", anchor=tk.CENTER)
        transaction_list.heading("category", text="Kategoria", anchor=tk.CENTER)
        transaction_list.heading("description", text="Kuvaus", anchor=tk.CENTER)

        for i in range(len(transactions)):
            datetime_object = datetime.strptime(transactions[i][0], "%Y-%m-%d")
            date = datetime.strftime(datetime_object, "%-d.%-m.%Y")
            amount = f"{('%.2f' % (transactions[i][1] / 100)).replace('.', ',')} €"
            category = transactions[i][2]
            description = transactions[i][3]
            transaction_list.insert(parent="", index="end", iid=i, text="", values=(date, amount, category, description))

        transaction_list.grid(sticky=tk.constants.W, padx=5, pady=5)

    def _handle_log_out(self):
        if budget_service.logout_user():
            self._show_login_view()

    def _initialize_buttons(self):
        btn_new_expense = ttk.Button(master=self._frame, text="Lisää uusi meno", command=self._show_new_expense_view)
        btn_new_expense.grid(sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

        btn_new_income = ttk.Button(master=self._frame, text="Lisää uusi tulo", command=self._show_new_income_view)
        btn_new_income.grid(sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

        btn_log_out = ttk.Button(master=self._frame, text="Kirjaudu ulos", command=self._handle_log_out)
        btn_log_out.grid(sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._initialize_username_label()
        self._initialize_transaction_list()
        self._initialize_buttons()
