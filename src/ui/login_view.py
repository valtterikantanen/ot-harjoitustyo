import tkinter as tk

from services.user_service import user_service, UserNotFoundError, WrongPasswordError

class LoginView:
    def __init__(self, root, handle_login, handle_display_create_user_view):
        self._root = root
        self._handle_login = handle_login
        self._handle_display_create_user_view = handle_display_create_user_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._error_label = None
        self._error_message = None

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

    def _display_error(self, message):
        self._error_message.set(message)
        self._error_label.grid(columnspan=2, sticky=tk.constants.EW, padx=5, pady=5)

    def _hide_error(self):
        self._error_label.grid_remove()

    def _handle_sign_in(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        try:
            user_service.login(username, password)
            self._handle_login()
        except WrongPasswordError:
            self._display_error("Väärä salasana.")
        except UserNotFoundError:
            self._display_error(f"Käyttäjää {username} ei löytynyt.")

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._error_message = tk.StringVar(self._frame)

        self._error_label = tk.Label(master=self._frame, textvariable=self._error_message, foreground="red")

        self._initialize_username_field()
        self._initialize_password_field()

        btn_login = tk.Button(master=self._frame, text="Kirjaudu sisään", command=self._handle_sign_in)
        btn_login.grid(columnspan=2, sticky=tk.constants.EW, padx=10, pady=5, ipadx=5, ipady=5)

        btn_sign_up = tk.Button(master=self._frame, text="Luo uusi käyttäjätili", command=self._handle_display_create_user_view)
        btn_sign_up.grid(columnspan=2, sticky=tk.constants.EW, padx=10, pady=5, ipadx=5, ipady=5)

        frm_buttons = tk.Frame()
        frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

        self._frame.grid_columnconfigure(1, weight=1, minsize=300)

        self._hide_error()