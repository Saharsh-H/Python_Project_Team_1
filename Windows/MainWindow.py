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

        main_window = customtkinter.CTkToplevel(self)
        main_window.lift()
        main_window.title("FakeMyTrip | Where your journey begins... hypothetically")
        main_window.geometry("800x600")
        main_window.grid_columnconfigure(0, weight=1)
        main_window.grid_rowconfigure(0, weight=0)
        main_window.grid_rowconfigure(1, weight=1)
        self.main_window = main_window
        self.header_frame = customtkinter.CTkFrame(main_window, height=50, corner_radius=0)
        self.header_frame.grid_columnconfigure(1, weight=0)  # Logout Button
        self.header_frame.grid_columnconfigure(2, weight=0)  # View Cart Button
        self.logout_button = customtkinter.CTkButton(
            self.header_frame,
            text="Logout",
            command=self.logout,
            width=100,
            fg_color="red",
            hover_color="darkred",
        )
        self.logout_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")
        self.cart_button = customtkinter.CTkButton(
            self.header_frame,
            text="View Cart",
            command=self.view_cart,
            width=100,
        )
        self.cart_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

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
            car_label.grid(row=index, column=0, padx=10, pady=5, sticky="w")

            book_button = customtkinter.CTkButton(
                self.results_frame,
                text="Book Now",
                command=lambda c=car: self.book_car(c),
            )
            book_button.grid(row=index, column=1, padx=10, pady=5)

    def book_car(self, car):
        print(f"Booking car: {car['car_model']} from {car['rental_company']} at {car['price']} rupees/day")

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
        # Placeholder Data
        car_data = [
            {"Model": "Toyota Corolla", "Price": 500, "Rental Company": "Hertz", "Duration": 7},
            {"Model": "Honda Civic", "Price": 450, "Rental Company": "Avis", "Duration": 5},
            {"Model": "Ford Mustang", "Price": 700, "Rental Company": "Enterprise", "Duration": 3},
        ] * 3  # Tripled for demo

        flight_data = [
            {"Flight No": "AI101", "Price": 1200, "Source": "NYC", "Destination": "LAX", "Date": "2024-12-10"},
            {"Flight No": "BA205", "Price": 900, "Source": "LAX", "Destination": "London", "Date": "2024-12-12"},
            {"Flight No": "DL300", "Price": 950, "Source": "Atlanta", "Destination": "Chicago", "Date": "2024-12-15"},
        ] * 3  # Tripled for demo

        hotel_data = [
            {"Hotel Name": "Hilton", "Price": 300, "City": "New York", "Duration (days)": 3},
            {"Hotel Name": "Marriott", "Price": 250, "City": "Los Angeles", "Duration (days)": 2},
            {"Hotel Name": "Hyatt", "Price": 400, "City": "Chicago", "Duration (days)": 4},
        ] * 3  # Tripled for demo

        # Create a new Toplevel window
        booked_items_window = customtkinter.CTkToplevel(self)
        booked_items_window.title("Your Booked Items")
        booked_items_window.geometry("700x500")

        # Create a Tabview for Cars, Flights, and Hotels
        tabview = customtkinter.CTkTabview(booked_items_window)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Add Tabs
        cars_tab = tabview.add("Cars")
        flights_tab = tabview.add("Flights")
        hotels_tab = tabview.add("Hotels")

        # Populate Each Tab
        self.populate_tab(cars_tab, car_data, ["Model", "Price", "Rental Company", "Duration"])
        self.populate_tab(flights_tab, flight_data, ["Flight No", "Price", "Source", "Destination", "Date"])
        self.populate_tab(hotels_tab, hotel_data, ["Hotel Name", "Price", "City", "Duration (days)"])

    def view_cart(self):
        print("View Cart clicked!")