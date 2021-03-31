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


# ------------------------------------------------- MENU CLASSES -------------------------------------------------------
# Used for "Story", and every Tutorial option
class Menu_image_sequence:
    def __init__(self, screen, pasta, num_pages, func_link, name):
        self.screen = screen
        self.name = name
        self.background_image = pygame.image.load("images/menu/interfaces/Main/sequence.png")
        self.images_list = [pygame.image.load(f"images/slides/{pasta}/{i+1}.png") for i in range(num_pages)]
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
        if self.current_page > self.num_pages-1:
            self.current_page = self.num_pages-1
        if self.current_page < 0:
            self.current_page = 0

    def get_rectangle(self):
        if self.current_page == self.num_pages-1:
            return 700, 633, 300, 40
        elif self.current_page == 0:
            return 85, 633, 300, 40
        else:
            return 200, 640, 1, 1

    def write_page_number(self):
        page_image = f.create_sized_text(20, 50, str(self.current_page+1), (255, 255, 255))
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


# Used for the Main Menu, Game Menu and Tutorial
class Menu:
    def __init__(self, buttons, directory, screen, user=None):
        self.internal_list = buttons
        self.directory = directory
        self.name = self.directory.split("/")[-1][:-4]
        self.image_nome = pygame.image.load(directory)
        if self.name == "game menu":
            self.effect = [pygame.image.load(f"images/menu/effects/3/{i+1}.png") for i in range(4)]
        else:
            self.effect = [pygame.image.load(f"images/menu/effects/1/{i+1}.png") for i in range(4)]
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0
        self.user = user
        self.coord_effect = (self.internal_list[0].x-12, self.internal_list[0].y-12)

    def draw_buttons(self):
        coordinates = {0: (680, 90), 1: (698, 192), 2: (685, 178)}
        coordinates2 = {0: (687, 90), 1: (687, 90), 2: (687, 192), 3: (687, 178), 4: (687, 178),  5: (687, 178)}
        coordinates3 = {0: (680, 90), 1: (680, 90), 2: (698, 192), 3: (685, 178), 4: (685, 178)}
        ch = {"main menu": coordinates, "game menu": coordinates2, "tutorial": coordinates3}
        co_cho = ch[self.name]
        coo = co_cho[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], self.coord_effect)
        self.screen.blit(pygame.image.load(f"images/menu/info/info_{self.name}/{self.active_code+1}.png"),
                         (coo[0], coo[1]))
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
        if self.active_code > len(self.internal_list)-1:
            self.active_code = 0
        if self.active_code < 0:
            self.active_code = len(self.internal_list)-1
        self.coord_effect = (self.internal_list[self.active_code].x-12, self.internal_list[self.active_code].y-12)

    def refresh(self, background):
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.image_nome, ((1080-470)//2, 0))
        self.screen.blit(pygame.image.load("images/menu/interfaces/navigation/navigation.png"), (355, 620))
        if self.user is not None:
            coo = (20, 490)
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/user_info/level{self.user.level}.png"),
                             (0, 0))
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/records.png"), (coo[0], coo[1]-210))
            self.screen.blit(pygame.image.load(f"images/menu/interfaces/User/parts.png"), (0, coo[1] - 310))
            self.screen.blit(pygame.image.load(f"images/cars/display/{self.user.level}.png"), (coo[0] - 18, coo[1]))
            self.user.draw_text(self.screen)
        self.draw_buttons()
        pygame.display.update()


# Used whenever the user wants to leave the game
class Exit:
    def __init__(self, directory, screen):
        self.image_nome = pygame.image.load(directory)
        self.effects = (True, False)
        self.effect = [pygame.image.load(f"images/Buttons/Effects/1/{i+1}.png") for i in range(4)]
        self.yes_button_image = pygame.image.load(f"images/Buttons/Exit/1.png")
        self.no_button_image = pygame.image.load(f"images/Buttons/Exit/2.png")
        self.active_code = 0
        self.screen = screen
        self.current_frame = 0

    def draw_buttons(self):
        coordinates = {0: (265, 410), 1: (595, 410)}
        coo = coordinates[self.active_code]
        self.screen.blit(self.effect[int(self.current_frame)], coo)
        self.screen.blit(self.yes_button_image, (coordinates[0][0]+13, coordinates[0][1]+10))
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
                    exit("Game Exit")
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
        if self.active_code > len(self.effects)-1:
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
