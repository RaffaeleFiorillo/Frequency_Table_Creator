# This module contains all the functions called by the main module.
# Al the functions take the screen where the images are going to be displayed as a parameter
# For each of the functions there is a correspondent class that manages the functionality of the function
# Each function in this module returns values that correspond to the functionality that the game should open next
# A function's comment in this module has a description and the functions it can lead to when it finishes
# This module is divided in categories like: --- CATEGORY NAME --- ; in order to make it more understandable

# -------------------------------------------- IMPORTS -----------------------------------------------------------------
import menu_classes as mc
import hard_work as hw
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


def display_table_standard(screen):
    hw.do_the_work_standard()
    data = f.prepare_table_data_standard()
    td = mc.Table_Display(screen, data)
    td.display_menu()
    return "new_table"


def display_table_custom(screen):
    # hw.do_the_work_customized()
    # here you create all the initialization values for the class that will display the table
    f.wait(1)
    return "new_table"


def create_table(screen):
    x_value = (1150 - 260) // 2
    exit_button = mc.Button(x_value+55, 650, "images/Buttons/Create_Table/exit.png", "exit1", 3)
    create_button2 = mc.Button(x_value, 550, "images/Buttons/Create_Table/create_2.png", "create2", 2)
    create_button1 = mc.Button(x_value, 450, "images/Buttons/Create_Table/create_1.png", "create1", 1)
    buttons_tc = [create_button1, create_button2, exit_button]
    tc = mc.Table_Creator(buttons_tc, screen)
    next_link = tc.display_menu()
    return next_link


# activated when a user wants to exit the program, leads to finish the program's execution or Main Menu
def exit_program(screen):
    # f.play(exit_sound)
    if mc.Exit("images/Menu/exit_menu.png", screen).display_menu():
        f.terminate_execution()
    return "main_menu"
