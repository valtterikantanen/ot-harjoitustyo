import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from services.budget_service import budget_service, AmountInWrongFormatError, TooBigNumberError

class AddTransactionView:
    def __init__(self, root, show_budget_view, category_type):
        self._root = root
        self._show_budget_view = show_budget_view
        self._category_type = category_type
        self._frame = None
        self._date_entry = None
        self._category_entry = None
        self._amount_entry = None
        self._description_entry = None
        self._error_label = None
        self._error_message = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=tk.X, ipadx=5, ipady=5)

    def destroy(self):
        self._frame.destroy()

    def _initialize_date_field(self):
        lbl_date = tk.Label(master=self._frame, text="Päivämäärä")
        self._date_entry = DateEntry(master=self._frame, locale="fi_FI", date_pattern="dd.mm.yyyy", width=30)

        lbl_date.grid(sticky=tk.constants.W)
        self._date_entry.grid(row=0, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_category_selection(self):
        categories_list = []
        for category in budget_service.get_categories(self._category_type):
            categories_list.append(category[1])

        def set_category(category_selection):
            self._category_entry = category_selection

        category_selection = tk.StringVar(self._frame)
        category_selection.set("Valitse kategoria...")

        lbl_category = tk.Label(master=self._frame, text="Kategoria")
        category_entry = tk.OptionMenu(self._frame, category_selection, *categories_list, command=set_category)

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

    def _initialize_buttons(self):
        btn_new_income = ttk.Button(master=self._frame, text="Lisää tapahtuma", command=self._handle_add_transaction)
        btn_new_income.grid(row=4, columnspan=2, sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

        btn_cancel = ttk.Button(master=self._frame, text="Peruuta", command=self._show_budget_view)
        btn_cancel.grid(row=5, columnspan=2, sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

    def _display_error(self, message):
        self._error_message.set(message)
        self._error_label.grid(columnspan=2, sticky=tk.constants.EW, padx=5, pady=5)

    def _hide_error(self):
        self._error_label.grid_remove()

    def _handle_add_transaction(self):
        date_entry = self._date_entry.get()
        date = f"{date_entry[6:]}-{date_entry[3:5]}-{date_entry[:2]}"
        category = self._category_entry
        amount = self._amount_entry.get()
        description = self._description_entry.get("1.0", "end-1c")

        if not self._category_entry:
            self._display_error("Valitse kategoria!")

        if len(description) > 500:
            self._display_error("Kuvauksen maksimipituus on 500 merkkiä.")

        try:
            if self._category_entry:
                budget_service.add_transaction(date, self._category_type, amount, category, description)
                self._show_budget_view()
        except AmountInWrongFormatError:
            self._display_error("Tarkista summa!\n• Desimaalierottimena voi käyttää pilkkua tai pistettä.\n• Kentässä ei voi olla kirjaimia eikä mm. miinus- tai €-merkkejä.\n• Älä käytä tuhaterottimia.")
        except TooBigNumberError:
            self._display_error("Liian suuri määrä!")

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._error_message = tk.StringVar(self._frame)

        self._error_label = tk.Label(master=self._frame, textvariable=self._error_message, foreground="red")

        self._initialize_date_field()
        self._initialize_category_selection()
        self._initalize_amount_field()
        self._initialize_description_field()
        self._initialize_buttons()

        self._hide_error()