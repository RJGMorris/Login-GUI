# Login system using tkinter
# Includes a database with sqlite
# Includes an email validation using re

import tkinter
import sqlite3
import re

# Make a regular expression for validating an Email
regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

# Connect to sqlite database
connection = sqlite3.connect("login_data.db")
cursor = connection.cursor()


class LoginPage(object):

    def __init__(self, login_window):
        self.open = True
        self.PADDING = 5

        self.login_window = login_window
        self.login_window.title("Login")
        self.login_window["padx"] = self.PADDING
        self.login_window["pady"] = self.PADDING

        self.username_label = tkinter.Label(self.login_window, text="Username:")
        self.username = tkinter.Entry(self.login_window)
        self.password_label = tkinter.Label(self.login_window, text="Password:")
        self.password = tkinter.Entry(self.login_window, show="*")

        self.error_label_text = tkinter.StringVar()
        self.error_label = tkinter.Label(self.login_window, textvariable=self.error_label_text)

        self.create_account_page = None

    # Functions
    def hide(self):
        self.open = False
        self.login_window.withdraw()

    def show(self):
        self.login_window.update()
        self.login_window.deiconify()

    def open_create_account_page(self):
        self.hide()
        create_account_page = CreateAccountPage(self)
        self.create_account_page = create_account_page

    def login(self):
        cursor.execute("SELECT * FROM users WHERE username=:username", {'username': self.username.get()})
        combination = cursor.fetchone()
        if combination:
            if self.username.get() == combination[0] and self.password.get() == combination[1]:
                self.error_label_text.set("Login Successful")
            else:
                self.error_label_text.set("Incorrect username password combination")
        else:
            self.error_label_text.set("Username is invalid")

    def build_login_page(self):
        self.username_label.grid(row=0, column=0, sticky='nsw', columnspan=1)
        self.username.grid(row=0, column=1, sticky='nsew', columnspan=2)
        self.password_label.grid(row=1, column=0, sticky='nsw', columnspan=1)
        self.password.grid(row=1, column=1, sticky='nsew', columnspan=2)

        self.error_label.grid(row=5, column=1, sticky='nsew', columnspan=2)

        login_button = tkinter.Button(self.login_window, text="Login", width=15, command=self.login)
        login_button.grid(row=4, column=1, columnspan=1, sticky="news", pady=self.PADDING)

        create_account_button = tkinter.Button(self.login_window, text="Create New Account", width=16,
                                               command=self.open_create_account_page)
        create_account_button.grid(row=4, column=2, columnspan=1, sticky="news", pady=self.PADDING)


class CreateAccountPage(tkinter.Toplevel):

    def __init__(self, login_window):
        self.PADDING = 5

        self.login_window = login_window
        tkinter.Toplevel.__init__(self)
        self.title("Create an Account")
        self["padx"] = self.PADDING
        self["pady"] = self.PADDING

        self.username_label = tkinter.Label(self, text="Enter a Username:")
        self.username = tkinter.Entry(self)
        self.password_label = tkinter.Label(self, text="Enter a Password:")
        self.password = tkinter.Entry(self, show="*")
        self.password_label2 = tkinter.Label(self, text="Enter Password again:")
        self.password2 = tkinter.Entry(self, show="*")

        self.error_label_text = tkinter.StringVar()
        self.error_label = tkinter.Label(self, textvariable=self.error_label_text)

        self.build_create_account_page()

    # Functions
    def create_account(self):
        cursor.execute("SELECT * FROM users WHERE username=:username", {'username': '{}'.format(self.username.get())})
        if not cursor.fetchone():
            if re.search(regex, self.username.get()):
                if self.password.get() == self.password2.get():
                    cursor.execute("INSERT INTO users VALUES (:username, :password)",
                                   {'username': self.username.get(), 'password': self.password.get()})
                    connection.commit()
                    self.destroy()
                else:
                    self.error_label_text.set("Passwords do not match")
            else:
                self.error_label_text.set("Invalid Email")
        else:
            self.error_label_text.set("Email already exists")

    def build_create_account_page(self):
        self.username_label.grid(row=0, column=0, sticky='nsw', columnspan=1)
        self.username.grid(row=0, column=1, sticky='nsew', columnspan=2)
        self.password_label.grid(row=1, column=0, sticky='nsw', columnspan=1)
        self.password.grid(row=1, column=1, sticky='nsew', columnspan=2)
        self.password_label2.grid(row=2, column=0, sticky='nsew', columnspan=1)
        self.password2.grid(row=2, column=1, sticky='nsew', columnspan=2)

        create_account_button = tkinter.Button(self, text="Create Account", width=15, command=self.create_account)
        create_account_button.grid(row=3, column=1, columnspan=1, sticky="news", pady=self.PADDING)

        back_button = tkinter.Button(self, text="Back", width=15, command=lambda: self.destroy())
        back_button.grid(row=3, column=2, columnspan=1, sticky="news", pady=self.PADDING)

        self.error_label.grid(row=4, column=1, sticky='nsew', columnspan=2)


# Login window setup
RUN = True
Login_Window = tkinter.Tk()

# login window main loop call
if __name__ == "__main__":
    login_page = LoginPage(Login_Window)
    login_page.build_login_page()
    while RUN:
        login_page.login_window.update_idletasks()
        login_page.login_window.update()

        try:
            if not login_page.login_window.winfo_exists():
                RUN = False
        except tkinter.TclError:
            RUN = False

        if login_page.create_account_page:
            try:
                if not login_page.create_account_page.winfo_exists() and not login_page.open:
                    login_page.show()
                    login_page.open = True
            except tkinter.TclError:
                RUN = False

connection.close()
