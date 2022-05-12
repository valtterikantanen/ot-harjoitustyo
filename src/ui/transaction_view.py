import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from services.transaction_service import transaction_service, AmountInWrongFormatError, TooBigNumberError, DateInWrongFormatError
from services.category_service import category_service
from services.user_service import user_service

class TransactionView:
    def __init__(self, root, show_budget_view, category_type, transaction_id, editing):
        self._root = root
        self._show_budget_view = show_budget_view
        self._category_type = category_type
        self._transaction_id = transaction_id
        self._editing = editing
        self._frame = None
        self._transaction = None
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

        if self._editing:
            date = self._transaction[0]
            self._date_entry = DateEntry(master=self._frame, locale="fi_FI", date_pattern="dd.mm.yyyy", width=30, year=int(date[:4]), month=int(date[5:7]), day=int(date[8:]))
        else:
            self._date_entry = DateEntry(master=self._frame, locale="fi_FI", date_pattern="dd.mm.yyyy", width=30)

        lbl_date.grid(sticky=tk.constants.W)
        self._date_entry.grid(row=0, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_category_selection(self):
        if self._editing:
            self._category_entry = self._transaction[2]

        categories_list = []
        user_id = user_service.get_current_user_id()

        for category in category_service.get_all(user_id, self._category_type):
            categories_list.append(category[1])

        def set_category(category_selection):
            self._category_entry = category_selection

        category_selection = tk.StringVar(self._frame)
        if self._editing:
            category_selection.set(self._category_entry)
        else:
            category_selection.set("Valitse kategoria...")

        lbl_category = tk.Label(master=self._frame, text="Kategoria")
        category_entry = tk.OptionMenu(self._frame, category_selection, *categories_list, command=set_category)

        lbl_category.grid(sticky=tk.constants.W)
        category_entry.grid(row=1, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_amount_field(self):
        if self._editing:
            str_amount = f"{('%.2f' % abs(self._transaction[1] / 100)).replace('.', ',')}"
        else:
            str_amount = ""
        
        amount = tk.StringVar(self._root, value=str_amount)
        lbl_amount = tk.Label(master=self._frame, text="Määrä (€)")
        self._amount_entry = tk.Entry(master=self._frame, textvariable=amount)

        lbl_amount.grid(sticky=tk.constants.W)
        self._amount_entry.grid(row=2, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_description_field(self):
        lbl_description = tk.Label(master=self._frame, text="Kuvaus")
        self._description_entry = tk.Text(master=self._frame, height=2, width=50)

        if self._editing:
            self._description_entry.insert(tk.INSERT, self._transaction[3])

        lbl_description.grid(sticky=tk.constants.W)
        self._description_entry.grid(row=3, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_buttons(self):
        add_or_update = "Päivitä tiedot" if self._editing else "Lisää tapahtuma"

        btn_new_expense = ttk.Button(master=self._frame, text=add_or_update, command=self._handle_edit_transaction)
        btn_new_expense.grid(row=4, columnspan=2, sticky=tk.constants.EW, padx=10, pady=5, ipadx=5, ipady=5)

        btn_cancel = ttk.Button(master=self._frame, text="Peruuta", command=self._show_budget_view)
        btn_cancel.grid(row=5, columnspan=2, sticky=tk.constants.EW, padx=10, pady=5, ipadx=5, ipady=5)

    def _display_error(self, message):
        self._error_message.set(message)
        self._error_label.grid(columnspan=2, sticky=tk.constants.EW, padx=5, pady=5)

    def _hide_error(self):
        self._error_label.grid_remove()

    def _handle_edit_transaction(self):
        date = self._date_entry.get()
        category_id = category_service.get_category_id(self._category_entry, self._category_type)
        amount = self._amount_entry.get()
        description = self._description_entry.get("1.0", "end-1c")
        user_id = user_service.get_current_user_id()

        if not self._category_entry:
            self._display_error("Valitse kategoria!")

        if len(description) > 50:
            self._display_error("Kuvauksen maksimipituus on 50 merkkiä.")

        try:
            if len(description) <= 50:
                if self._editing:
                    transaction_service.update(self._transaction_id, date, self._category_type, amount, category_id, description)
                    messagebox.showinfo(message="Tiedot päivitetty!")
                else:
                    transaction_service.create(date, self._category_type, amount, category_id, user_id, description)
                    messagebox.showinfo(message="Tapahtuma lisätty")
                self._show_budget_view()
        except AmountInWrongFormatError:
            self._display_error("Tarkista summa!\n• Desimaalierottimena voi käyttää pilkkua tai pistettä.\n• Kentässä ei voi olla kirjaimia eikä mm. miinus- tai €-merkkejä.\n• Älä käytä tuhaterottimia.")
        except TooBigNumberError:
            self._display_error("Määrän on oltava välillä 0...9 999 999,99 €.")
        except DateInWrongFormatError:
            self._display_error("Syötä päivämäärä muodossa '01.01.2020'.")

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._transaction = transaction_service.get_one(self._transaction_id)
        
        self._error_message = tk.StringVar(self._frame)

        self._error_label = tk.Label(master=self._frame, textvariable=self._error_message, foreground="red")

        self._initialize_date_field()
        self._initialize_category_selection()
        self._initialize_amount_field()
        self._initialize_description_field()
        self._initialize_buttons()

        self._hide_error()