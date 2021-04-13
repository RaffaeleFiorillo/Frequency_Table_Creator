# This module contains functions that are used by all the others modules
# -------------------------------------------- IMPORTS -----------------------------------------------------------------
import pygame
from os import walk, mkdir, system
from sys import exit as exit_2
from sys import platform
from random import choice as random_choice, randint as random_randint, random as random_random

# ---------------------------------------- GLOBAL VARIABLES ------------------------------------------------------------
pygame.mixer.init()


# ------------------------------------- REIMPLEMENTED FUNCTIONS --------------------------------------------------------
# These functions are just a reimplementation of existing python packages. They are useful because other modules of this
# game don't need to import the module random or time (etc.), just this module functions.

def choice(list_r):
    return random_choice(list_r)


def randint(first_number, last_number):
    return random_randint(first_number, last_number)


def random():
    return random_random()


def wait(seconds):
    pygame.time.wait(seconds * 1000)


def terminate_execution():
    exit_2()


# uses the pygame module to load a sound to memory and returns it
def load_sound(location):
    return pygame.mixer.Sound(f"sounds/{location}")


# plays a sound passed as argument
def play(sound: pygame.mixer.Sound):
    volume = get_sound_volume()
    sound.set_volume(volume)
    sound.play()


"""def play_music():
    sound = music_sound
    volume = get_music_volume()
    sound.set_volume(volume)
    sound.play(-1)"""

"""def music_fade_out():
    music_sound.fadeout(2)"""


# stops all currently playing sounds
def stop_all_sounds():
    pygame.mixer.stop()


# ------------------------------------------ SOUNDS --------------------------------------------------------------------
# error_sound = load_sound("menu/error_message2.WAV")  # sound for every time an error occurs
# success_sound = load_sound("menu/success.WAV")       # sound for every time a success occurs
# music_sound = load_sound("game/music.WAV")


# -------------------------------------------- MENU FUNCTIONS ----------------------------------------------------------
def get_sound_volume():
    file = open("saves/active_user.txt", "r")
    line = file.readline().split(" ")
    file.close()
    if len(line) != 1:
        return float(line[7]) / 10
    else:
        return 1.0


def get_music_volume():
    file = open("saves/active_user.txt", "r")
    line = file.readline().split(" ")
    file.close()
    if len(line) != 1:
        return float(line[6]) / 20.0
    else:
        return 0.5


def create_folder(nome_user):
    mkdir("" + nome_user)


# returns a list with all the usernames currently existing, but only on windows, linux and Mac OS
def list_users():
    return list(walk("saves"))[0][1]


# returns a list with all the names of the texts that the user will type in the matches
def get_text_names():
    texts = walk("texts")
    texts = [text for text in texts][0][1:][1][:-1]
    return texts[:-1]


# return a text image that fits into a set size, with some customizations (like color and font size)
def create_sized_text(max_size_image, max_size_letter, text, color, min_size_letter=30):
    pygame.font.init()
    rendered_text = None
    for i in range(min_size_letter, max_size_letter)[::-1]:
        text_font = pygame.font.SysFont('Times New Roman', i)
        text_font.set_bold(True)
        rendered_text = text_font.render(text, True, color)
        if rendered_text.get_size()[0] <= max_size_image:
            break
    return rendered_text


def clean_screen():
    if platform == "linux" or platform == "linux2":
        system("clear")
    elif platform == "win32":
        system("cls")


def get_elements(text):
    return [elem for elem in text if elem != ""]


def render_texts(text):
    text = get_elements(text.split(" "))
    lines = [""]
    for element in text:
        line_plus_element = lines[-1] + element
        if len(line_plus_element) < 84:
            lines[-1] = line_plus_element.strip()+" "
        else:
            lines[-1]= lines[-1].strip()
            lines.append(element.strip()+" ")
    rendered_lines = [create_sized_text(700, 20, line, (255, 255, 255), 15) for line in lines]
    elements = get_elements(text)
    return rendered_lines, elements


def prepare_table_data_standard():
    with open("data.txt", "r") as file:
        data = file.readlines()
    line1 = [dat for dat in data[0].split(" ")[:-1] if dat != "" and dat != "\n"]
    line2 = [dat for dat in data[1].split(" ")[:-1] if dat != ""]
    table = [line.split(" ") for line in data[2:]]
    return [line1, line2, table]


def create_line_1_image(line1):
    new_line = "Rol of the sample: " + " ".join(line1)
    return create_sized_text(1000, 21, new_line, (255, 255, 255), 12)


"""values = ["1", " ", "2", " ", "3", " ", "4", " ", "5", " ", "6", " ", "7", " ", "8", " ", "9"]
text = "".join([choice(values) for _ in range(200)])
print(render_texts(text))"""
