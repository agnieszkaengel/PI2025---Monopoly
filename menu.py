import pygame
from dimensions_generator import Dimensions
class Menu:
    def __init__ (self, dim:Dimensions):
        self.width = dim.menu_width
        self.height = dim.menu_width * 0.5
        self.screen_width = dim.screen_width
        self.screen_height = dim.screen_height
        self.menu_left_corner = ((self.screen_width-self.width)//2, (self.screen_height-self.height)*0.7)
        self.title_size = self.width * 0.05
        self.text_size = self.title_size * 0.5
        self.button_size = (self.width * 0.4, self.width * 0.1)
        self.start_pos = (self.menu_left_corner[0] + 0.5 * self.width, self.menu_left_corner[1] + self.title_size * 3)
        self.end_pos = (self.menu_left_corner[0] + 0.5 * self.width, self.menu_left_corner[1] + self.height - self.title_size)
        self.buttons: list [pygame.Rect] = self.create_buttons_list()#[] #[0] - przycisk gra podstawowa, [1] - personalizowana rozgrywka, [2] - przycisk gotowe w menu podstawowej rozgrywki
        self.nick_inboxes: list [pygame.Rect] = [] #[0] i [1] - gracz 1 [nick] i [nr pionka] itd
        self.personalize_inboxes: list[pygame.Rect] = []
        self.users = []
        self.personalize_settings = ['', '', '']
        self.token_errors = [""] * 4
        self.num = 0

    def add_user (self, nick:str, pionek:str):
        self.users.append((nick, pionek))

    def create_users_list(self, num):
        self.num = num
        for i in range(num):
            self.add_user('', '')

    def create_buttons_list(self):
        buttons = []
        buttons.append(pygame.Rect(self.start_pos[0]+self.title_size, self.start_pos[1], self.button_size[0], self.button_size[1])) #gra podstawowa
        buttons.append(pygame.Rect(self.start_pos[0] + self.title_size, self.start_pos[1]+self.button_size[1]*1.5, self.button_size[0], self.button_size[1])) # gra personalizowana
        buttons.append(pygame.Rect(self.start_pos[0]+self.title_size, self.start_pos[1]+self.button_size[1]*2, self.button_size[0], self.button_size[1])) #gotowe w nick menu dla 2os
        buttons.append(pygame.Rect(self.start_pos[0], self.start_pos[1] + self.button_size[1] * 2, self.button_size[0], self.button_size[1]))  # gotowe w menu personalizowanej rozgrywki

        return buttons
    def draw_main_part(self, screen, text, line, state):
        if state == 4:
            pygame.draw.rect(screen, (193, 225, 193),(self.menu_left_corner[0], self.menu_left_corner[1], self.width - 1, self.height * 1.5 - 1))
            pygame.draw.rect(screen, (0, 0, 0),(self.menu_left_corner[0], self.menu_left_corner[1], self.width, self.height * 1.5), 3)
        else:
            pygame.draw.rect(screen, (193, 225, 193),(self.menu_left_corner[0], self.menu_left_corner[1], self.width - 1, self.height - 1))
            pygame.draw.rect(screen, (0, 0, 0),(self.menu_left_corner[0], self.menu_left_corner[1], self.width, self.height), 3)

        image = pygame.image.load("menu.png").convert_alpha()
        im_size = self.height * 1.5
        image = pygame.transform.scale(image, (im_size, im_size))
        image_rect = image.get_rect(center=(self.menu_left_corner[0] + (self.width // 2), self.menu_left_corner[1] - (0.5 * im_size)))
        screen.blit(image, image_rect)

        font = pygame.font.SysFont('Arial', int(self.title_size), True)
        text_color = (0, 0, 0)
        text = font.render(str(text), True, text_color)
        text_rect = text.get_rect(center=(self.menu_left_corner[0] + 0.5 * self.width, self.menu_left_corner[1] + self.title_size))
        screen.blit(text, text_rect)
        if line:
            pygame.draw.line(screen, text_color, self.start_pos, self.end_pos, 3)

    def draw_menu(self, screen):
        self.draw_main_part(screen, "MENU GRY", True, 0)
        self.draw_button(screen, "Gra podstawowa", self.start_pos[0]+self.title_size, self.start_pos[1])
        self.draw_button(screen, "Gra personalizowana", self.start_pos[0] + self.title_size, self.start_pos[1]+self.button_size[1]*1.5)

        image = pygame.image.load("board.png").convert_alpha()
        im_size = self.height * 0.5
        image = pygame.transform.scale(image, (im_size, im_size))
        image_rect = image.get_rect(center=(self.menu_left_corner[0] + (self.width // 4), self.menu_left_corner[1]+0.38*self.menu_left_corner[1]))
        screen.blit(image, image_rect)

    def draw_button(self, screen, text, x, y):

        pygame.draw.rect(screen, (47, 79, 79), (x, y, self.button_size[0], self.button_size[1]))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.button_size[0], self.button_size[1]), 3)

        text_color = (193, 225, 193)
        font = pygame.font.SysFont('Arial', int(self.text_size), True)
        text = font.render(text, True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (x + self.button_size[0] / 2, y + self.button_size[1] / 2)
        screen.blit(text, text_rect)
       # return pygame.Rect(x, y, self.button_size[0], self.button_size[1])

    def draw_nick_menu(self, screen, playersnum, state):
        text_color = (193, 225, 193)
        font = pygame.font.SysFont('Arial', int(self.text_size * 0.9), True)

        self.draw_main_part(screen, "WYBÓR NICKU I PIONKA", False, state)
        self.draw_button(screen, "Gotowe", self.start_pos[0]+self.title_size, self.start_pos[1]+self.button_size[1]*1.7)

        self.draw_image(screen, "pionek1.png", self.start_pos[0]+self.height*0.15, self.start_pos[1]+self.height*0.15)
        self.draw_image(screen, "pionek2.png", self.start_pos[0] + self.height * 0.15 * 2.5, self.start_pos[1] + self.height * 0.15)
        self.draw_image(screen, "pionek3.png", self.start_pos[0] + self.height * 0.15 * 4, self.start_pos[1] + self.height * 0.15)
        self.draw_image(screen, "pionek4.png", self.start_pos[0] + self.height * 0.15 * 5.5, self.start_pos[1] + self.height * 0.15)


        self.nick_inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size-self.button_size[0], self.start_pos[1], 'Gracz 1:', 1))
        self.nick_inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size - self.button_size[0], self.start_pos[1]+self.button_size[1]*0.7, '', 1))
        self.nick_inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size - self.button_size[0], self.start_pos[1]+self.button_size[1]*1.7, 'Gracz 2:', 1))
        self.nick_inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size - self.button_size[0], self.start_pos[1]+self.button_size[1]*2.4, "", 1))

        nick_surface = font.render("Twój nick:", True, text_color)
        screen.blit(nick_surface, (self.nick_inboxes[0].x + 5, self.nick_inboxes[0].y + 5))
        screen.blit(nick_surface, (self.nick_inboxes[2].x + 5, self.nick_inboxes[2].y + 5))
        pionek_surface = font.render("Twój numer pionka:", True, text_color)
        screen.blit(pionek_surface, (self.nick_inboxes[1].x + 5, self.nick_inboxes[1].y + 5))
        screen.blit(pionek_surface, (self.nick_inboxes[3].x + 5, self.nick_inboxes[3].y + 5))

        if playersnum > 2:
            self.nick_inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size-self.button_size[0], self.start_pos[1]+self.button_size[1]*3.4,'Gracz 3:', 1))
            self.nick_inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size-self.button_size[0], self.start_pos[1] + self.button_size[1] * 4.1, '', 1))
            screen.blit(nick_surface, (self.nick_inboxes[4].x + 5, self.nick_inboxes[4].y + 5))
            screen.blit(pionek_surface, (self.nick_inboxes[5].x + 5, self.nick_inboxes[5].y + 5))

            text_surface = font.render(self.users[2][0], True, text_color)
            screen.blit(text_surface, (self.nick_inboxes[4].x + nick_surface.get_width() * 1.2, self.nick_inboxes[4].y + 5))  # nick gracza 3
            text_surface = font.render(self.users[2][1], True, text_color)
            screen.blit(text_surface, (self.nick_inboxes[5].x + pionek_surface.get_width() * 1.1, self.nick_inboxes[5].y + 5))  # pionek gracza 3

        if playersnum > 3:
            self.nick_inboxes.append(self.draw_inbox(screen, self.start_pos[0] + self.title_size, self.start_pos[1] + self.button_size[1] * 3.4, 'Gracz 4:', 1))
            self.nick_inboxes.append(self.draw_inbox(screen, self.start_pos[0] + self.title_size, self.start_pos[1] + self.button_size[1] * 4.1, "", 1))
            screen.blit(nick_surface, (self.nick_inboxes[6].x + 5, self.nick_inboxes[6].y + 5))
            screen.blit(pionek_surface, (self.nick_inboxes[7].x + 5, self.nick_inboxes[7].y + 5))

            text_surface = font.render(self.users[3][0], True, text_color)
            screen.blit(text_surface, (self.nick_inboxes[6].x + nick_surface.get_width() * 1.2, self.nick_inboxes[6].y + 5))  # nick gracza 4
            text_surface = font.render(self.users[3][1], True, text_color)
            screen.blit(text_surface, (self.nick_inboxes[7].x + pionek_surface.get_width() * 1.1, self.nick_inboxes[7].y + 5))  # pionek gracza 4

        text_surface = font.render(self.users[0][0], True, text_color)
        screen.blit(text_surface, (self.nick_inboxes[0].x+nick_surface.get_width()*1.2, self.nick_inboxes[0].y + 5)) #nick gracza 1
        text_surface = font.render(self.users[0][1], True, text_color)
        screen.blit(text_surface,(self.nick_inboxes[1].x + pionek_surface.get_width() * 1.1, self.nick_inboxes[1].y + 5)) #pionek gracza 1


        text_surface = font.render(self.users[1][0], True, text_color)
        screen.blit(text_surface, (self.nick_inboxes[2].x+nick_surface.get_width()*1.2, self.nick_inboxes[2].y + 5)) #nick gracza 2
        text_surface = font.render(self.users[1][1], True, text_color)
        screen.blit(text_surface, (self.nick_inboxes[3].x + pionek_surface.get_width() * 1.1, self.nick_inboxes[3].y + 5))#pionek gracza 2


        if hasattr(self, "token_errors"):
            for i in range(playersnum):
                if i in self.token_errors:
                    error_surface = font.render(self.token_errors[i], True, (255, 0, 0))  # Czerwony kolor błędu
                    screen.blit(error_surface, (self.nick_inboxes[i * 2+1].x + self.button_size[0], self.nick_inboxes[i * 2+1].y))

    def draw_image(self, screen, name, x, y):
        image = pygame.image.load(name).convert_alpha()
        im_size = self.height * 0.15
        image = pygame.transform.scale(image, (im_size, im_size))
        image_rect = image.get_rect(center=(x,y))
        screen.blit(image, image_rect)

    def handle_event(self, event, inbox_number, player):
        if event.type == pygame.KEYDOWN:
            if inbox_number%2 == 0:
                if event.key == pygame.K_BACKSPACE:
                    self.users[player] = (self.users[player][0][:-1], self.users[player][1])
                else:
                    self.users[player] = (self.users[player][0] + event.unicode, self.users[player][1])
            else:
                if event.key == pygame.K_BACKSPACE:
                    self.users[player] = (self.users[player][0], self.users[player][1][:-1])
                else:
                    self.users[player] = (self.users[player][0], self.users[player][1] + event.unicode)



    def draw_inbox(self, screen, x, y, text, size):
        pygame.draw.rect(screen, (47, 79, 79), (x, y, self.button_size[0]*size, self.button_size[1]//2))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.button_size[0]*size, self.button_size[1]//2), 3)

        text_color = (47, 79, 79)
        font = pygame.font.SysFont('Arial', int(self.text_size), True)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x+self.title_size, y - self.text_size)
        screen.blit(text_surface, text_rect)
        return pygame.Rect(x, y, self.button_size[0]*size, self.button_size[1]//2)

    def personalize_game_menu(self, screen):
        self.draw_main_part(screen, "WYBIERZ OPCJE ROZGRYWKI", False, 3)
        self.personalize_inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.button_size[0], self.start_pos[1], "", 2))
        self.personalize_inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.button_size[0], self.start_pos[1] + self.button_size[1] * 0.7, '', 2))
        self.personalize_inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.button_size[0], self.start_pos[1] + self.button_size[1] * 1.4, '', 2))

        text_color = (193, 225, 193)
        font = pygame.font.SysFont('Arial', int(self.text_size * 0.9), True)

        lgr_surface = font.render("Podaj liczbę graczy: ", True, text_color)
        screen.blit(lgr_surface, (self.personalize_inboxes[0].x + 5, self.personalize_inboxes[0].y + 5))

        mgr_surface = font.render("Podaj kwotę początkową majątku graczy: ", True, text_color)
        screen.blit(mgr_surface, (self.personalize_inboxes[1].x + 5, self.personalize_inboxes[1].y + 5))

        sgr_surface = font.render("Podaj kwotą dodawaną przy przejściu pola START: ", True, text_color)
        screen.blit(sgr_surface, (self.personalize_inboxes[2].x + 5, self.personalize_inboxes[2].y + 5))

        self.draw_button(screen, "Gotowe", self.start_pos[0], self.start_pos[1] + self.button_size[1] * 2)

        text_surface = font.render(self.personalize_settings[0], True, text_color)
        screen.blit(text_surface, (self.personalize_inboxes[0].x + lgr_surface.get_width() * 1.1, self.personalize_inboxes[0].y + 5))  # liczba graczy

        text_surface = font.render(self.personalize_settings[1], True, text_color)
        screen.blit(text_surface, (self.personalize_inboxes[1].x + mgr_surface.get_width() * 1.05, self.personalize_inboxes[1].y + 5))  # kwota poczatkowa majatku

        text_surface = font.render(self.personalize_settings[2], True, text_color)
        screen.blit(text_surface, (self.personalize_inboxes[2].x + sgr_surface.get_width() * 1.05,self.personalize_inboxes[2].y + 5))  # kwota przy przejsciu

        if hasattr(self, "input_errors"):
            font = pygame.font.SysFont('Arial', int(self.text_size * 0.8), True)
            for i, msg in self.input_errors.items():
                error_surface = font.render(msg, True, (255, 0, 0))
                inbox_rect = self.personalize_inboxes[i]
                screen.blit(error_surface, (inbox_rect.x, inbox_rect.y + inbox_rect.height - 1))

    def handle_personalize_settings(self, event, inbox):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.personalize_settings[inbox] = self.personalize_settings[inbox][:-1]
            else:
                self.personalize_settings[inbox] = self.personalize_settings[inbox] + event.unicode

    def validate_tokens(self):
        self.token_errors = {}
        chosen = []
        valid = True

        for i in range(self.num):
            token = self.users[i][1]
            print(f"Checking token at index {i}: '{token}'")
            if not token.isdigit() or not (1 <= int(token) <= 4):
                print(f"Token '{token}' invalid")
                self.token_errors[i] = "1–4"
                valid = False
            elif token in chosen:
                print(f"Token '{token}' already chosen")
                self.token_errors[i] = "Zajęty"
                valid = False
            else:
                chosen.append(token)

        return valid

    def validate_personalization_inputs(self):
        self.input_errors = {}
        valid = True

        # Liczba graczy
        players_input = self.personalize_settings[0]
        print(f"Checking number of players: '{players_input}'")
        if not players_input.isdigit():
            print("Invalid: not a number")
            self.input_errors[0] = "Musi być liczbą całkowitą"
            valid = False
        else:
            players = int(players_input)
            if players < 2 or players > 4:
                print("Invalid: out of range (2–4)")
                self.input_errors[0] = "Dozwolone 2–4"
                valid = False

        # Kwota początkowa
        start_money_input = self.personalize_settings[1]
        print(f"Checking starting money: '{start_money_input}'")
        if not start_money_input.isdigit():
            print("Invalid: not a number")
            self.input_errors[1] = "Musi być liczbą"
            valid = False
        elif int(start_money_input) < 0:
            print("Invalid: negative number")
            self.input_errors[1] = "Nie może być ujemna"
            valid = False

        # Kwota za przejście START
        pass_start_input = self.personalize_settings[2]
        print(f"Checking pass start bonus: '{pass_start_input}'")
        if not pass_start_input.isdigit():
            print("Invalid: not a number")
            self.input_errors[2] = "Musi być liczbą"
            valid = False
        elif int(pass_start_input) < 0:
            print("Invalid: negative number")
            self.input_errors[2] = "Nie może być ujemna"
            valid = False

        return valid

