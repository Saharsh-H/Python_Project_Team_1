import customtkinter
import uuid

class ViewPackageWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, db, user, added_packages, main_window):
        super().__init__(parent)
        self.db = db
        self.user = user
        self.users_col = db["users"]
        self.packages_col = db["packages"]
        self.added_packages = added_packages
        self.main_window = main_window

        user_data = self.users_col.find_one({"_id": self.user}) or {}
        self.booked_packages = user_data.get("packages", [])
        if not isinstance(self.booked_packages, list):
            self.booked_packages = []

        self.lift()
        self.title("Your Packages")
        self.geometry("600x500+100+100")
        self.bind("<Configure>", self.on_window_configure)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.wm_attributes("-topmost", 1)

        self.tab_view = customtkinter.CTkTabview(self, width=580, height=400)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.view_packages_tab = self.tab_view.add("View Packages")
        self.booked_packages_tab = self.tab_view.add("Booked Packages")

        self.view_packages_canvas = customtkinter.CTkCanvas(
            self.view_packages_tab,
            highlightthickness=0,
            bg="grey20",
        )
        self.view_packages_scrollbar = customtkinter.CTkScrollbar(
            self.view_packages_tab, command=self.view_packages_canvas.yview
        )
        self.view_packages_canvas.configure(yscrollcommand=self.view_packages_scrollbar.set)

        self.view_packages_scrollbar.pack(side="right", fill="y")
        self.view_packages_canvas.pack(side="left", fill="both", expand=True)

        self.packages_frame = customtkinter.CTkFrame(
            self.view_packages_canvas, fg_color="grey20"
        )
        self.view_packages_canvas.create_window((0, 0), window=self.packages_frame, anchor="nw")

        self.packages_frame.bind(
            "<Configure>", lambda e: self.view_packages_canvas.configure(scrollregion=self.view_packages_canvas.bbox("all"))
        )

        self.view_packages_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.display_packages(self.packages_frame, added_packages, "View Packages")

        self.book_now_button = customtkinter.CTkButton(
            self, text="Book This Package", command=self.book_now, width=200
        )
        self.book_now_button.grid(row=1, column=0, pady=10)

        self.update_book_now_button_state()

        self.booked_packages_canvas = customtkinter.CTkCanvas(
            self.booked_packages_tab,
            highlightthickness=0,
            bg="grey20",
        )
        self.booked_packages_scrollbar = customtkinter.CTkScrollbar(
            self.booked_packages_tab, command=self.booked_packages_canvas.yview
        )
        self.booked_packages_canvas.configure(yscrollcommand=self.booked_packages_scrollbar.set)

        self.booked_packages_scrollbar.pack(side="right", fill="y")
        self.booked_packages_canvas.pack(side="left", fill="both", expand=True)

        self.booked_frame = customtkinter.CTkFrame(
            self.booked_packages_canvas, fg_color="grey20"
        )
        self.booked_packages_canvas.create_window((0, 0), window=self.booked_frame, anchor="nw")

        self.booked_frame.bind(
            "<Configure>", lambda e: self.booked_packages_canvas.configure(scrollregion=self.booked_packages_canvas.bbox("all"))
        )

        self.booked_packages_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.display_packages(self.booked_frame, self.booked_packages, "Booked Packages")

    def on_window_configure(self, event):
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        self.view_packages_canvas.configure(width=window_width, height=window_height - 100)
        self.booked_packages_canvas.configure(width=window_width, height=window_height - 100)

        self.view_packages_canvas.configure(scrollregion=self.view_packages_canvas.bbox("all"))
        self.booked_packages_canvas.configure(scrollregion=self.booked_packages_canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        canvas = event.widget
        if event.delta > 0:
            canvas.yview_scroll(-1, "units")
        else:
            canvas.yview_scroll(1, "units")

    def update_book_now_button_state(self):
        if self.added_packages:
            self.book_now_button.configure(state="normal")
        else:
            self.book_now_button.configure(state="disabled")

    def display_packages(self, frame, packages, tab_name):
        for widget in frame.winfo_children():
            widget.destroy()

        if not packages:
            customtkinter.CTkLabel(
                frame, text=f"No {tab_name.lower()} yet.", font=("Roboto", 14)
            ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            return

        row = 0
        if isinstance(packages, list):
            for package in packages:
                package_id = package.get("package_id", "Unknown Package ID")
                customtkinter.CTkLabel(
                    frame, text=f"Package ID: {package_id}", font=("Roboto", 16, "bold")
                ).grid(row=row, column=0, padx=10, pady=(10, 5), sticky="w")
                row += 1

                for category, items in package.items():
                    if category != "package_id" and items:
                        customtkinter.CTkLabel(
                            frame, text=f"{category.capitalize()}:", font=("Roboto", 14, "bold")
                        ).grid(row=row, column=0, padx=10, pady=(10, 5), sticky="w")
                        row += 1

                        for item in items:
                            item_details = self.format_item_details(item, category)
                            customtkinter.CTkLabel(
                                frame, text=item_details, anchor="w", justify="left"
                            ).grid(row=row, column=0, padx=10, pady=(0, 10), sticky="ew")
                            row += 1
        elif isinstance(packages, dict):
            for category, items in packages.items():
                if items:
                    customtkinter.CTkLabel(
                        frame, text=f"{category.capitalize()}:", font=("Roboto", 16, "bold")
                    ).grid(row=row, column=0, padx=10, pady=(10, 5), sticky="w")
                    row += 1

                    for item in items:
                        item_details = self.format_item_details(item, category)
                        customtkinter.CTkLabel(
                            frame, text=item_details, anchor="w", justify="left"
                        ).grid(row=row, column=0, padx=10, pady=(0, 10), sticky="ew")

                        customtkinter.CTkButton(
                            frame,
                            text="Remove",
                            fg_color="red",
                            hover_color="darkred",
                            command=lambda cat=category, itm=item: self.remove_from_package(cat, itm)
                        ).grid(row=row, column=1, padx=10, pady=(0, 10), sticky="ew")

                        row += 1

    def remove_from_package(self, category, item):
        if category in self.added_packages and item in self.added_packages[category]:
            self.added_packages[category].remove(item)
            print(f"Removed item from {category}: {item}")

            self.display_packages(self.packages_frame, self.added_packages, "View Packages")
            self.update_book_now_button_state()

    def format_item_details(self, item, category):
        if category.lower() == "cars":
            return (
                f"Model: {item.get('car_model', 'N/A')}\n"
                f"Duration: {item.get('duration', 'N/A')} days\n"
                f"Price: {item.get('price', 'N/A')} rupees/day\n"
                f"Source: {item.get('source', 'N/A')}\n"
                f"Destination: {item.get('destination', 'N/A')}\n"
                f"Rental Company: {item.get('rental_company', 'N/A')}"
            )
        elif category.lower() == "flights":
            return (
                f"Airline: {item.get('airline', 'N/A')}\n"
                f"Departure: {item.get('departure_time', 'N/A')}\n"
                f"Duration: {item.get('duration', 'N/A')} hours\n"
                f"Price: {item.get('price', 'N/A')} rupees\n"
                f"Source: {item.get('source', 'N/A')}\n"
                f"Destination: {item.get('destination', 'N/A')}\n"
                f"Seats Available: {item.get('seats_available', 'N/A')}"
            )
        elif category.lower() == "hotels":
            return (
                f"Hotel Name: {item.get('hotel_name', 'N/A')}\n"
                f"Destination: {item.get('destination', 'N/A')}\n"
                f"Duration: {item.get('duration', 'N/A')} days\n"
                f"Price: {item.get('price', 'N/A')} rupees/day\n"
                f"Rating: {item.get('rating', 'N/A')}\n"
                f"Rooms Available: {item.get('rooms_available', 'N/A')}"
            )
        else:
            return "Unknown category"

    def book_now(self):
        package_id = str(uuid.uuid4())
        new_package = {"package_id": package_id, "Cars": [], "Hotels": [], "Flights": []}

        for category, items in self.added_packages.items():
            if category in new_package:
                new_package[category].extend(items)

            for item in items:
                if category.lower() == "flights":
                    result = self.packages_col.update_one(
                        {"_id": category, f"flights._id": item["_id"]},
                        {"$inc": {"flights.$.seats_available": -1}}
                    )
                    if result.modified_count > 0:
                        print(f"Successfully reduced seats for flight: {item['_id']}")
                    else:
                        print(f"Failed to reduce seats for flight: {item['_id']}")

                elif category.lower() == "hotels":
                    result = self.packages_col.update_one(
                        {"_id": category, f"hotels._id": item["_id"]},
                        {"$inc": {"hotels.$.rooms_available": -1}}
                    )
                    if result.modified_count > 0:
                        print(f"Successfully reduced rooms for hotel: {item['_id']}")
                    else:
                        print(f"Failed to reduce rooms for hotel: {item['_id']}")

                else:
                    self.packages_col.update_one(
                        {"_id": category},
                        {"$pull": {category.lower(): {"_id": item["_id"]}}}
                    )

        result = self.users_col.update_one(
            {"_id": self.user},
            {"$push": {"packages": new_package}},
            upsert=True
        )

        if result.modified_count > 0:
            print(f"Successfully booked package with ID {package_id}.")
        else:
            print("Failed to book the package.")

        self.added_packages.clear()
        print("Added packages cleared.")

        self.main_window.refresh_tab_views()
        self.display_packages(self.packages_frame, self.added_packages, "View Packages")

        self.booked_packages = self.users_col.find_one({"_id": self.user}).get("packages", [])
        self.display_packages(self.booked_frame, self.booked_packages, "Booked Packages")
        self.update_book_now_button_state()