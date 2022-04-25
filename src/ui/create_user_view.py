import tkinter as tk

from services.budget_service import budget_service

class CreateUserView:
    def __init__(self, root, handle_create_user, handle_show_login_view):
        self._root = root
        self._handle_create_user = handle_create_user
        self._handle_show_login_view = handle_show_login_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._confirm_password_entry = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=tk.X, ipadx=5, ipady=5)

    def destroy(self):
        self._frame.destroy()

    def _initialize_username_field(self):
        lbl_username = tk.Label(master=self._frame, text="Käyttäjätunnus")
        self._username_entry = tk.Entry(master=self._frame)

        lbl_username.grid(sticky=tk.constants.W)
        self._username_entry.grid(row=0, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_password_field(self):
        lbl_password = tk.Label(master=self._frame, text="Salasana")
        self._password_entry = tk.Entry(master=self._frame, show="\u2022")

        lbl_password.grid(sticky=tk.constants.W)
        self._password_entry.grid(row=1, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _initialize_confirm_password_field(self):
        lbl_confirm_password = tk.Label(master=self._frame, text="Vahvista salasana")
        self._confirm_password_entry = tk.Entry(master=self._frame, show="\u2022")

        lbl_confirm_password.grid(sticky=tk.constants.W)
        self._confirm_password_entry.grid(row=2, column=1, sticky=tk.constants.EW, padx=5, pady=5)

    def _handle_signing_up(self):
        username = self._username_entry.get()
        password1 = self._password_entry.get()
        password2 = self._confirm_password_entry.get()

        budget_service.create_user(username, password1, password2)

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._initialize_username_field()
        self._initialize_password_field()
        self._initialize_confirm_password_field()

        btn_sign_up = tk.Button(master=self._frame, text="Luo käyttäjätili", command=self._handle_signing_up)

        btn_sign_up.grid(columnspan=2, sticky=tk.constants.EW, padx=5, pady=5)

        frm_buttons = tk.Frame()
        frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

        self._frame.grid_columnconfigure(1, weight=1, minsize=300)