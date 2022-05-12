import tkinter as tk
from tkinter import ttk

from services.category_service import category_service
from services.user_service import user_service

class AddCategoryView:
    def __init__(self, root, show_category_view):
        self._root = root
        self._show_category_view = show_category_view
        self._frame = None
        self._name_entry = None
        self._type_entry = None
        self._error_label = None
        self._error_message = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=tk.X, ipadx=5, ipady=5)

    def destroy(self):
        self._frame.destroy()

    def _initialize_name_field(self):
        lbl_name = tk.Label(master=self._frame, text="Nimi")
        self._name_entry = tk.Entry(master=self._frame)

        lbl_name.grid(sticky=tk.constants.W)
        self._name_entry.grid(row=0, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_type_selection(self):
        type_list = ["Meno", "Tulo"]

        def set_type(type_selection):
            self._type_entry = type_selection

        type_selection = tk.StringVar(self._frame)
        type_selection.set("Valitse tyyppi...")

        lbl_type = tk.Label(master=self._frame, text="Tyyppi")
        type_entry = tk.OptionMenu(self._frame, type_selection, *type_list, command=set_type)

        lbl_type.grid(sticky=tk.constants.W)
        type_entry.grid(row=1, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_buttons(self):
        btn_new_income = ttk.Button(master=self._frame, text="Lisää kategoria", command=self._handle_add_category)
        btn_new_income.grid(row=2, columnspan=2, sticky=tk.constants.EW, padx=10, pady=5, ipadx=5, ipady=5)

        btn_cancel = ttk.Button(master=self._frame, text="Peruuta", command=self._show_category_view)
        btn_cancel.grid(row=3, columnspan=2, sticky=tk.constants.EW, padx=10, pady=5, ipadx=5, ipady=5)

    def _display_error(self, message):
        self._error_message.set(message)
        self._error_label.grid(columnspan=2, sticky=tk.constants.EW, padx=5, pady=5)

    def _hide_error(self):
        self._error_label.grid_remove()

    def _handle_add_category(self):
        name = self._name_entry.get().strip()
        user_id = user_service.get_current_user_id()

        if len(name) == 0:
            self._display_error("Syötä kategorian nimi!")

        if not self._type_entry:
            self._display_error("Valitse kategoria!")
        elif self._type_entry == "Meno":
            category_type = "expense"
        elif self._type_entry == "Tulo":
            category_type = "income"

        if self._type_entry and len(name) > 0:
            category_service.add(name, category_type, user_id)
            self._show_category_view()

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._error_message = tk.StringVar(self._frame)

        self._error_label = tk.Label(master=self._frame, textvariable=self._error_message, foreground="red")

        self._initialize_name_field()
        self._initialize_type_selection()
        self._initialize_buttons()