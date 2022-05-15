import tkinter as tk

from services.user_service import user_service, PasswordsDontMatchError, UsernameAlreadyExistsError, InvalidUsernameOrPasswordError
from services.category_service import category_service

class CreateUserView:
    """Uuden käyttäjätilin luomisesta vastaava näkymä."""

    def __init__(self, root, show_budget_view, show_login_view):
        """Luokan konstruktori.
        
        Args:
            root:
                tkinterin juurielementti, jonka sisään näkymä alustetaan.
            show_budget_view:
                Arvo, jota kutsutaan, jos käyttäjätunnuksen luonti on onnistunut.
                Siirtää käyttäjän sovelluksen päänäkymään.
            show_login_view:
                Arvo, jota kutsutaan, kun siirrytään (takaisin) kirjautumisnäkymään.
        """

        self._root = root
        self._show_budget_view = show_budget_view
        self._show_login_view = show_login_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._confirm_password_entry = None
        self._error_label = None
        self._error_message = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän."""

        self._frame.pack(fill=tk.X, ipadx=5, ipady=5)

    def destroy(self):
        """Piilottaa näkymän."""

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

    def _display_error(self, message):
        self._error_message.set(message)
        self._error_label.grid(columnspan=2, sticky=tk.constants.EW, padx=5, pady=5)

    def _hide_error(self):
        self._error_label.grid_remove()

    def _handle_signing_up(self):
        username = self._username_entry.get()
        password1 = self._password_entry.get()
        password2 = self._confirm_password_entry.get()

        try:
            user_id = user_service.create(username, password1, password2)
            category_service.add_default_categories(user_id)
            user_service.login(username, password1)
            self._show_budget_view()
        except PasswordsDontMatchError:
            self._display_error("Salasanat eivät täsmää!")
        except UsernameAlreadyExistsError:
            self._display_error(f"Käyttäjätunnus {username} on jo käytössä!")
        except InvalidUsernameOrPasswordError:
            self._display_error("Anna käyttäjätunnus ja salasana!")

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._error_message = tk.StringVar(self._frame)

        self._error_label = tk.Label(master=self._frame, textvariable=self._error_message, foreground="red")

        self._initialize_username_field()
        self._initialize_password_field()
        self._initialize_confirm_password_field()

        btn_sign_up = tk.Button(master=self._frame, text="Luo käyttäjätili", command=self._handle_signing_up)
        btn_sign_up.grid(columnspan=2, sticky=tk.constants.EW, padx=10, pady=5, ipadx=5, ipady=5)

        btn_cancel = tk.Button(master=self._frame, text="Peruuta", command=self._show_login_view)
        btn_cancel.grid(columnspan=2, sticky=tk.constants.EW, padx=10, pady=5, ipadx=5, ipady=5)

        frm_buttons = tk.Frame()
        frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

        self._frame.grid_columnconfigure(1, weight=1, minsize=300)

        self._hide_error()