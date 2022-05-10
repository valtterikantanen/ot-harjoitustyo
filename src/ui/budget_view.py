from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

from services.transaction_service import transaction_service
from services.user_service import user_service

class BudgetView:
    def __init__(self, root, show_login_view, show_add_transaction_view, show_category_view, show_edit_transaction_view):
        self._root = root
        self._show_login_view = show_login_view
        self._show_add_transaction_view = show_add_transaction_view
        self._show_category_view = show_category_view
        self._show_edit_transaction_view = show_edit_transaction_view
        self._selected_transaction_id = None
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=tk.X, ipadx=5, ipady=5)

    def destroy(self):
        self._frame.destroy()

    def _initialize_username_label(self):
        username = user_service.user.username
        lbl_username = tk.Label(master=self._frame, text=f"Käyttäjätunnus: {username}")
        lbl_username.grid(row=0, columnspan=2, sticky=tk.constants.EW)

    def _initialize_transaction_list(self):
        transactions = transaction_service.get_all()

        transaction_list = ttk.Treeview(self._frame)

        transaction_list["columns"] = ("id", "date", "amount", "category", "description")

        def select_item(a):
            selected_item = transaction_list.focus()
            if selected_item:
                self._selected_transaction_id = transaction_list.item(selected_item)["values"][0]

        transaction_list.column("#0", width=0, stretch=tk.NO)
        transaction_list.column("id", width=0, stretch=tk.NO)
        transaction_list.column("date", anchor=tk.W, width=95)
        transaction_list.column("amount", anchor=tk.E, width=120)
        transaction_list.column("category", anchor=tk.E, width=180)
        transaction_list.column("description", anchor=tk.W, width=400)

        transaction_list.heading("#0", text="", anchor=tk.CENTER)
        transaction_list.heading("id", text="", anchor=tk.CENTER)
        transaction_list.heading("date", text="Päivämäärä", anchor=tk.CENTER)
        transaction_list.heading("amount", text="Summa", anchor=tk.CENTER)
        transaction_list.heading("category", text="Kategoria", anchor=tk.CENTER)
        transaction_list.heading("description", text="Kuvaus", anchor=tk.CENTER)

        transaction_list.bind("<ButtonRelease-1>", select_item)

        scrollbar = ttk.Scrollbar(self._frame, orient=tk.VERTICAL, command=transaction_list.yview)
        transaction_list.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky=tk.constants.NSEW)

        for i in range(len(transactions)):
            transaction_id = transactions[i][0]
            datetime_object = datetime.strptime(transactions[i][1], "%Y-%m-%d")
            date = datetime.strftime(datetime_object, "%-d.%-m.%Y")
            amount = f"{('%.2f' % (transactions[i][2] / 100)).replace('.', ',').replace('-', '−')} €"
            category = transactions[i][3]
            description = transactions[i][4]
            tag = "red" if amount[0] == "−" else "green"
            transaction_list.insert(parent="", index="end", iid=i, text="", values=(transaction_id, date, amount, category, description), tags=tag)

        transaction_list.grid(row=1, column=0, sticky=tk.constants.NSEW, padx=5, pady=5)
        transaction_list.tag_configure("red", foreground="red")
        transaction_list.tag_configure("green", foreground="green")

        def delete():
            selected_item = transaction_list.selection()[0] if transaction_list.selection() else None
            if selected_item:
                answer = messagebox.askyesno(message="Haluatko varmasti poistaa tapahtuman?", icon="warning")
                if answer:
                    transaction_service.delete(self._selected_transaction_id)
                    transaction_list.delete(selected_item)
            else:
                messagebox.showerror(message="Valitse poistettava tapahtuma!")

        def edit():
            selected_item = transaction_list.selection()[0] if transaction_list.selection() else None
            if selected_item:
                self._show_edit_transaction_view(self._selected_transaction_id)
            else:
                messagebox.showerror(message="Valitse muokattava tapahtuma!")

        btn_edit_transaction = ttk.Button(master=self._frame, text="Muokkaa tapahtumaa", command=edit)
        btn_edit_transaction.grid(row=4, columnspan=2, sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)
        
        btn_delete_transaction = ttk.Button(master=self._frame, text="Poista tapahtuma", command=delete)
        btn_delete_transaction.grid(row=5, columnspan=2, sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

    def _handle_log_out(self):
        user_service.logout()
        self._show_login_view()

    def _handle_show_new_expense_view(self):
        self._show_add_transaction_view("expense")

    def _handle_show_new_income_view(self):
        self._show_add_transaction_view("income")

    def _initialize_buttons(self):
        btn_new_expense = ttk.Button(master=self._frame, text="Lisää uusi meno", command=self._handle_show_new_expense_view)
        btn_new_expense.grid(row=2, columnspan=2, sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

        btn_new_income = ttk.Button(master=self._frame, text="Lisää uusi tulo", command=self._handle_show_new_income_view)
        btn_new_income.grid(row=3, columnspan=2, sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

        btn_show_categories = ttk.Button(master=self._frame, text="Tarkastele kategorioita", command=self._show_category_view)
        btn_show_categories.grid(columnspan=2, sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

        btn_log_out = ttk.Button(master=self._frame, text="Kirjaudu ulos", command=self._handle_log_out)
        btn_log_out.grid(columnspan=2, sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._initialize_username_label()
        self._initialize_transaction_list()
        self._initialize_buttons()
