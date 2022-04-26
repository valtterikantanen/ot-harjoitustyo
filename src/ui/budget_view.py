import tkinter as tk
from tkinter import ttk

from services.budget_service import budget_service

class BudgetView:
    def __init__(self, root, handle_show_login_view, show_new_expense_view, show_new_income_view):
        self._root = root
        self._handle_show_login_view = handle_show_login_view
        self._show_new_expense_view = show_new_expense_view
        self._show_new_income_view = show_new_income_view
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=tk.X, ipadx=5, ipady=5)

    def destroy(self):
        self._frame.destroy()

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
            transaction_list.insert(parent="", index="end", iid=i, text="", values=(transactions[i][0], str(transactions[i][1] / 100).replace(".", ",") + " €", transactions[i][2], transactions[i][3]))

        transaction_list.grid(row=0, column=0, sticky=tk.constants.W, padx=5, pady=5)

    def _initialize_buttons(self):
        btn_new_expense = ttk.Button(master=self._frame, text="Lisää uusi meno", command=self._show_new_expense_view)
        btn_new_expense.grid(sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

        btn_new_income = ttk.Button(master=self._frame, text="Lisää uusi tulo", command=self._show_new_income_view)
        btn_new_income.grid(sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        label = tk.Label(master=self._frame, text="Tervetuloa!")

        self._initialize_transaction_list()

        self._initialize_buttons()

        #self._frame.grid_columnconfigure(1, weight=1, minsize=600)