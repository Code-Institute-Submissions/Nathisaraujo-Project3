import os
import gspread
from google.oauth2.service_account import Credentials
from random import randint
from prettytable import PrettyTable
import time
import sys

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('family_favorites')
recipes = SHEET.worksheet('recipes')

class colors:
    def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
    def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
    def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
    def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
    def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

def initial_page():
    """

    Ask what the user wants to do

    """
    clear_console()

    print("\nWhat would you like to do? \n")
    print("1. Check a recipe")
    print("2. Add a new one\n")
    
    while True:
        user_option = input("Enter your answer here:").strip()
        if user_option == "1":
            prYellow("Ok! Let's check what we have here...\n")
            time.sleep(1.5)
            check_recipe()
        elif user_option == "2":
            prPurple("HMMMM! New recipe coming!\n")
            time.sleep(1.5)
            add_recipe()
        else:
            prRed('Please, enter 1 or 2 to continue.')
            continue

def search_recipe_by_name(recipe_name):    
    recipes = []
    all_rows = SHEET.worksheet("recipes").get_all_values()
    for row in all_rows:
        if recipe_name.lower() in row[0].lower(): 
            recipes.append(row)
    return recipes

def check_recipe():
    clear_console()

    print("How would you like to finde a recipe?\n")
    print("1. View all recipes")
    print("2. Suggestion Recipe")
    print("3. Specific Recipe")
    print("4. Go back to main page.")

    while True:
        user_option = input("Enter your answer here:").strip().lower()
        if user_option == "1":
            all_recipes()
        elif user_option == "2":
            recipe_suggestion()
        elif user_option == "3":
            recipe_by_name()
        elif user_option == "4":
            os.system('clear')
            main()
        elif user_option == "exit":
            exit_program()
        else:
            prRed('Please, enter a valid option to continue.')
            prRed("Or you can enter 'exit' to end the program.")
            continue

def recipe_by_name():
    prPurple("Ok! Enter the recipe name here and we're going to see if we have it!\n")
    recipe_name = input("Check Recipe:")
    found_recipes = search_recipe_by_name(recipe_name)

    headers = ["Name", "Ingredients", "How to make it", "Creator's Name", "Who's Favorite"]

    if found_recipes:
        print(f"Found {len(found_recipes)} matching recipes:")
        recipe_row = found_recipes[0]
        prCyan("\nRecipe Details:")

        tables = PrettyTable()
        tables.field_names = headers
        tables.max_width = 30
        tables.align = "l"

        for row in found_recipes:
            tables.add_row(row)
        print(tables)

        next_move()     
    else:
        prRed("No recipes found with that name.")
        print("Please, choose again.")
        time.sleep(1.5)
        check_recipe()
            
def next_move():
    print("What to do next?")
    print("1. Main page")
    print("2. Exit program")
    user_option = input("Enter here your option:").strip().lower()
    while True:
        if user_option == "1":
            main()
        elif user_option == "2":
            exit_program()

def recipe_suggestion():
    clear_console()

    prPurple("Ok! I think you'll like this one:\n")
    time.sleep(0.8)
    all_recipes = SHEET.worksheet("recipes").get_all_values()         
        
    if len(all_recipes) > 1:
        headers = ["Name", "Ingredients", "How to make it", "Creator's Name", "Who's Favorite"]
        random_index = randint(1, len(all_recipes)-1)  
        random_recipe = all_recipes[random_index - 1]
                
        tables = PrettyTable()
        tables.field_names = headers
        tables.max_width = 30
        tables.align = "l"

        tables.add_row(random_recipe)
        print(tables)

        print("What to do next?")
        print("1. Another recommendation.")
        print("2. Go back to main menu.")
        print("3. Exit the program.")

        while True:
            user_option = input("Enter your answer here:").strip().lower()
            if user_option == "1":
                os.system('clear')
                recipe_suggestion()
            elif user_option == "2":
                os.system('clear')
                main()
            elif user_option == "3":
                exit_program()
            else:
                prRed('Please, enter a valid option to continue.')
                continue

