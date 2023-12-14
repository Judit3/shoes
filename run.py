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
        Gives format for shoe information to print
        """
        print(f"Brand: {self.brand_name}\n")
        print(f"Description: {self.shoe_description}\n")
        print(f"Price: {self.shoe_price}\n")

    def append_row(self):
        """
        Appends the brand information to the 'shopping' worksheet
        """
        shopping_sheet = SHEET.worksheet('shopping')
        shopping_sheet.append_row([self.brand_name, self.shoe_description, self.shoe_price])
        print("Brand information copied to 'shopping' worksheet.\n")


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

    select_what_to_do()


def copy_to_shopping():
    """ 
    Allows the user to enter the name of the shoe brand and copies the information to the 'shopping' worksheet
    """
    brand_name = input("Please enter the shoe brand that you would like to buy (as seen on the spreadsheet): \n")

    if brand_name in SHEET.worksheet("shoe_list").col_values(1):
        my_brand = Brand(brand_name)
        my_brand.append_row()
    else:
        print("Sorry, brand not found\n")

    select_what_to_do()


def exit_program():
    """
    Allows the users to exit the program
    """
    confirm_exit = input("Confirm exit (Y/N):\n")
    
    if confirm_exit == "Y":
        print("Exiting program...\n")
        print("To start again, please, press Run Program button avobe\n")
        exit()
    elif confirm_exit == "N":
        print("Great!\n")
        select_what_to_do()
    else:
        print("INVALID INPUT, please, enter Y or N in capital letters\n")
        exit_program()

def select_what_to_do():
    """
    Allow users to select what they want to do among the functionalities of the program
    """
    print("Welcome to SHOES\n")
    print("How can we help you?\n")
    print("1 - Shoe information by brand\n")
    print("2 - Add shoe to the shopping list\n")
    print("3 - Exit the program\n")

    what_to_do_input = input("Please, enter the numbers of one of the previous options:\n")

    if what_to_do_input == "1":
        print_shoe_info()
    elif what_to_do_input == "2":
        copy_to_shopping()
    elif what_to_do_input == "3":
        exit_program()

select_what_to_do()


