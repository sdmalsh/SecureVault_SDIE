from tkinter import *
from tkinter import filedialog, messagebox

from encryption import encrypt_folder, decrypt_folder

# =========================
# Open Main Program
# =========================

def open_main_program(on_logout=None):

    root = Tk()

    root.title("SecureVault SDIE")

    root.geometry("600x450")

    root.configure(bg="#1e1e1e")

    root.resizable(False, False)

    selected_path = ""

    # =========================
    # Select Folder
    # =========================

    def select_folder():

        nonlocal selected_path

        selected_path = filedialog.askdirectory()

        if selected_path:

            status_label.config(
                text=selected_path,
                fg="cyan"
            )

    # =========================
    # Encrypt
    # =========================

    def start_encryption():

        nonlocal selected_path

        if selected_path == "":

            messagebox.showerror(
                "Error",
                "Please Select Folder"
            )

            return

        try:
            encrypted_count = encrypt_folder(selected_path)

            status_label.config(
                text=f"{encrypted_count} Files Encrypted",
                fg="#2ecc71"
            )
            
            messagebox.showinfo(
                "Success",
                f"Encrypted {encrypted_count} files successfully"
            )

        except Exception as e:
            messagebox.showerror(
                "Encryption Error",
                f"Error during encryption: {str(e)}"
            )

    # =========================
    # Decrypt
    # =========================

    def start_decryption():

        nonlocal selected_path

        if selected_path == "":

            messagebox.showerror(
                "Error",
                "Please Select Folder"
            )

            return

        try:
            decrypted_count = decrypt_folder(selected_path)

            status_label.config(
                text=f"{decrypted_count} Files Decrypted",
                fg="#f1c40f"
            )
            
            messagebox.showinfo(
                "Success",
                f"Decrypted {decrypted_count} files successfully"
            )

        except Exception as e:
            messagebox.showerror(
                "Decryption Error",
                f"Error during decryption: {str(e)}"
            )

    def logout():

        root.destroy()

        if callable(on_logout):
            on_logout()

    # =========================
    # Title
    # =========================

    Label(
        root,
        text="SecureVault SDIE",
        font=("Arial", 24, "bold"),
        bg="#1e1e1e",
        fg="cyan"
    ).pack(pady=20)

    # =========================
    # Buttons
    # =========================

    Button(
        root,
        text="Select Folder",
        command=select_folder,
        width=25,
        height=2,
        bg="#2c3e50",
        fg="white"
    ).pack(pady=10)

    Button(
        root,
        text="Encrypt Folder",
        command=start_encryption,
        width=25,
        height=2,
        bg="#27ae60",
        fg="white"
    ).pack(pady=10)

    Button(
        root,
        text="Decrypt Folder",
        command=start_decryption,
        width=25,
        height=2,
        bg="#f39c12",
        fg="white"
    ).pack(pady=10)

    Button(
        root,
        text="Logout",
        command=logout,
        width=25,
        height=2,
        bg="#3498db",
        fg="white"
    ).pack(pady=10)

    Button(
        root,
        text="Exit",
        command=root.destroy,
        width=25,
        height=2,
        bg="#c0392b",
        fg="white"
    ).pack(pady=10)

    # =========================
    # Status
    # =========================

    status_label = Label(
        root,
        text="No Folder Selected",
        font=("Arial", 12),
        bg="#1e1e1e",
        fg="white"
    )

    status_label.pack(pady=20)

    root.mainloop()