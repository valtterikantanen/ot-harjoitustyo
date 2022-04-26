import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from services.budget_service import budget_service

class AddExpenseView:
    def __init__(self, root, show_budget_view):
        self._root = root
        self._show_budget_view = show_budget_view
        self._frame = None
        self._date_entry = None
        self._category_entry = None
        self._amount_entry = None
        self._description_entry = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=tk.X, ipadx=5, ipady=5)

    def destroy(self):
        self._frame.destroy()

    def _initialize_date_field(self):
        lbl_date = tk.Label(master=self._frame, text="Päivämäärä")
        self._date_entry = DateEntry(master=self._frame, width=30, year=2022)

        lbl_date.grid(sticky=tk.constants.W)
        self._date_entry.grid(row=0, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_category_selection(self):
        categories_list = []
        for category in budget_service.get_categories("meno"):
            categories_list.append(category[1])

        def set_category(category_selection):
            self._category_entry = category_selection

        self._category_entry = tk.StringVar(self._frame)
        self._category_entry.set("Valitse kategoria...")

        lbl_category = tk.Label(master=self._frame, text="Kategoria")
        category_entry = tk.OptionMenu(self._frame, self._category_entry, *categories_list, command=set_category)

        lbl_category.grid(sticky=tk.constants.W)
        category_entry.grid(row=1, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initalize_amount_field(self):
        lbl_amount = tk.Label(master=self._frame, text="Määrä (€)")
        self._amount_entry = tk.Entry(master=self._frame)

        lbl_amount.grid(sticky=tk.constants.W)
        self._amount_entry.grid(row=2, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_description_field(self):
        lbl_description = tk.Label(master=self._frame, text="Kuvaus")
        self._description_entry = tk.Text(master=self._frame, height=5, width=50)

        lbl_description.grid(sticky=tk.constants.W)
        self._description_entry.grid(row=3, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_expense_button(self):
        btn_new_expense = ttk.Button(master=self._frame, text="Lisää meno", command=self._handle_add_expense)
        btn_new_expense.grid(row=4, columnspan=2, sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

    def _handle_add_expense(self):
        date = self._date_entry.get()
        category = self._category_entry
        amount = self._amount_entry.get()
        description = self._description_entry.get("1.0", "end-1c")

        if budget_service.add_transaction(date, "meno", amount, category, description):
            self._show_budget_view()


    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._initialize_date_field()
        self._initialize_category_selection()
        self._initalize_amount_field()
        self._initialize_description_field()
        self._initialize_expense_button()
        

        

        '''btn_login = tk.Button(master=self._frame, text="Kirjaudu sisään", command=self._handle_sign_in)
        btn_sign_up = tk.Button(master=self._frame, text="Luo uusi käyttäjätili", command=self._handle_display_create_user_view)

        btn_login.grid(columnspan=2, sticky=tk.constants.EW, padx=5, pady=5)

        btn_sign_up.grid(columnspan=2, sticky=tk.constants.EW, padx=5, pady=5)

        frm_buttons = tk.Frame()
        frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

        self._frame.grid_columnconfigure(1, weight=1, minsize=300)

        self.budget_service.add_transaction(
            date, income_or_expense, amount, category_id, description)'''