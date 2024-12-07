import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter
from Windows.ViewPackageWindow import ViewPackage
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
        self.source_entry = None
        self.destination_entry = None
        main_window = customtkinter.CTkToplevel(self)
        main_window.lift()
        main_window.title("FakeMyTrip | Where your journey begins... hypothetically")
        main_window.geometry("1024x768")
        main_window.grid_columnconfigure(0, weight=1)
        main_window.grid_rowconfigure(0, weight=0)
        main_window.grid_rowconfigure(1, weight=1)
        self.main_window = main_window
        self.header_frame = customtkinter.CTkFrame(main_window, height=50, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=0)  # Logout Button
        self.header_frame.grid_columnconfigure(2, weight=0)  # View Cart Button
        self.entries = {}  # Dictionary to store input widgets for each tab

        self.duration = customtkinter.CTkLabel(
            self.header_frame,
            text="Duration",
            width=100,
        )
        self.duration.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

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

        self.car_durations = {}  # Dictionary to store durations for each car

    def add_tab_content(self, tab, tab_type, callback):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=0)

        self.entries[tab_type] = {}  # Initialize entries for this tab

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
        self.entries[tab_type]['source'] = source_entry  # Store source entry

        destination_entry = customtkinter.CTkEntry(
            tab, placeholder_text=f"{tab_type} Destination", height=50, width=250
        )
        destination_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.entries[tab_type]['destination'] = destination_entry  # Store destination entry

        date_entry = customtkinter.CTkEntry(
            tab, placeholder_text=f"Travel Date (DD-MM-YYYY)", height=50, width=250
        )
        date_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))

        search_button = customtkinter.CTkButton(tab, text=f"Search {tab_type}", command=callback)
        search_button.grid(row=3, column=0, padx=10, pady=10)

        self.view_packages_button = customtkinter.CTkButton(
            tab,
            text="View Your Package",
            command=self.view_packages
        )
        self.view_packages_button.grid(row=3, column=1, padx=10, pady=(0, 0))

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

        self.view_packages_button = customtkinter.CTkButton(
            tab,
            text = "View Your Package",
            command = self.view_packages
            )
        self.view_packages_button.grid(row = 3,column = 1 ,padx = 10,pady = (0,0))

    def search_cars(self):
        cars_tab = self.main_window.tab_view.tab("Cars")

        # Clear any existing results frame
        if hasattr(self, "results_frame") and self.results_frame.winfo_exists():
            self.results_frame.destroy()

        car_data = self.package_col.find_one({"_id": "Cars"})
        if not car_data or "cars" not in car_data:
            print("No car data found!")
            return

        source = self.entries['Cars']['source'].get().strip()
        destination = self.entries['Cars']['destination'].get().strip()

        data = car_data["cars"]
        filtered_cars = [
            car for car in data
            if (not source or car.get("source", "").lower() == source.lower()) and
               (not destination or car.get("destination", "").lower() == destination.lower())
        ]

        # Create a frame to hold the canvas and scrollbar
        self.results_frame = customtkinter.CTkFrame(cars_tab, corner_radius=10)
        self.results_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configure grid weights to allow resizing
        cars_tab.grid_rowconfigure(4, weight=1)  # Ensure the results frame grows
        cars_tab.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)

        # Create a canvas for scrolling
        canvas = customtkinter.CTkCanvas(self.results_frame, bg="white", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Add a vertical scrollbar linked to the canvas
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        scrollable_frame = customtkinter.CTkFrame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        scrollable_frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind canvas resize events to adjust width
        def resize_canvas(event):
            canvas_width = event.width
            canvas.itemconfig(scrollable_frame_window, width=canvas_width)

        canvas.bind("<Configure>", resize_canvas)

        # Configure grid for the scrollable frame
        scrollable_frame.grid_columnconfigure(0, weight=3)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        scrollable_frame.grid_columnconfigure(2, weight=1)
        scrollable_frame.grid_columnconfigure(3, weight=1)

        # Add headers for the table
        header_style = {"font": ("Roboto", 20, "bold"), "anchor": "center"}
        customtkinter.CTkLabel(scrollable_frame, text="Description", **header_style).grid(
            row=0, column=0, padx=10, pady=5, sticky="ew"
        )
        customtkinter.CTkLabel(scrollable_frame, text="Add", **header_style).grid(
            row=0, column=1, padx=10, pady=5, sticky="ew"
        )
        customtkinter.CTkLabel(scrollable_frame, text="Delete", **header_style).grid(
            row=0, column=2, padx=10, pady=5, sticky="ew"
        )
        customtkinter.CTkLabel(scrollable_frame, text="Duration", **header_style).grid(
            row=0, column=3, padx=10, pady=5, sticky="ew"
        )

        # Populate the scrollable frame with data
        for index, car in enumerate(filtered_cars, start=1):
            car_id = car.get("car_model", f"car_{index}")
            if car_id not in self.car_durations:
                self.car_durations[car_id] = 0

            car_details = (
                f"Model: {car['car_model']}\n"
                f"Price: {car['price']} rupees/day\n"
                f"Source: {car['source']}\n"
                f"Destination: {car['destination']}\n"
                f"Rental Company: {car['rental_company']}\n"
            )
            customtkinter.CTkLabel(scrollable_frame, text=car_details, anchor="w", justify="left").grid(
                row=index, column=0, padx=10, pady=5, sticky="ew"
            )

            duration_label = customtkinter.CTkLabel(
                scrollable_frame,
                text=f"{self.car_durations[car_id]} Days",
                anchor="e",
                justify="right",
                font=("Roboto", 20, "bold")
            )
            duration_label.grid(row=index, column=3, padx=10, pady=5, sticky="ew")

            customtkinter.CTkButton(
                scrollable_frame,
                text="Add",
                command=lambda c=car_id, lbl=duration_label: self.update_duration(c, lbl, 1)
            ).grid(row=index, column=1, padx=10, pady=5, sticky="ew")

            customtkinter.CTkButton(
                scrollable_frame,
                text="Delete",
                command=lambda c=car_id, lbl=duration_label: self.update_duration(c, lbl, -1)
            ).grid(row=index, column=2, padx=10, pady=5, sticky="ew")

    def update_duration(self, car_id, label, change):
        self.car_durations[car_id] = max(0, self.car_durations[car_id] + change)
        label.configure(text=f"{self.car_durations[car_id]} Days")
        print(f"Car {car_id} duration updated to {self.car_durations[car_id]}")

    def book_car(self, car):
        print(f"Booking car: {car['car_model']} from {car['rental_company']} at {car['price']} rupees/day")

    def add_to_pkg(self, car_id, label):
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

        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor="center")

        for record in data:
            tree.insert("", "end", values=tuple(record.values()))

    def view_packages(self):
        view_pckg = ViewPackage()

    def view_cart(self):
        print("View Cart clicked!")