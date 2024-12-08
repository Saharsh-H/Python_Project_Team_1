# Travel Booking System
    This app is a travel booking system that allows users to search for and book flights, hotels and rental cars. This app is written using Python.

# How to use the app
    Step 1: Open the main.py file and click on "Run".
    Step 2: Create an account by clicking on the register button.
    Step 3: Enter the same credentials in the login page that you used while registering.

# List of supported Operating Systems
1. Windows
2. Mac OS
3. Linux

# Requirements
Python and CustomTkinter should be installed on your machine.

# Features Implemented
need to fill this

# Libraries used
1. CustomTkinter
2. Tkinter
3. Pymongo Database
4. PIL

# In-Built Modules used
1. Sys and OS: They are used to add the parent directory to the system path so that other modules can be imported.

2. CustomTkinter: Provides the graphical components used in the application and was used for the overall GUI of the application.

3. Tkinter.ttk: It helped us use themed widgets like Treeview and scrollbar in our GUI.

3. Pymongo: It helps us to connect to the MongoDB database and also interacts with the users and packages collections.

4. PIL: Used for opening and resizing the logo image and to convert it to a format compatible with CustomTkinter.

5. Uuid: It was used to generate Unique Package ID's.

# Modules created
1. Windows.RegisterWindow: It imports the RegisterWindow class, that is used for handling the user registration.

2. Classes.CarManager: It imports the CarManager class, that is used to manage cars available, addition and viewing from a manager point of view.

3. Windows.MainWindow: It imports the MainWindow class, which leads to the main application window after the user succesfully logs in.

4. Classes.UserManager: It imports the UserManager class, that is used to create a new user object during registration.

# Classes created
1. Travel Manager: This is the base class that manages general travel-related information such as a unique identifier, price, duration, and destination. It tracks availability with a default value of True. The get_details method returns the key details of the travel like its ID, availability, price, duration, and destination. Most other classes inherit attributes and methods from this class.

2. Car Manager: It inherits from the Travel Manager class, adds attributes and methods related to car rentals.  It provides a mechanism to manage details about a car rental, including specific details like the car model, source, and rental company.

3. Hotel Manager: This class extends the Travel Manager class and incorporates attributes and methods related to hotel stays. It facilitates the management of hotel information, such as the hotel name, its rating, and the availability of rooms.

4. Flight Manager:  It extends the functionality of the Travel Manager class by incorporating attributes and methods specific to flight reservations. It enables managing flight details, including the airline, departure location, departure time, and seat availability.

5. Package Manager: This class manages a travel package, identified by a unique package ID. It organizes the package into three categories: cars, hotels, and flights, with each category holding a list of relevant items.

6. User Manager: This class handles user information, including a unique username and password. It also manages a list of packages associated with the user.

7. App: It displays a login form with username, password fields and a "Login" button for an already existing user. It also provides a "Register" button to create a new user.

8. Register Window: It is the registration window where users can create new accounts with a unique username and password.

9. Main Window: It is the central window for the user' operations, that allows the user to search, navigate between tabs (Cars, Flights, Hotels) and also book packages

10. View Package Window: It allows the user to view the packages that they have added and 

# Group Members
1. A Sri Avneesh: Worked on the main window page including populating the individual tabs when we click on search cars, hotels or flights.

2. Kamalnath A: Worked on creating a logout button and view package button, and also created the Register window.

3. Parikshith Aithal K V: Worked on the backend including implementation of the classes and inheritance.

4. Saharsh S Hiremath: Worked on the login page and the README.md file.

5. Rihan Sourabh Doshi: Worked on the view package window and created the entire database to store the data and packages.