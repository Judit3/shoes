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
shopping_sheet = SHEET.worksheet('shopping')

# Define variables to target the columns in the spreadsheet to access them in the functions

brands = SHEET.worksheet('shoe_list').col_values(1)
descriptions = SHEET.worksheet('shoe_list').col_values(2)
prices = SHEET.worksheet('shoe_list').col_values(3)

#Global varaible to track wether the program is running for the first time
program_has_run = False

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
        print("Sorry, brand not found.")

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
        print("Sorry, brand not found.\n")

    select_what_to_do()


def sum_shopping_price():
    """ 
    Allows to sum the values in the price column into the shopping list
    """
    priece_values = (shopping_sheet.col_values(3))

    priece_values_converted = []
    for priece_value in priece_values[1:]:
        priece_values_converted.append(int(priece_value))
    
    total = sum(priece_values_converted)
    print(f"Total: {total}\n")
    
    shopping_sheet.update_cell(2, 4, total)


def delete_row_in_shopping():
    """
    Allows the user to clear the content of one row in the shopping worksheet by brand name
    """
    brand_name = input("Please, enter the name on the brand you want to delete from your shopping list: \n")
    
    if brand_name in SHEET.worksheet("shopping").col_values(1):
        brand_column = shopping_sheet.col_values(1)
        row_index = brand_column.index(brand_name) + 1
    
        confirm_deletion = input(f"Do you want to delete the brand {brand_name} form your shopping list? (Y/N):\n")
        if confirm_deletion == "Y":
            shopping_sheet.delete_rows(row_index)
            print(f"Row for brand {brand_name} has been deleted.\n")
        elif confirm_deletion == "N":
            print("Great!\n")
            select_what_to_do()
        else:
            print("INVALID INPUT, please, enter Y or N in capital letters.\n")
            delete_row_in_shopping()


def clear_shopping_worksheet():
    """
    Allows the user to clear the content of the shopping worksheet 
    """
    confirm_clearance = input("Do you want to empty your shopping list? (Y/N):\n")

    if confirm_clearance == "Y":
        print("Shopping list has been emptied.\n")
        headings = shopping_sheet.row_values(1)
        shopping_sheet.clear()
        shopping_sheet.append_row(headings)
    elif confirm_clearance == "N":
        print("Great!\n")
        select_what_to_do()
    else:
        print("INVALID INPUT, please, enter Y or N in capital letters.\n")
        clear_shopping_worksheet()


def exit_program():
    """
    Allows the users to exit the program
    """
    confirm_exit = input("Confirm exit (Y/N):\n")
    
    if confirm_exit == "Y":
        print("Exiting program...\n")
        print("To start again, please, click the Run Program button above.\n")
        exit()
    elif confirm_exit == "N":
        print("Great!\n")
        select_what_to_do()
    else:
        print("INVALID INPUT, please, enter Y or N in capital letters.\n")
        exit_program()


def select_what_to_do():
    """
    Allow users to select what they want to do among the functionalities of the program
    """
    global program_has_run
    if not program_has_run:
        print("Welcome to SHOES\n")
        program_has_run = True

    print("How can we help you?\n")
    print("1 - Shoe information by brand\n")
    print("2 - Add shoe to the shopping list\n")
    print("3 - Calculate the total price of your shopping list\n")
    print("4 - Delete one brand row form the shopping list\n")
    print("5 - Clear the content of the shopping list\n")
    print("6 - Exit the program\n")
   

    what_to_do_input = input("Please, enter the number of one of the options above:\n")

    if what_to_do_input == "1":
        print_shoe_info()
    elif what_to_do_input == "2":
        copy_to_shopping()
    elif what_to_do_input == "3":
        sum_shopping_price()
    elif what_to_do_input == "4":
        delete_row_in_shopping()
    elif what_to_do_input == "5":
        clear_shopping_worksheet()
    elif what_to_do_input == "6":
        exit_program()


select_what_to_do()


