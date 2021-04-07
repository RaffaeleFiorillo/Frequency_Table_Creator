# This module contains all the functions called by the main module.
# Al the functions take the screen where the images are going to be displayed as a parameter
# For each of the functions there is a correspondent class that manages the functionality of the function
# Each function in this module returns values that correspond to the functionality that the game should open next
# A function's comment in this module has a description and the functions it can lead to when it finishes
# This module is divided in categories like: --- CATEGORY NAME --- ; in order to make it more understandable

# -------------------------------------------- IMPORTS -----------------------------------------------------------------
import menu_classes as mc
import functions as f


# ------------------------------------------ START INTERFACE -----------------------------------------------------------
# this is the first interface the user sees when he opens the game
def start_page(screen):
    start = mc.Start(screen)
    # f.play(start_sound)
    output = start.display_menu()
    if output:
        return "main_menu"
    return False


# ------------------------------------------- MAIN MENU ----------------------------------------------------------------
# display and manage the Main Menu, leads to the Choose User Menu, New Game Menu or Exit Game Menu
def main_menu(screen):
    # f.stop_all_sounds()
    # f.play(change_menu_sound)
    position_x_main = (1150 - 260) // 2
    position_y_main = [y for y in range(150, 600, 150)]
    effects_main = ["new_table", "tutorial", "exit1"]
    buttons_main = [mc.Button(position_x_main, y, f"images/Buttons/Main/{position_y_main.index(y) + 1}.png",
                              effects_main[position_y_main.index(y)], position_y_main.index(y)) for y in
                    position_y_main[:len(effects_main)]]
    m_m = mc.Menu(buttons_main, f"images/Menu/main_menu.png", screen)
    return m_m.display_menu()


def tutorial():
    pass


def display_table():
    pass


def create_table(screen):
    exit_button = mc.Button(995, 675, "images/Buttons/Create_Table/exit.png", "exit_2", 2)
    create_button = mc.Button((1150 - 260) // 2, 500, "images/Buttons/Create_Table/create.png", "create", 1)
    buttons_tc = [create_button, exit_button]
    tc = mc.Table_Creator(buttons_tc, screen)
    tc.display_menu()
    return "main_menu"


# activated when a user wants to exit the program, leads to finish the program's execution or Main Menu
def exit_program(screen):
    # f.play(exit_sound)
    if mc.Exit("images/Menu/exit_menu.png", screen).display_menu():
        f.terminate_execution()
    return "main_menu"
