import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter
from Classes.UserManager import UserManager
from PIL import Image, ImageTk
from tkinter import ttk

class ViewPackage(customtkinter.CTk):
    def __init__(self):
        pass