import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter
from Classes.UserManager import UserManager
from PIL import Image, ImageTk
from tkinter import ttk

class MainWindow(customtkinter.CTk):
    def __init__(self, db, parent, packages_col):
        super().__init__()

        self.db = db
        self.parent = parent
        self.package_col = packages_col
        parent.withdraw()
        self.current_page = 1

        main_window = customtkinter.CTkToplevel(self)
        main_window.lift()
        main_window.title("FakeMyTrip | Where your journey begins... hypothetically")
        main_window.geometry("800x600")
        main_window.grid_columnconfigure(0, weight=1)
        main_window.grid_rowconfigure(0, weight=0)
        main_window.grid_rowconfigure(1, weight=1)
        self.main_window = main_window
        self.header_frame = customtkinter.CTkFrame(main_window, height=50, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=0)  # Logout Button
        self.header_frame.grid_columnconfigure(2, weight=0)  # View Cart Button        

        self.duration = customtkinter.CTkLabel(
            self.header_frame,
            text="Duration",
            width=100,
        )
        self.duration.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        self.cart_button = customtkinter.CTkButton(
            self.header_frame,
            text="View Cart",
            command=self.view_cart,
            width=100,
        )
        self.cart_button.grid(row=0, column=3, padx=10, pady=5, sticky="ne")

        main_window.tab_view = customtkinter.CTkTabview(main_window)
        main_window.tab_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_window.tab_view.columnconfigure(0, weight=1)

        main_window.tab_view.add("Cars")
        main_window.tab_view.add("Flights")
        main_window.tab_view.add("Hotels")
        main_window.tab_view.set("Cars")

        self.add_tab_content(main_window.tab_view.tab("Cars"), "Cars", self.search_cars)
        self.add_tab_content(main_window.tab_view.tab("Flights"), "Flights", self.search_flights)
        self.add_hotels_tab_content(main_window.tab_view.tab("Hotels"))

        for tab_name in ["Cars", "Flights", "Hotels"]:
            tab = main_window.tab_view.tab(tab_name)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(2, weight=1)

    def add_tab_content(self, tab, tab_type, callback):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=0)

        logout_button = customtkinter.CTkButton(
            tab,
            text="Logout",
            command=self.logout,
            width=100,
            fg_color="red",  
            hover_color="darkred", 
        )
        logout_button.grid(row=0, column=1, padx=10, pady=(0, 0), sticky="ne")

        source_entry = customtkinter.CTkEntry(
            tab, placeholder_text=f"{tab_type} Source", height=50, width=250
        )
        source_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        destination_entry = customtkinter.CTkEntry(
            tab, placeholder_text=f"{tab_type} Destination", height=50, width=250
        )
        destination_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))

        date_entry = customtkinter.CTkEntry(
            tab, placeholder_text=f"Travel Date (DD-MM-YYYY)", height=50, width=250
        )
        date_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))

        search_button = customtkinter.CTkButton(tab, text=f"Search {tab_type}", command=callback)
        search_button.grid(row=3, column=0, padx=10, pady=10)

        self.view_packages_button = customtkinter.CTkButton(tab,text = "View Packages",command = self.view_packages)
        self.view_packages_button.grid(row = 3,column = 1,padx = 10,pady = (0,0))

    def add_hotels_tab_content(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=0)
        logout_button = customtkinter.CTkButton(
            tab,
            text="Logout",
            command=self.logout,
            width=100,
            fg_color="red",  
            hover_color="darkred",  
        )
        logout_button.grid(row=0, column=1, padx=10, pady=(0, 0), sticky="ne")
        location_entry = customtkinter.CTkEntry(
            tab, placeholder_text="Enter Location", height=50, width=250
        )
        location_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        date_entry = customtkinter.CTkEntry(
            tab, placeholder_text="Enter Check-in Date (DD-MM-YYYY)", height=50, width=250
        )
        date_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))

        search_button = customtkinter.CTkButton(
            tab, text="Search Hotels", command=self.search_hotels
        )
        search_button.grid(row=2, column=0, padx=10, pady=10)

        self.view_packages_button = customtkinter.CTkButton(tab,text = "View Packages",command = self.view_packages)
        self.view_packages_button.grid(row = 3,column = 1 ,padx = 10,pady = (0,0))

    def search_cars(self):

        cars_tab = self.main_window.tab_view.tab("Cars")

        if hasattr(self, "results_frame") and self.results_frame.winfo_exists():
            self.results_frame.destroy()

        car_data = self.package_col.find_one({"_id": "Cars"})
        if not car_data or "cars" not in car_data:
            print("No car data found!")
            return

        self.results_frame = customtkinter.CTkFrame(cars_tab, corner_radius=10)
        self.results_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=3)
        self.results_frame.grid_columnconfigure(1, weight=1)

        description = customtkinter.CTkLabel(
            self.results_frame,
            text = "Description",
            anchor="w", 
            justify="left",
            font = ("Roboto", 20, "bold")
        )
        description.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        Add_1_Day = customtkinter.CTkLabel(
            self.results_frame,
            text = "Add 1 Day",
            anchor="e", 
            justify="right",
            font = ("Roboto", 20, "bold")
        )
        Add_1_Day.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        Delete_1_Day = customtkinter.CTkLabel(
            self.results_frame,
            text = "Delete 1 Day",
            anchor="e", 
            justify="right",
            font = ("Roboto", 20, "bold")
        )
        Delete_1_Day.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        Total_Duration = customtkinter.CTkLabel(
            self.results_frame,
            text = "Total Duration",
            anchor="e", 
            justify="right",
            font = ("Roboto", 20, "bold")
        )
        Total_Duration.grid(row=0, column=4, padx=10, pady=5, sticky="w")

        for index, car in enumerate(car_data["cars"]):
            print(f"{index}: {car}")
            car_details = (
                f"Model: {car['car_model']}\n"
                f"Price: {car['price']} rupees/day\n"
                f"Rental Company: {car['rental_company']}\n"
                f"Duration: {car['duration']} days\n"
            )
            car_label = customtkinter.CTkLabel(
                self.results_frame, text=car_details, anchor="w", justify="left"
            )
            car_label.grid(row = index + 1, column=0, padx=10, pady=5, sticky="w")

            add_to_pkg_button = customtkinter.CTkButton(
                self.results_frame,
                text="Add to Your Package",
                command=lambda c=car: self.add_to_pkg(c),
            )
            add_to_pkg_button.grid(row = index + 1, column=1, padx=10, pady=5)

            book_button = customtkinter.CTkButton(
                self.results_frame,
                text="Add",
                command=lambda c=car: self.book_car(c),
            )
            book_button.grid(row = index + 1, column=2, padx=10, pady=5)

            delete_button = customtkinter.CTkButton(
                self.results_frame,
                text="Delete",
                command=lambda c=car: self.delete_car(c),
            )
            delete_button.grid(row = index + 1, column=3, padx=10, pady=5)

            Duration = customtkinter.CTkLabel(
            self.results_frame,
            text = "0" + " Days",
            anchor="e", 
            justify="right",
            font = ("Roboto", 20, "bold")
            )
            Duration.grid(row = index + 1, column=4, padx=10, pady=5, sticky="w")

    def book_car(self, car):
        print(f"Booking car: {car['car_model']} from {car['rental_company']} at {car['price']} rupees/day")

    def add_to_pkg(self, car):
        print("Added to your package")

    def delete_car(self, car):
        print(f"Deleting car: {car['car_model']} from {car['rental_company']} at {car['price']} rupees/day")

    def search_flights(self):
        print("Search button clicked for Flights!")

    def search_hotels(self):
        print("Search button clicked for Hotels!")

    def logout(self):
        print("Logout clicked!")
        self.parent.deiconify()
        self.destroy()

    def populate_tab(self, tab, data, headers):
        # Create Treeview for the data
        tree = ttk.Treeview(tab, columns=headers, show="headings", height=10)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Add Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Set the column headers
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor="center")

        # Add rows to the Treeview
        for record in data:
            tree.insert("", "end", values=tuple(record.values()))

    def view_packages(self):
        view_pckg = ViewPackage

    def view_cart(self):
        print("View Cart clicked!")