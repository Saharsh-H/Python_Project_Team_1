import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter
from PIL import Image, ImageTk
from tkinter import ttk
from Windows.ViewPackageWindow import ViewPackageWindow
from Classes.PackageManager import PackageManager
class MainWindow(customtkinter.CTk):
    def __init__(self, db, parent, packages_col, user, added_packages):
        super().__init__()

        self.db = db
        self.user = user
        self.parent = parent
        self.added_packages = added_packages
        self.package_col = packages_col
        parent.withdraw()
        if not self.added_packages:
            self.added_packages = {
                "Cars": [],
                "Flights": [],
                "Hotels": []
            }
        self.current_page = 1
        self.source_entry = None
        self.destination_entry = None
        main_window = customtkinter.CTkToplevel(self)
        main_window.lift()
        main_window.title("FakeMyTrip | Where your journey begins... hypothetically")
        main_window.geometry("1000x800")
        main_window.grid_columnconfigure(0, weight=1)
        main_window.grid_rowconfigure(0, weight=0)
        main_window.grid_rowconfigure(1, weight=1)
        self.main_window = main_window
        self.success_label = customtkinter.CTkLabel(self.main_window, text="", fg_color="green", height=30)
        self.header_frame = customtkinter.CTkFrame(main_window, height=50, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=0)
        self.header_frame.grid_columnconfigure(2, weight=0)
        self.entries = {}

        self.duration = customtkinter.CTkLabel(
            self.header_frame,
            text="Duration",
            width=100,
        )
        self.duration.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        self.success_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.success_label.grid_remove()

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

        self.car_durations = {}

    def add_tab_content(self, tab, tab_type, callback):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=0)

        self.entries[tab_type] = {}

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
            tab, placeholder_text=f"Pickup City", height=50, width=250
        )
        source_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.entries[tab_type]['source'] = source_entry

        destination_entry = customtkinter.CTkEntry(
            tab, placeholder_text=f"Drop City", height=50, width=250
        )
        destination_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.entries[tab_type]['destination'] = destination_entry

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

        self.entries['Hotels'] = {}
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
        self.entries['Hotels']['location'] = location_entry

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

        self.results_frame = customtkinter.CTkFrame(cars_tab, corner_radius=10)
        self.results_frame.grid(row=5, column=0, columnspan=5, padx=10, pady=100, sticky="nsew")

        cars_tab.grid_rowconfigure(5, weight=3)
        cars_tab.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)
        if not filtered_cars:
            no_results_label = customtkinter.CTkLabel(self.results_frame, text="No cars found for your search.",
                                                      fg_color="red", anchor="center")
            no_results_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            return
        self.success_label_car = customtkinter.CTkLabel(cars_tab, text="", fg_color="green", height=30)

        canvas = customtkinter.CTkCanvas(self.results_frame, bg="grey20", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = customtkinter.CTkFrame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        scrollable_frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def resize_canvas(event):
            canvas_width = event.width
            canvas.itemconfig(scrollable_frame_window, width=canvas_width)

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(scrollable_frame_window, width=e.width))
        canvas.configure(bg="grey20")

        # Bind mouse wheel for scrolling (for both Windows and Linux)
        def on_mouse_wheel(event):
            if event.delta:  # For Windows
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:  # For Linux
                canvas.yview_scroll(-1*(event.num-5), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # For Windows
        canvas.bind_all("<Button-4>", on_mouse_wheel)  # For Linux (scroll up)
        canvas.bind_all("<Button-5>", on_mouse_wheel)  # For Linux (scroll down)

        scrollable_frame.grid_columnconfigure(0, weight=3)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        scrollable_frame.grid_columnconfigure(2, weight=1)
        scrollable_frame.grid_columnconfigure(3, weight=1)

        header_style = {"font": ("Roboto", 20, "bold"), "anchor": "center"}
        customtkinter.CTkLabel(scrollable_frame, text="Description", **header_style).grid(
            row=0, column=0, padx=10, pady=5, sticky="ew"
        )
        customtkinter.CTkLabel(scrollable_frame, text="Add", **header_style).grid(
            row=0, column=2, padx=10, pady=5, sticky="ew"
        )
        customtkinter.CTkLabel(scrollable_frame, text="Delete", **header_style).grid(
            row=0, column=3, padx=10, pady=5, sticky="ew"
        )
        customtkinter.CTkLabel(scrollable_frame, text="Duration", **header_style).grid(
            row=0, column=4, padx=10, pady=5, sticky="ew"
        )

        for index, car in enumerate(filtered_cars, start=1):
            car_id = car['_id']
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
            duration_label.grid(row=index, column=4, padx=10, pady=5, sticky="ew")

            customtkinter.CTkButton(
                scrollable_frame,
                text="Add",
                command=lambda c=car_id, lbl=duration_label: self.update_duration(c, lbl, 1)
            ).grid(row=index, column=2, padx=10, pady=5, sticky="ew")

            customtkinter.CTkButton(
                scrollable_frame,
                text="Delete",
                command=lambda c=car_id, lbl=duration_label: self.update_duration(c, lbl, -1)
            ).grid(row=index, column=3, padx=10, pady=5, sticky="ew")

            customtkinter.CTkButton(
                scrollable_frame,
                text="Add to package",
                state="disabled" if self.car_durations[car_id] == 0 else "normal",
                command=lambda c=car_id, lbl=duration_label: self.add_to_pkg(c, lbl)
            ).grid(row=index, column=1, padx=10, pady=5, sticky="ew")

    def update_duration(self, car_id, label, change):
        self.car_durations[car_id] = max(0, self.car_durations[car_id] + change)
        label.configure(text=f"{self.car_durations[car_id]} Days")
        print(f"Car {car_id} duration updated to {self.car_durations[car_id]}")

        add_button = label.master.grid_slaves(row=label.grid_info()["row"], column=1)[0]
        if self.car_durations[car_id] > 0:
            add_button.configure(state="normal")
        else:
            add_button.configure(state="disabled")

    def book_car(self, car):
        print(f"Booking car: {car['car_model']} from {car['rental_company']} at {car['price']} rupees/day")

    def add_to_pkg(self, car_id, label):
        cars = self.package_col.find_one({"_id": "Cars"})
        car = list(filter(lambda c: c["_id"] == car_id, cars["cars"]))[0]

        updated_duration = self.car_durations.get(car_id, 0)
        car["duration"] = updated_duration

        if self.added_packages == dict():
            self.added_packages["Cars"] = [car]
            self.added_packages["Flights"] = []
            self.added_packages["Hotels"] = []
        else:
            self.added_packages["Cars"].append(car)

        self.success_label_car.configure(text="Car added to package successfully", fg_color="green")
        self.success_label_car.grid()  # Show the success label
        self.after(3000, lambda: self.success_label_car.grid_remove())

    def delete_car(self, car):
        print(f"Deleting car: {car['car_model']} from {car['rental_company']} at {car['price']} rupees/day")

    def add_to_package(self, category, item):
        if category not in self.added_packages:
            self.added_packages[category] = []

        self.added_packages[category].append(item)

        print(f"Added {category} item to package: {item}")


        if hasattr(self, "success_label"):
            self.success_label.configure(text=f"{category} added to package successfully!", fg_color="green")
            self.success_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
            self.after(3000, lambda: self.success_label.grid_forget())

    def search_flights(self):
        flights_tab = self.main_window.tab_view.tab("Flights")

        if hasattr(self, "results_frame_flights") and self.results_frame_flights.winfo_exists():
            self.results_frame_flights.destroy()

        flight_data = self.package_col.find_one({"_id": "Flights"})
        if not flight_data or "flights" not in flight_data:
            print("No flight data found!")
            return

        source = self.entries['Flights']['source'].get().strip()
        destination = self.entries['Flights']['destination'].get().strip()

        data = flight_data["flights"]
        filtered_flights = [
            flight for flight in data
            if (not source or flight.get("source", "").lower() == source.lower()) and
               (not destination or flight.get("destination", "").lower() == destination.lower())
        ]

        self.results_frame_flights = customtkinter.CTkFrame(flights_tab, corner_radius=10)
        self.results_frame_flights.grid(row=5, column=0, columnspan=5, padx=10, pady=100, sticky="nsew")

        flights_tab.grid_rowconfigure(5, weight=3)
        flights_tab.grid_columnconfigure(0, weight=1)
        self.results_frame_flights.grid_rowconfigure(0, weight=1)
        self.results_frame_flights.grid_columnconfigure(0, weight=1)
        if not filtered_flights:
            no_results_label = customtkinter.CTkLabel(self.results_frame_flights,
                                                      text="No flights found for your search.", fg_color="red",
                                                      anchor="center")
            no_results_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            return
        canvas = customtkinter.CTkCanvas(self.results_frame_flights, bg="grey20", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.results_frame_flights, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(bg="grey20")
        scrollable_frame = customtkinter.CTkFrame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        scrollable_frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def resize_canvas(event):
            canvas_width = event.width
            canvas.itemconfig(scrollable_frame_window, width=canvas_width)

        canvas.bind("<Configure>", resize_canvas)

        def on_mouse_wheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:
                canvas.yview_scroll(-1*(event.num-5), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Button-4>", on_mouse_wheel)
        canvas.bind_all("<Button-5>", on_mouse_wheel)

        scrollable_frame.grid_columnconfigure(0, weight=3)
        scrollable_frame.grid_columnconfigure(1, weight=1)

        header_style = {"font": ("Roboto", 20, "bold"), "anchor": "center"}
        customtkinter.CTkLabel(scrollable_frame, text="Description", **header_style).grid(
            row=0, column=0, padx=10, pady=5, sticky="ew"
        )
        customtkinter.CTkLabel(scrollable_frame, text="Add to Package", **header_style).grid(
            row=0, column=1, padx=10, pady=5, sticky="ew"
        )

        for index, flight in enumerate(filtered_flights, start=1):
            flight_details = (
                f"Airline: {flight['airline']}\n"
                f"Departure: {flight['departure_time']}\n"
                f"Duration: {flight['duration']} hours\n"
                f"Price: {flight['price']} rupees\n"
                f"Source: {flight['source']}\n"
                f"Destination: {flight['destination']}\n"
                f"Seats Available: {flight['seats_available']}\n"
            )
            customtkinter.CTkLabel(scrollable_frame, text=flight_details, anchor="w", justify="left").grid(
                row=index, column=0, padx=10, pady=5, sticky="ew"
            )

            customtkinter.CTkButton(
                scrollable_frame,
                text="Add to package",
                command=lambda f=flight: self.add_to_package("Flights", f)
            ).grid(row=index, column=1, padx=10, pady=5, sticky="ew")
    
        self.success_label = customtkinter.CTkLabel(flights_tab, text="", fg_color="green", height=30)

    def search_hotels(self):
        hotels_tab = self.main_window.tab_view.tab("Hotels")

        if hasattr(self, "results_frame_hotels") and self.results_frame_hotels.winfo_exists():
            self.results_frame_hotels.destroy()

        hotel_data = self.package_col.find_one({"_id": "Hotels"})
        if not hotel_data or "hotels" not in hotel_data:
            print("No hotel data found!")
            return

        location_entry = self.entries['Hotels'].get('location', None)
        location = location_entry.get().strip() if location_entry else ""

        data = hotel_data["hotels"]
        filtered_hotels = [
            hotel for hotel in data
            if not location or hotel.get("destination", "").lower() == location.lower()
        ]

        self.hotel_durations = {}

        self.results_frame_hotels = customtkinter.CTkFrame(hotels_tab, corner_radius=10)
        self.results_frame_hotels.grid(row=5, column=0, columnspan=5, padx=10, pady=100, sticky="nsew")



        hotels_tab.grid_rowconfigure(5, weight=3)
        hotels_tab.grid_columnconfigure(0, weight=1)
        self.results_frame_hotels.grid_rowconfigure(0, weight=1)
        self.results_frame_hotels.grid_columnconfigure(0, weight=1)
        if not filtered_hotels:
            no_results_label = customtkinter.CTkLabel(self.results_frame_hotels,
                                                      text="No hotels found for your search.", fg_color="red",
                                                      anchor="center")
            no_results_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            return
        canvas = customtkinter.CTkCanvas(self.results_frame_hotels, bg="grey20", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.results_frame_hotels, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = customtkinter.CTkFrame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        scrollable_frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(bg="grey20")
        def resize_canvas(event):
            canvas_width = event.width
            canvas.itemconfig(scrollable_frame_window, width=canvas_width)

        canvas.bind("<Configure>", resize_canvas)

        def on_mouse_wheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:
                canvas.yview_scroll(-1*(event.num-5), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Button-4>", on_mouse_wheel)
        canvas.bind_all("<Button-5>", on_mouse_wheel)

        scrollable_frame.grid_columnconfigure(0, weight=3)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        scrollable_frame.grid_columnconfigure(2, weight=1)
        scrollable_frame.grid_columnconfigure(3, weight=1)

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

        for index, hotel in enumerate(filtered_hotels, start=1):
            hotel_id = hotel['_id']
            if hotel_id not in self.hotel_durations:
                self.hotel_durations[hotel_id] = 0

            hotel_details = (
                f"Hotel Name: {hotel['hotel_name']}\n"
                f"Destination: {hotel['destination']}\n"
                f"Rating: {hotel['rating']} stars\n"
                f"Rooms Available: {hotel['rooms_available']}\n"
                f"Price: {hotel['price']} rupees/day\n"
            )
            customtkinter.CTkLabel(scrollable_frame, text=hotel_details, anchor="w", justify="left").grid(
                row=index, column=0, padx=10, pady=5, sticky="ew"
            )

            duration_label = customtkinter.CTkLabel(
                scrollable_frame,
                text=f"{self.hotel_durations[hotel_id]} Days",
                anchor="e",
                justify="right",
                font=("Roboto", 20, "bold")
            )
            duration_label.grid(row=index, column=3, padx=10, pady=5, sticky="ew")

            customtkinter.CTkButton(
                scrollable_frame,
                text="Add",
                command=lambda h=hotel_id, lbl=duration_label: self.update_hotel_duration(h, lbl, 1)
            ).grid(row=index, column=1, padx=10, pady=5, sticky="ew")

            customtkinter.CTkButton(
                scrollable_frame,
                text="Delete",
                command=lambda h=hotel_id, lbl=duration_label: self.update_hotel_duration(h, lbl, -1)
            ).grid(row=index, column=2, padx=10, pady=5, sticky="ew")

            customtkinter.CTkButton(
                scrollable_frame,
                text="Add to package",
                state="disabled" if self.hotel_durations[hotel_id] == 0 else "normal",
                command=lambda h=hotel_id, lbl=duration_label: self.add_hotel_to_package(h, lbl)
            ).grid(row=index, column=4, padx=10, pady=5, sticky="ew")

        self.success_label= customtkinter.CTkLabel(hotels_tab, text="", fg_color="green", height=30)

    def logout(self):
        print("Logout clicked!")
        self.parent.deiconify()
        self.destroy()

    def update_hotel_duration(self, hotel_id, label, change):
        self.hotel_durations[hotel_id] = max(0, self.hotel_durations[hotel_id] + change)
        label.configure(text=f"{self.hotel_durations[hotel_id]} Days")
        print(f"Hotel {hotel_id} duration updated to {self.hotel_durations[hotel_id]}")
        add_button = label.master.grid_slaves(row=label.grid_info()["row"], column=4)[0]
        if self.hotel_durations[hotel_id] > 0:
            add_button.configure(state="normal")
        else:
            add_button.configure(state="disabled")

    def add_hotel_to_package(self, hotel_id, label):
        hotels = self.package_col.find_one({"_id": "Hotels"})
        hotel = list(filter(lambda h: h["_id"] == hotel_id, hotels["hotels"]))[0]

        if "Hotels" not in self.added_packages:
            self.added_packages["Hotels"] = []

        updated_duration = self.hotel_durations.get(hotel_id, 0)
        hotel["duration"] = updated_duration

        self.added_packages["Hotels"].append(hotel)

        self.success_label.configure(text="Hotel added to package successfully", fg_color="green")
        self.success_label.grid()
        self.after(3000, lambda: self.success_label.grid_remove())

    def populate_tab(self, tab, data, headers):
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
        if hasattr(self, 'view_package_window') and self.view_package_window.winfo_exists():
            self.view_package_window.lift()
        else:
            self.view_package_window = ViewPackageWindow(self, self.db, self.user, self.added_packages, self)

    def view_cart(self):
        print("View Cart clicked!")

    def refresh_tab_views(self):
        self.search_cars()
        self.search_flights()
        self.search_hotels()
        print("All tab views refreshed.")