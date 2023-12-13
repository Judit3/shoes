# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials


# Connect the Googlesheet for this project using Google APIs
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('shoes')

shoe_list = SHEET.worksheet('shoe_list').get_all_values()

# Define variables to target the columns in the spreadsheet to access them in the functions

brands = SHEET.worksheet('shoe_list').col_values(1)
descriptions = SHEET.worksheet('shoe_list').col_values(2)
prices = SHEET.worksheet('shoe_list').col_values(3)


class Brand:
    """
    Class representing brand within the spreadsheet
    """
    global shoe_list

    def __init__(self, brand_name):
        for brand in shoe_list:
            if brand_name == brand[0]:
                self.shoe_description = brand[1]
                self.shoe_price = brand[2]
                self.brand_name = brand_name

    def show_information(self):
        """
        Gives format for shoe info to print
        """
        print(f"Brand: {self.brand_name}\n")
        print(f"Description: {self.shoe_description}\n")
        print(f"Price: {self.shoe_price}\n")

def print_shoe_info():
    """ 
    Allows the user to enter the name of the shoe brand and shows the information of the selected product
    """
    brand_name = input("Please, enter a shoe brand (as seen on the spreadsheet): \n")

    if(brand_name in SHEET.worksheet("shoe_list").col_values(1)):
        my_brand = Brand(brand_name)
        my_brand.show_information()
    else:
        print("Sorry, brand not found")

