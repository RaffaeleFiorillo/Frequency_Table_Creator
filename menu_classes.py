# This module contains all the classes responsible for displaying and managing all the Menus and interfaces available
# In the Game. There are also some classes that makes it easier for all the menu classes to do their job.
# Every menu class has three major methods that are very similar if not the same: - display_menu(); - manage_buttons();
# - refresh(); display_menu is the one called after instantiating a new object of a menu class, it is the only method
# used externally of the class. It is the most important, and his job is to display the events of a menu.
# The manage_buttons method is for transforming input from the keyboard into the correct output. And the refresh method
# just updates the menu after every alteration the user makes.

# -------------------------------------------------- IMPORTS -----------------------------------------------------------
import pygame
import functions as f


# --------------------------------------------------- SOUNDS ----------------------------------------------------------
# button_y_sound = f.load_sound("menu/button_activation.WAV")     # sound for changing button on y axis
# button_x_sound = f.load_sound("menu/button_lateral.WAV")        # sound for changing button on x axis
# volume_change_sound = f.load_sound("menu/volume_change.WAV")    # sound for changing volume
# erase_letter_sound = f.load_sound("menu/typing.WAV")            # sound for every time a letter is erased
# error_sound = f.load_sound("menu/error_message2.WAV")           # sound for every time an error occurs
# success_sound = f.load_sound("menu/success.WAV")                # sound for every time a success occurs


# ------------------------------------------------ SUPPORT CLASSES -----------------------------------------------------
class Button:
    def __init__(self, x, y, directory, effect, code):
        self.x = x
        self.y = y
        self.image = pygame.image.load(directory)
        self.effect = effect
        self.code = code

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def change_image(self, directory):
        self.image = pygame.image.load(directory)


class Text_Box:
    text = ""
    last_character = ""
    elements_number = 0
    elements = []

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return " ".join(self.elements)

    def display_box(self, screen):
        adjust, precision = 0, 15
        unity = 255 // precision
        for i in range(precision):
            rgb = unity * i
            color, x, y = (rgb, rgb, rgb), self.x + adjust, self.y + adjust
            w, h = self.width - adjust * 2, self.height - adjust * 2
            pygame.draw.rect(screen, color, (x, y, w, h), 7 - i, 1, 1)
            adjust += 6 - i

    def display_text(self, screen):
        rendered_texts, self.elements = f.render_texts(self.text)
        self.elements_number = len(self.elements)
        coordinates = [(self.x + 30, self.y + 30 + i * 30) for i in range(len(rendered_texts))]
        for text, coo in zip(rendered_texts, coordinates):
            screen.blit(text, coo)

    def draw(self, screen):
        self.display_box(screen)
        self.display_text(screen)


