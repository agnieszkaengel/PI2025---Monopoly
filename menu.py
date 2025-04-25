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
        self.start_pos = ()
        self.end_pos = ()
        self.button_01 = None
        self.button_02 = None
        self.button_1 = None
        self.inbox_g1 = None
        self.inbox_g2 = None

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

        self.start_pos = (self.menu_left_corner[0] + 0.5 * self.width, self.menu_left_corner[1] + self.title_size * 3)
        self.end_pos = (self.menu_left_corner[0] + 0.5 * self.width, self.menu_left_corner[1] + self.height - self.title_size)
        pygame.draw.line(screen, text_color, self.start_pos, self.end_pos, 3)

    def draw_menu(self, screen):
        self.draw_main_part(screen, "MENU GRY")
        self.button_01 = self.draw_button(screen, "Gra podstawowa", self.start_pos[0]+self.title_size, self.start_pos[1])
        self.button_02 = self.draw_button(screen, "Gra personalizowana", self.start_pos[0] + self.title_size, self.start_pos[1]+self.button_size[1]*1.5)

    def draw_button(self, screen, text, x, y):

        pygame.draw.rect(screen, (47, 79, 79), (x, y, self.button_size[0], self.button_size[1]))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.button_size[0], self.button_size[1]), 3)

        text_color = (193, 225, 193)
        font = pygame.font.SysFont('Arial', int(self.text_size), True)
        text = font.render(text, True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (x + self.button_size[0] / 2, y + self.button_size[1] / 2)
        screen.blit(text, text_rect)
        return pygame.Rect(x, y, self.button_size[0], self.button_size[1])

    def draw_nick_menu(self, screen):
        self.draw_main_part(screen, "WYBÓR NICKU I PIONKA")
        self.button_1 = self.draw_button(screen, "Gotowe", self.start_pos[0]+self.title_size, self.start_pos[1]+self.button_size[1]*2)

        self.draw_image(screen, "pionek1.png", self.start_pos[0]+self.height*0.15, self.start_pos[1]+self.height*0.15)
        self.draw_image(screen, "pionek2.png", self.start_pos[0] + self.height * 0.15 * 2.5, self.start_pos[1] + self.height * 0.15)
        self.draw_image(screen, "pionek3.png", self.start_pos[0] + self.height * 0.15 * 4, self.start_pos[1] + self.height * 0.15)
        self.draw_image(screen, "pionek4.png", self.start_pos[0] + self.height * 0.15 * 5.5, self.start_pos[1] + self.height * 0.15)

        self.inbox_g1 = self.draw_inbox(screen, self.start_pos[0]-self.title_size-self.button_size[0], self.start_pos[1], "Gracz 1:")
        self.inbox_g2 = self.draw_inbox(screen, self.start_pos[0] - self.title_size - self.button_size[0], self.start_pos[1]+self.button_size[1]*2, "Gracz 2:")


    def draw_image(self, screen, name, x, y):
        image = pygame.image.load(name).convert_alpha()
        im_size = self.height * 0.15
        image = pygame.transform.scale(image, (im_size, im_size))
        image_rect = image.get_rect(center=(x,y))
        screen.blit(image, image_rect)

    def draw_inbox(self, screen, x, y, text):

        pygame.draw.rect(screen, (47, 79, 79), (x, y, self.button_size[0], self.button_size[1]))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.button_size[0], self.button_size[1]), 3)
        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.button_size[0], self.button_size[1] // 2), 3)

        text_color = (47, 79, 79)
        font = pygame.font.SysFont('Arial', int(self.text_size), True)
        text = font.render(text, True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (x+self.title_size, y - self.text_size)
        screen.blit(text, text_rect)
        return pygame.Rect(x, y, self.button_size[0], self.button_size[1])
        #self.handle_event(event, input_box)

    def handle_event(self, event):
        text = ""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Wpisano:", text)
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode