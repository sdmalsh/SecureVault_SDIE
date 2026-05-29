import customtkinter as ctk
from tkinter import PhotoImage, messagebox
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

import database
from assets.gui import open_main_program


class SecurityLoginApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("SecureVault SDIE Login")

        self.geometry("700x500")

        self.resizable(False, False)

        self.configure(fg_color="#16181d")

        # =========================
        # Title
        # =========================

        title_label = ctk.CTkLabel(
            self,
            text="SecureVault SDIE",
            font=("Arial", 28, "bold"),
            text_color="cyan"
        )

        title_label.pack(pady=40)

        # =========================
        # Username
        # =========================

        self.username_input = ctk.CTkEntry(
            self,
            width=300,
            height=40,
            placeholder_text="Username"
        )

        self.username_input.pack(pady=15)

        # =========================
        # Password
        # =========================

        self.password_input = ctk.CTkEntry(
            self,
            width=300,
            height=40,
            placeholder_text="Password",
            show="*"
        )

        self.password_input.pack(pady=15)

        # =========================
        # Login Button
        # =========================

        login_btn = ctk.CTkButton(
            self,
            text="Secure Login",
            width=300,
            height=45,
            command=self.login_action
        )

        login_btn.pack(pady=30)
        # هنا تضع كل عناصر الواجهة
        # Labels
        # Entries
        # Buttons

            # =========================
    # Login Action
    # =========================

    def login_action(self):

        username = self.username_input.get().strip()

        password = self.password_input.get()

        user = database.check_login(username, password)

        if user:

            messagebox.showinfo(
                "Success",
                "Login Successful"
            )

            self.destroy()

            open_main_program()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Username or Password"
            )
            # =========================
# Start Login System
# =========================

def start_login():

    database.create_database()

    app = SecurityLoginApp()

    app.mainloop()