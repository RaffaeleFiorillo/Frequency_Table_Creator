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


def reshape_into_class(part1, part2):
    return f"{part1[1:-1]} |- {part2[:-1]}"


def reshape_into_fraction(nominator, denominator):
    return f"{nominator[1:-1]}/{denominator[:-1]}"


def reshape_table_lines(table):
    new_table = []
    for line in table:
        new_line = []
        for i in range(len(line)):
            if i == 0:
                new_line.append(reshape_into_class(line[0], line[1]))
            elif i in [1, 4, 8]:
                continue
            elif i == 3:
                new_line.append(reshape_into_fraction(line[3], line[4]))
            else:
                new_line.append(line[i])
        new_table.append(new_line)
    return new_table


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


def get_table_line_images(lines):
    line_sizes, lines_images = [], []
    for line in lines:
        sizes = []
        for element in line:
            image = create_sized_text(50, 21, f" {element} ", (0, 0, 0), 18)
            sizes.append(image.get_size())
        lines_images.append(create_sized_text(50, 21, " "+"  ".join(line)+" ", (0, 0, 0), 20))
        line_sizes.append(sizes)
    columns_max_sizes = [max([line_sizes[i][y] for i in range(len(line_sizes[0]))]) for y in range(len(line_sizes))]
    return columns_max_sizes, lines_images


def prepare_table_data_standard():
    with open("data.txt", "r") as file:
        data = file.readlines()
    line1 = [dat for dat in data[0].split(" ")[:-1] if dat != "" and dat != "\n"]
    line2 = [dat for dat in data[1].split(" ")[:-1] if dat != ""]
    table = [line.split(" ") for line in data[2:]]
    return [line1, line2, table]


def create_line_1_image(line1):
    new_line = "Rol of the sample: " + "; ".join(line1)
    return create_sized_text(1100, 21, new_line, (0, 0, 0), 12)


def create_line_2_image(line2):
    new_line = []
    for i in range(len(line2)):
        if i not in [6, 7]:
            new_line.append(line2[i])
        elif i == 6:
            new_line.append(reshape_into_class(line2[6], line2[7]))
    line2_1, line2_2 = new_line[:4], new_line[4:]
    elements = ["Total Amplitude", "Class Amplitude", "Sample Size", "Class Number", "Media", "Mode", "Mode Class",
                "Median", "Variance", "Standard Deviation"]
    content1 = [f"{elements[i]}: {line2_1[i]} | " for i in range(len(line2_1))]
    content2 = [f"{elements[i+4]}: {line2_2[i]} | " for i in range(len(line2_2))]
    content1 = create_sized_text(1100, 21, "".join(content1), (0, 0, 0), 12)
    content2 = create_sized_text(1100, 21, "".join(content2), (0, 0, 0), 12)
    return content1, content2


def create_table_images(table):
    table = reshape_table_lines(table)
    columns_max_sizes, lines_images = get_table_line_images(table)
    return columns_max_sizes, lines_images


def draw_table_lines(screen, lines_number, max_line_length):
    color, s_x, s_y, advance = (0, 0, 0), 35, 160, 25
    for _ in range(lines_number):
        pygame.draw.line(screen, color, (s_x, s_y+advance), (s_x+max_line_length, s_y+advance), 1)


def get_tables_lables():
    words = ["   Class   ", "Absolute Frequency", "Relative Frequency", "Relative Frequency Percentage",
             "Cumulative Frequency", "Cumulative Frequency Percentage"]
    size_image, images, sizes = [], [], [110, 150, 150, 150, 200, 150, 200]
    for word in words:
        image = create_sized_text(sizes[words.index(word)], 20, f" {word} ", (0, 0, 0), 15)
        images.append(image)
        size_image.append(image.get_size())
    return size_image, images


