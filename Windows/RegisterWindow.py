import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter
from Classes.UserManager import UserManager
from Windows.MainWindow import MainWindow
class RegisterWindow(customtkinter.CTk):
    def __init__(self, users_col, parent, db):
        super().__init__()
        self.users_col = users_col
        self.parent = parent
    def open_register_window(self, db):

        register_window = customtkinter.CTkToplevel(self)
        register_window.lift()
        register_window.geometry("400x300")
        register_window.title("Register")

        register_window.grid_columnconfigure(0, weight=1)
        header_frame = customtkinter.CTkFrame(register_window, height=50, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        back_button = customtkinter.CTkButton(
            header_frame,
            text="Back to Login",
            command=register_window.destroy,
            width=100,
            fg_color="red",
            hover_color="darkred",
        )
        back_button.grid(row=0, column=1, padx=10, pady=5, sticky="e")        
        register_label = customtkinter.CTkLabel(register_window, text="Register a New Account", font=("Arial", 16))
        register_label.grid(row=0, column=0, pady=(20, 10))

        username_entry = customtkinter.CTkEntry(register_window, placeholder_text="Enter new username", height=50,
                                                width=250)
        username_entry.grid(row=1, column=0, padx=10, pady=10)

        password_entry = customtkinter.CTkEntry(register_window, placeholder_text="Enter new password", height=50,
                                                width=250, show="*")
        password_entry.grid(row=2, column=0, padx=10, pady=10)

        status_label = customtkinter.CTkLabel(register_window, text="", text_color="red")
        status_label.grid(row=3, column=0, padx=10, pady=10)

        def register_user():
            username = username_entry.get()
            password = password_entry.get()

            if username and password:
                if self.users_col.find_one({"_id": username}):
                    status_label.configure(text="Username already exists.")
                else:
                    user = UserManager(username, password)
                    try:
                        self.users_col.insert_one(user.__dict__)
                        status_label.configure(text="Registration successful!", text_color="green")
                        register_window.destroy()
                    except Exception as e:
                        print(e)
                        status_label.configure(text="Registration failed.", text_color="red")
            else:
                status_label.configure(text="Please fill in all fields.")

        register_button = customtkinter.CTkButton(register_window, text="Register", command=register_user, width=100)
        register_button.grid(row=4, column=0, padx=10, pady=10)
