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
        self.inboxes: list [pygame.Rect] = [] #[0] i [1] - gracz 1 [nick] i [nr pionka] itd
        self.users = []

    def add_user (self, nick:str, pionek:str):
        self.users.append((nick, pionek))

    def create_users_list(self, num):
        for i in range(num):
            self.add_user('', '')

    def create_buttons_list(self):
        buttons = []
        buttons.append(pygame.Rect(self.start_pos[0]+self.title_size, self.start_pos[1], self.button_size[0], self.button_size[1]))
        buttons.append(pygame.Rect(self.start_pos[0] + self.title_size, self.start_pos[1]+self.button_size[1]*1.5, self.button_size[0], self.button_size[1]))
        buttons.append(pygame.Rect(self.start_pos[0]+self.title_size, self.start_pos[1]+self.button_size[1]*2, self.button_size[0], self.button_size[1]))
        return buttons
    def draw_main_part(self, screen, text):
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
        pygame.draw.line(screen, text_color, self.start_pos, self.end_pos, 3)

    def draw_menu(self, screen):
        self.draw_main_part(screen, "MENU GRY")
        self.draw_button(screen, "Gra podstawowa", self.start_pos[0]+self.title_size, self.start_pos[1])
        self.draw_button(screen, "Gra personalizowana", self.start_pos[0] + self.title_size, self.start_pos[1]+self.button_size[1]*1.5)

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

    def draw_nick_menu(self, screen):
        self.draw_main_part(screen, "WYBÓR NICKU I PIONKA")
        self.draw_button(screen, "Gotowe", self.start_pos[0]+self.title_size, self.start_pos[1]+self.button_size[1]*2)

        self.draw_image(screen, "pionek1.png", self.start_pos[0]+self.height*0.15, self.start_pos[1]+self.height*0.15)
        self.draw_image(screen, "pionek2.png", self.start_pos[0] + self.height * 0.15 * 2.5, self.start_pos[1] + self.height * 0.15)
        self.draw_image(screen, "pionek3.png", self.start_pos[0] + self.height * 0.15 * 4, self.start_pos[1] + self.height * 0.15)
        self.draw_image(screen, "pionek4.png", self.start_pos[0] + self.height * 0.15 * 5.5, self.start_pos[1] + self.height * 0.15)

        self.inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size-self.button_size[0], self.start_pos[1], 'Gracz 1:'))
        self.inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size - self.button_size[0], self.start_pos[1]+self.button_size[1]*0.7, ''))

        self.inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size - self.button_size[0], self.start_pos[1]+self.button_size[1]*1.7, 'Gracz 2:'))
        self.inboxes.append(self.draw_inbox(screen, self.start_pos[0] - self.title_size - self.button_size[0], self.start_pos[1]+self.button_size[1]*2.4, ""))

        text_color = (193, 225, 193)
        font = pygame.font.SysFont('Arial', int(self.text_size * 0.9), True)

        nick_surface = font.render("Twój nick:", True, text_color)
        screen.blit(nick_surface, (self.inboxes[0].x + 5, self.inboxes[0].y + 5))
        screen.blit(nick_surface, (self.inboxes[2].x + 5, self.inboxes[2].y + 5))

        pionek_surface = font.render("Twój numer pionka:", True, text_color)
        screen.blit(pionek_surface, (self.inboxes[1].x + 5, self.inboxes[1].y + 5))
        screen.blit(pionek_surface, (self.inboxes[3].x + 5, self.inboxes[3].y + 5))


        text_surface = font.render(self.users[0][0], True, text_color)
        screen.blit(text_surface, (self.inboxes[0].x+nick_surface.get_width()*1.2, self.inboxes[0].y + 5))

        text_surface = font.render(self.users[1][0], True, text_color)
        screen.blit(text_surface, (self.inboxes[2].x+nick_surface.get_width()*1.2, self.inboxes[2].y + 5))

        text_surface = font.render(self.users[0][1], True, text_color)
        screen.blit(text_surface, (self.inboxes[1].x + pionek_surface.get_width() * 1.1, self.inboxes[1].y + 5))

        text_surface = font.render(self.users[1][1], True, text_color)
        screen.blit(text_surface, (self.inboxes[3].x + pionek_surface.get_width() * 1.1, self.inboxes[3].y + 5))


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
            '''
            if event.key == pygame.K_BACKSPACE:
                if user == 1:A
                    self.user_nick1 = self.user_nick1[:-1]
                elif user == 2:
                    self.user_nick2 = self.user_nick2[:-1]
                elif user == 3:
                    self.user_pionek1 = self.user_pionek1[:-1]
                elif user == 4:
                    self.user_pionek2 = self.user_pionek2[:-1]
            else:
                if user == 1:
                    self.user_nick1 += event.unicode
                elif user == 2:
                    self.user_nick2 += event.unicode
                elif user == 3:
                    self.user_pionek1 += event.unicode
                elif user == 4:
                    self.user_pionek2 += event.unicode
            '''
    def draw_inbox(self, screen, x, y, text):

        pygame.draw.rect(screen, (47, 79, 79), (x, y, self.button_size[0], self.button_size[1]//2))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.button_size[0], self.button_size[1]//2), 3)
        #pygame.draw.rect(screen, (0, 0, 0), (x, y, self.button_size[0], self.button_size[1] // 2), 3)

        text_color = (47, 79, 79)
        font = pygame.font.SysFont('Arial', int(self.text_size), True)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x+self.title_size, y - self.text_size)
        screen.blit(text_surface, text_rect)
        return pygame.Rect(x, y, self.button_size[0], self.button_size[1]//2)


