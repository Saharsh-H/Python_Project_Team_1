import customtkinter
import uuid  # For generating unique package IDs


class ViewPackageWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, db, user, added_packages):
        super().__init__(parent)
        self.db = db
        self.user = user
        self.users_col = db["users"]
        self.packages_col = db["packages"]
        self.added_packages = added_packages
        self.booked_packages = self.users_col.find_one({"_id": self.user}).get("packages", [])
        self.lift()
        self.title("Your Packages")
        self.geometry("600x400")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tab_view = customtkinter.CTkTabview(self, width=500, height=350)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.view_packages_tab = self.tab_view.add("View Packages")
        self.booked_packages_tab = self.tab_view.add("Booked Packages")

        self.tab_view.grid_columnconfigure(0, weight=1)
        self.tab_view.grid_rowconfigure(0, weight=1)

        # Frame for "View Packages" tab
        self.packages_frame = customtkinter.CTkFrame(self.view_packages_tab)
        self.packages_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.packages_frame.grid_columnconfigure(0, weight=1)

        self.display_packages(self.packages_frame, self.added_packages, "View Packages")

        # Add a "Book Now" button to the bottom center of the main window
        self.book_now_button = customtkinter.CTkButton(
            self, text="Book Now", command=self.book_now
        )
        self.book_now_button.grid(row=1, column=0, pady=10, sticky="ew")
        self.update_book_now_button()

        # Frame for "Booked Packages" tab
        self.booked_frame = customtkinter.CTkFrame(self.booked_packages_tab)
        self.booked_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.booked_frame.grid_columnconfigure(0, weight=1)

        self.display_packages(self.booked_frame, self.booked_packages, "Booked Packages")

    def update_book_now_button(self):
        """Update visibility of the 'Book Now' button based on added_packages."""
        if not self.added_packages:
            self.book_now_button.grid_remove()  # Hide the button if no packages to book
        else:
            self.book_now_button.grid()  # Show the button if packages exist

    def display_packages(self, frame, packages, tab_name):
        # Clear any previous content
        for widget in frame.winfo_children():
            widget.destroy()

        if not packages:
            # Display a message if no packages are present
            customtkinter.CTkLabel(
                frame, text=f"No {tab_name.lower()} yet.", font=("Roboto", 14)
            ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            return

        row = 0
        for package in packages:  # Iterate through the list of packages
            package_id = package.get("package_id", "Unknown Package ID")
            customtkinter.CTkLabel(
                frame, text=f"Package ID: {package_id}", font=("Roboto", 16, "bold")
            ).grid(row=row, column=0, padx=10, pady=(10, 5), sticky="w")
            row += 1

            for category, items in package.items():
                if category != "package_id" and items:  # Skip package_id and empty categories
                    customtkinter.CTkLabel(
                        frame, text=f"{category.capitalize()}:", font=("Roboto", 14, "bold")
                    ).grid(row=row, column=0, padx=10, pady=(10, 5), sticky="w")
                    row += 1

                    for item in items:
                        item_details = (
                            f"Model: {item.get('car_model', 'N/A')}\n"
                            f"Duration: {item.get('duration', 'N/A')} days\n"
                            f"Price: {item.get('price', 'N/A')} rupees/day\n"
                            f"Source: {item.get('source', 'N/A')}\n"
                            f"Destination: {item.get('destination', 'N/A')}\n"
                            f"Rental Company: {item.get('rental_company', 'N/A')}"
                        )
                        customtkinter.CTkLabel(
                            frame, text=item_details, anchor="w", justify="left"
                        ).grid(row=row, column=0, padx=10, pady=(0, 10), sticky="ew")
                        row += 1

    def book_now(self):
        # Generate a unique package ID
        package_id = str(uuid.uuid4())

        # Initialize the new package structure
        new_package = {"package_id": package_id, "Cars": [], "Hotels": [], "Flights": []}

        # Populate the new package with items from added_packages
        for category, items in self.added_packages.items():
            if category in new_package:
                new_package[category].extend(items)  # Add items to the respective category

        # Update the user's document in the database
        result = self.users_col.update_one(
            {"_id": self.user},
            {
                "$push": {"packages": new_package},  # Push the new package into the packages array
            },
            upsert=True  # Create the user's document if it doesn't exist
        )

        if result.modified_count > 0:
            print(f"Successfully booked package with ID {package_id}.")
        else:
            print("Failed to book the package.")

        # Clear the added_packages dictionary
        self.added_packages.clear()
        print("Added packages cleared.")

        # Refresh the "View Packages" tab
        self.display_packages(self.packages_frame, self.added_packages, "View Packages")
        # Refresh the "Booked Packages" tab
        self.booked_packages = self.users_col.find_one({"_id": self.user}).get("packages", [])
        self.display_packages(self.booked_frame, self.booked_packages, "Booked Packages")
        self.update_book_now_button()