# ------------------------------------------------- MENU CLASSES -------------------------------------------------------
# Used for "Story", and every Tutorial option
class Menu_image_sequence:
    def __init__(self, screen, pasta, num_pages, func_link, name):
        self.screen = screen
        self.name = name
        self.background_image = pygame.image.load("images/menu/interfaces/Main/sequence.png")
        self.images_list = [pygame.image.load(f"images/slides/{pasta}/{i + 1}.png") for i in range(num_pages)]
        self.slide_name = pygame.image.load(f"images/slides/{pasta}/name.png")
        self.num_pages = num_pages
        self.current_page = 0
        self.origin_link = func_link

    def manage_buttons(self, keys):
        if keys[pygame.K_RIGHT]:
            """if self.current_page+1 == self.num_pages:
                f.play(error_sound)
            else:
                f.play(button_y_sound)"""
            self.current_page += 1
        elif keys[pygame.K_LEFT]:
            """if self.current_page == 0:
                f.play(error_sound)
            else:
                f.play(button_y_sound)"""
            self.current_page -= 1
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            if self.current_page == self.num_pages:
                return self.origin_link
        elif keys[pygame.K_ESCAPE]:
            return self.origin_link
        if self.current_page > self.num_pages - 1:
            self.current_page = self.num_pages - 1
        if self.current_page < 0:
            self.current_page = 0

    def get_rectangle(self):
        if self.current_page == self.num_pages - 1:
            return 700, 633, 300, 40
        elif self.current_page == 0:
            return 85, 633, 300, 40
        else:
            return 200, 640, 1, 1

    def write_page_number(self):
        page_image = f.create_sized_text(20, 50, str(self.current_page + 1), (255, 255, 255))
        self.screen.blit(page_image, (515, 640))

    def refresh(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.images_list[self.current_page], (108, 120))
        self.screen.blit(self.slide_name, (400, 0))
        self.write_page_number()
        pygame.draw.rect(self.screen, (0, 0, 0), self.get_rectangle())
        pygame.display.update()

    def display_menu(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(pygame.key.get_pressed())
                    if effect is not None:
                        return effect
            self.refresh()


# Used for the Main Menu
class Menu:
    def __init__(self, buttons, directory, screen):
        self.internal_list = buttons
        self.directory = directory
        self.name = self.directory.split("/")[-1][:-4]
        self.image_nome = pygame.image.load(directory)
        self.effect = [pygame.image.load(f"images/Buttons/Effects/Main/{i + 1}.png") for i in range(4)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0
        self.coord_effect = (self.internal_list[0].x - 12, self.internal_list[0].y - 12)

    def draw_buttons(self):
        # coordinates = {0: (680, 90), 1: (698, 192), 2: (685, 178)}
        self.screen.blit(self.effect[int(self.current_frame)], self.coord_effect)
        """self.screen.blit(pygame.image.load(f"images/menu/info/info_{self.name}/{self.active_code+1}.png"),
                         (coordinates[0], coordinates[1]))"""
        for but in self.internal_list:
            but.draw(self.screen)
        self.current_frame += 0.25
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(pygame.key.get_pressed())
                    if effect is not None:
                        return effect
            self.refresh(background)

    def manage_buttons(self, keys):
        valor = 0
        if keys[pygame.K_UP]:
            # f.play(button_y_sound)
            valor = -1
        elif keys[pygame.K_DOWN]:
            # f.play(button_y_sound)
            valor = 1
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            return self.internal_list[self.active_code].effect
        self.active_code += valor
        if self.active_code > len(self.internal_list) - 1:
            self.active_code = 0
        if self.active_code < 0:
            self.active_code = len(self.internal_list) - 1
        self.coord_effect = (self.internal_list[self.active_code].x - 12, self.internal_list[self.active_code].y - 12)

    def refresh(self, background):
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.image_nome, (0, 0))
        # self.screen.blit(pygame.image.load("images/Buttons/Effects/Main/"), (355, 620))
        self.draw_buttons()
        pygame.display.update()


# Used whenever the user wants to leave the program
class Exit:
    def __init__(self, directory, screen):
        self.image_nome = pygame.image.load(directory)
        self.effects = (True, False)
        self.effect = [pygame.image.load(f"images/Buttons/Effects/Exit/{i + 1}.png") for i in range(4)]
        self.yes_button_image = pygame.image.load(f"images/Buttons/Exit/1.png")
        self.no_button_image = pygame.image.load(f"images/Buttons/Exit/2.png")
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0

    def draw_buttons(self):
        coordinates = {0: (265, 410), 1: (595, 410)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], coo)
        self.screen.blit(self.yes_button_image, (coordinates[0][0] + 13, coordinates[0][1] + 10))
        self.screen.blit(self.no_button_image, (coordinates[1][0] + 13, coordinates[1][1] + 10))
        self.current_frame += 0.25
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    f.terminate_execution()
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(pygame.key.get_pressed())
                    if effect is not None:
                        return effect
            self.refresh()

    def manage_buttons(self, keys):
        valor = 0
        if keys[pygame.K_RIGHT]:
            # f.play(button_x_sound)
            valor = 1
        elif keys[pygame.K_LEFT]:
            # f.play(button_x_sound)
            valor = -1
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            return self.effects[self.active_code]
        self.active_code += valor
        if self.active_code > len(self.effects) - 1:
            self.active_code = 0
        if self.active_code < 0:
            self.active_code = 1

    def refresh(self):
        self.screen.blit(self.image_nome, (0, 0))
        self.draw_buttons()
        # self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation2.png"), (350, 600))
        pygame.display.update()


