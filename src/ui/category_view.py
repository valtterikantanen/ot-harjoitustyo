from datetime import datetime

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

from services.budget_service import budget_service

class CategoryView:
    def __init__(self, root, show_budget_view, show_add_category_view):
        self._root = root
        self._show_budget_view = show_budget_view
        self._show_add_category_view = show_add_category_view
        self._frame = None
        self._selected_category_id = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=tk.X, ipadx=5, ipady=5)

    def destroy(self):
        self._frame.destroy()

    def _initialize_category_list(self):
        categories = budget_service.get_categories(None)

        category_list = ttk.Treeview(self._frame)

        category_list["columns"] = ("id", "name", "type")

        def select_item(a):
            selected_item = category_list.focus()
            self._selected_category_id = category_list.item(selected_item)["values"][0]

        category_list.column("#0", width=0, stretch=tk.NO)
        category_list.column("id", anchor=tk.CENTER, width=50)
        category_list.column("name", anchor=tk.CENTER, width=250)
        category_list.column("type", anchor=tk.CENTER, width=75)

        category_list.heading("#0", text="", anchor=tk.CENTER)
        category_list.heading("id", text="ID", anchor=tk.CENTER)
        category_list.heading("name", text="Nimi", anchor=tk.CENTER)
        category_list.heading("type", text="Tyyppi", anchor=tk.CENTER)
        category_list.bind("<ButtonRelease-1>", select_item)

        for i in range(len(categories)):
            category_id = categories[i][0]
            name = categories[i][1]
            category_type = "Meno" if categories[i][2] == "expense" else "Tulo"
            category_list.insert(parent="", index="end", iid=i, text="", values=(category_id, name, category_type))

        category_list.grid(sticky=tk.constants.W, padx=5, pady=5)

        def delete():
            selected_item = category_list.selection()[0] if category_list.selection() else None
            if selected_item:
                budget_service.delete_category(self._selected_category_id)
                category_list.delete(selected_item)
            else:
                tkinter.messagebox.showerror(message="Valitse kategoria!")

        btn_delete_category = ttk.Button(master=self._frame, text="Poista kategoria", command=delete)
        btn_delete_category.grid(sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

        btn_add_category = ttk.Button(master=self._frame, text="Lisää kategoria", command=self._show_add_category_view)
        btn_add_category.grid(sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

        btn_show_main_view = ttk.Button(master=self._frame, text="Palaa päänäkymään", command=self._show_budget_view)
        btn_show_main_view.grid(sticky=tk.constants.EW, padx=10, pady=10, ipadx=10, ipady=10)

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._initialize_category_list()
