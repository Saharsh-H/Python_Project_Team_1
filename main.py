import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter
import pymongo
from Windows.RegisterWindow import RegisterWindow
from PIL import Image, ImageTk
# from Classes.CarManager import CarManager
from Windows.MainWindow import MainWindow
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
mongo_path = "MONGO_PATH"
myclient = pymongo.MongoClient(mongo_path)
db = myclient["travel_manager"]
users_col = db["users"]
packages_col = db["packages"]
# car = CarManager("car1", 500, 20, "Ecity", "Majestic", "Swift", "Oraange")
d = {"_id":"car2", "price": 987600, "duration": 20, "source": "Ecty","destination": "Maestic","car_model": "Inova","rental_company": "VRL"}
# packages_col.find_one_and_update({"_id": "Cars"}, {"$push": {"cars": d}}, upsert=True)
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x550")
        self.title("FakeMyTrip | Where your journey begins... hypothetically")
        self.grid_columnconfigure(0, weight=1)

        self.logo_image = Image.open("Logo.webp")
        self.logo_image = self.logo_image.resize((300, 300))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = customtkinter.CTkLabel(self, image=self.logo_photo, text="")
        self.logo_label.grid(row=0, column=0, pady=(20, 10))

        self.login_entry1 = customtkinter.CTkEntry(self, placeholder_text="Enter your username", height=50, width=250)
        self.login_entry1.grid(row=2, column=0, padx=10, pady=10)

        self.login_entry2 = customtkinter.CTkEntry(self, placeholder_text="Enter your password", height=50, width=250,
                                                   show="*")
        self.login_entry2.grid(row=3, column=0, padx=10, pady=10)


        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=4, column=0, padx=10, pady=10)

        self.login_button = customtkinter.CTkButton(self.button_frame, text="Login", command=self.login_button_callback,
                                                    width=100)
        self.login_button.grid(row=0, column=0, padx=5, pady=5)

        self.register_button = customtkinter.CTkButton(self.button_frame, text="Register",
                                                       command=self.register_button_callback, width=100)
        self.register_button.grid(row=0, column=1, padx=5, pady=5)

        self.login_label = customtkinter.CTkLabel(self, text="", text_color="red")
        self.login_label.grid(row=1, column=0, padx=10, pady=10)

    def login_button_callback(self):
        users = users_col.find_one({"_id": self.login_entry1.get()})
        if users is not None:
            if self.login_entry2.get() == users["password"]:
                main_window = MainWindow(db, self, packages_col)
                main_window.withdraw()
            else:
                self.login_label.configure(text="Password is incorrect.")
                self.login_entry2.delete(0, "end")
        else:
            self.login_label.configure(text="Username not found.")

    def register_button_callback(self):
        window = RegisterWindow(users_col, self, db)
        window.open_register_window(db)



app = App()
app.mainloop()