def add_recipe():   
    clear_console()

    prPurple("Ok! Then we'll need you to give us some information...")
    time.sleep(1.0)

    global user_details, recipe_name, ingredients_list, recipe_preparation, recipe_favorite
    
    user_details = input("First name:")
    recipe_name = input("Name of the recipe:")
    ingredients_list = input("What are the ingredients?")
    recipe_preparation = input("How we prepare the recipe?")
    recipe_favorite = input("This recipe is who's favorite?")

    print(f"""
        Your name: {user_details}
        Recipe name: {recipe_name}
        Ingredients List: {ingredients_list}
        Recipe Preparation: {recipe_preparation}
        Recipe Favorite: {recipe_favorite}
        """)
     
    print("Please, make sure you added all information right.\n")
    print("1. Confirm")
    print("2. Edit")
    print("3. Cancel and go to main page")

    while True:
        user_option = input("Enter your answer here:").strip().lower()
        if user_option == "1": 
            confirm_recipe()        
        elif user_option == "2":
            edit_recipe()
        elif user_option == "3":
            clear_console()
            main()
        elif user_option == "exit":
            exit_program()
        else:
            prRed('Please, enter a valid option to continue.')
            prRed("Or you can enter EXIT to go back to the initial menu.")

def edit_recipe():
    global user_details, recipe_name, ingredients_list, recipe_preparation, recipe_favorite

    clear_console()
    prRed("Which information would you like to edit?\n")
    print("1. First name")
    print("2. Recipe name")
    print("3. Ingredients list")
    print("4. Recipe preparation")
    print("5. Recipe favorite")
    print("6. Cancel and go to the main page")

    edit_option = input("Enter your option here:")
    if edit_option == "1":
        user_details = input(f'First name ({user_details}):') or user_details
    elif edit_option == "2":
        recipe_name = input(f'Recipe name ({recipe_name}):') or recipe_name
    elif edit_option == "3":
        ingredients_list = input(f'Ingredients list ({ingredients_list}):') or ingredients_list
    elif edit_option == "4":
        recipe_preparation = input(f'Recipe preparation ({recipe_preparation}):') or recipe_preparation
    elif edit_option == "5":
        recipe_favorite = input(f'Recipe favorite ({recipe_favorite}):') or recipe_favorite
    elif edit_option == "6":
        main()
    else:
        prRed('Please, enter a valid option to continue.')

    print(f"""
        Your name: {user_details}
        Recipe name: {recipe_name}
        Ingredients List: {ingredients_list}
        Recipe Preparation: {recipe_preparation}
        Recipe Favorite: {recipe_favorite}
        """)
        
    prRed("\nPlease, make sure you added all information right.")
    print("1. Confirm")
    print("2. Edit")
    print("3. Cancel and go to main page")

    while True:
        user_option = input("Enter your answer here:").strip().lower()
                        
        if user_option == "1": #volta para 1
            confirm_recipe()
        elif user_option == "2": 
            edit_recipe()

def confirm_recipe():
    data_list = (user_details, recipe_name, ingredients_list, recipe_preparation, recipe_favorite)
    recipes.append_row(data_list)
    prYellow("Loading your information...")
    time.sleep(1.0)
    prGreen("Recipe added.")

    next_move()

def clear_console():
    os.system('clear' if os.name == 'posix' else 'cls')

def exit_program():
    prRed("Exiting the program...")
    time.sleep(1.0)
    sys.exit(0)

def main():
    """
    run all program functions

    """
    print("             FAMILY FAVORITES             ")
    print("\n")
    print("  _____               _ _                  ")
    print(" |  ___|_ _ _ __ ___ (_) |_   _            ")
    print(" | |_ / _` | '_ ` _ \| | | | | |           ")
    print(" |  _| (_| | | | | | | | | |_| |           ")
    print(" |_|  \__,_|_| |_| |_|_|_|\__, |           ")
    print("                          |___/            ")
    print("  _____                     _ _            ")
    print(" |  ___|_ ___   _____  _ __(_) |_ ___  ___ ")
    print(" | |_ / _` \ \ / / _ \| '__| | __/ _ \/ __|")
    print(" |  _| (_| |\ V / (_) | |  | | ||  __/\__ \\")
    print(" |_|  \__,_| \_/ \___/|_|  |_|\__\___||___/")

    prYellow("""\n
              FAMILY FAVORITES 
    is a heartfelt family recipe book where
    we can share our favorite recipes!
    This is a gift to our future generation who will
    be able to prepare the most special recipes.\n
        """)
    input("Press Enter to continue...")
    initial_page()
                                           
main()