# The first Interface that shows up when the game is executed. It shows "Frequency Table Creator"'s logo
class Start:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/Menu/start_menu.png")
        self.time = 0

    def show_directives(self):
        if int(self.time) % 2 == 0:
            text_font = pygame.font.SysFont('Times New Roman', 20)
            text_font.set_bold(True)
            self.screen.blit(text_font.render("Press any key to continue", True, (255, 255, 255)), (450, 670))

    def display_menu(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            self.time += clock.tick(30) / 990
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    return True
            self.refresh()

    def refresh(self):
        self.screen.blit(self.image, (0, 0))
        self.show_directives()
        pygame.display.update()


class Table_Creator:
    effect = []
    current_frame = 0
    image_name = pygame.image.load("images/Menu/table_creator_menu.png")
    active_code = 0
    text_box = Text_Box(200, 50, 760, 300)
    info_text_image = f.create_sized_text(100, 21, "You can start typing the sample. It will be shown in this box.",
                                          (0, 0, 0), 20)

    def __init__(self, buttons, screen):
        self.internal_list = buttons
        self.screen = screen
        self.coord_effect = (self.internal_list[0].x - 12, self.internal_list[0].y - 12)
        self.effect.append([pygame.image.load(f"images/Buttons/Effects/Main/{i + 1}.png") for i in range(4)])
        self.effect.append([pygame.image.load(f"images/Buttons/Effects/Other/{i + 1}.png") for i in range(4)])

    def draw_buttons(self):
        effect_code = 0
        if self.active_code == 2:
            effect_code = 1
        self.screen.blit(self.effect[effect_code][int(self.current_frame)], self.coord_effect)
        for button in self.internal_list:
            button.draw(self.screen)
        self.current_frame += 0.25
        if self.current_frame > 3:
            self.current_frame = 0

    def display_menu(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    effect = self.manage_buttons(pygame.key.get_pressed(), event)
                    if effect is not None:
                        if effect == "create":
                            self.save_data()
                        return effect
            self.refresh()

    def save_data(self):
        file = open("data.txt", "w")
        file.write(str(self.text_box))
        file.close()

    def manage_buttons(self, keys, event):
        valor = 0
        if keys[pygame.K_UP]:
            # f.play(button_y_sound)
            valor = -1
        elif keys[pygame.K_DOWN]:
            # f.play(button_y_sound)
            valor = 1
        elif keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            return self.internal_list[self.active_code].effect
        if event.key == pygame.K_BACKSPACE:
            # f.play(erase_letter_sound)
            self.text_box.text = self.text_box.text[:-1]
        elif event.unicode.isdigit() or event.unicode == " ":
            if self.text_box.last_character != " ":
                self.text_box.text += event.unicode
                self.text_box.last_character = event.unicode
            else:
                if event.unicode != " ":
                    self.text_box.text += event.unicode
                    self.text_box.last_character = event.unicode

        self.active_code += valor
        if self.active_code > len(self.internal_list) - 1:
            self.active_code = 0
        if self.active_code < 0:
            self.active_code = len(self.internal_list) - 1
        self.coord_effect = (self.internal_list[self.active_code].x - 12, self.internal_list[self.active_code].y - 12)

    def display_info(self):
        text = f"Current element number: {self.text_box.elements_number}"
        image_text = f.create_sized_text(250, 21, text, (0, 0, 0), 20)
        self.screen.blit(image_text, (445, 400))
        if not self.text_box.elements_number:
            self.screen.blit(self.info_text_image, (270, 200))

    def refresh(self):
        self.screen.blit(self.image_name, (0, 0))
        self.text_box.draw(self.screen)
        self.display_info()
        self.draw_buttons()
        pygame.display.update()


class Table_Display:
    info_text_image = f.create_sized_text(100, 21, "Press any button to continue", (0, 0, 0), 20)
    image_name = pygame.image.load("images/Menu/table_creator_menu.png")
    coordinates = []

    def __init__(self, screen, data):
        self.screen = screen
        self.line1 = f.create_line_1_image(data[0])
        self.line2 = f.create_line_2_image(data[1])
        self.column_sizes, self.table = f.create_table_images(data[2])

    def display_menu(self):
        clock = pygame.time.Clock()
        keepGoing = True
        while keepGoing:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    return "new_table"
            self.refresh()

    def draw_table(self):
        max_line_length = sum([element[0] for element in self.column_sizes])
        for i in range(len(self.table)):
            self.screen.blit(self.table[i], (35, 185+25*i))
        f.draw_table_lines(self.screen, len(self.table), max_line_length)
        # f.fill_table(self.table)

    def draw_lable(self):
        ss, aa = f.get_tables_lables()
        pygame.draw.line(self.screen, (0, 0, 0), (20, 160), (1110, 160), 2)
        x = 20
        for s, a in zip(ss, aa):
            self.screen.blit(a, (x, 160))
            x+= s[0]
        pygame.draw.line(self.screen, (0, 0, 0), (20, 185), (1110, 185), 2)

    def refresh(self):
        self.screen.blit(self.image_name, (0, 0))
        # self.display_titles()
        self.screen.blit(self.line1, (30, 60))
        pygame.draw.line(self.screen, (100, 100, 100), (25, 83), (1125, 83), 2)
        self.screen.blit(self.line2[0], (30, 90))
        pygame.draw.line(self.screen, (100, 100, 100), (25, 113), (1125, 113), 2)
        self.screen.blit(self.line2[1], (30, 115))
        pygame.draw.line(self.screen, (100, 100, 100), (25, 140), (1125, 140), 2)
        self.draw_lable()
        self.draw_table()
        pygame.display.update()
