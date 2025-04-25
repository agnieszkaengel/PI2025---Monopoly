import pygame
from dimensions_generator import Dimensions
class Menu:
    def __init__ (self, dim:Dimensions):
        self.width = dim.menu_width
        self.screen_width = dim.screen_width
        self.screen_height = dim.screen_height
        self.menu_left_corner = ((self.screen_width-self.width)//2, (self.screen_height-self.width)//2)
        self.title_size = self.width * 0.05
        self.text_size = self.title_size * 0.5
        self.button_size = (self.width * 0.4, self.width * 0.1)
        self.button_2 = None
        self.button_3 = None

    def draw_main_menu(self, screen):
        pygame.draw.rect(screen, (193, 225, 193), (self.menu_left_corner[0], self.menu_left_corner[1], self.width - 1, self.width - 1))
        pygame.draw.rect(screen, (0, 0, 0), (self.menu_left_corner[0], self.menu_left_corner[1], self.width, self.width), 3)

        font = pygame.font.SysFont('Arial', int(self.title_size), True)
        text_color = (0, 0, 0)
        text = font.render("MENU GRY", True, text_color)
        text_rect = text.get_rect(center=(self.menu_left_corner[0]+0.5*self.width, self.menu_left_corner[1]+self.title_size))
        screen.blit(text, text_rect)

        start_pos = (self.menu_left_corner[0] + 0.5 * self.width, self.menu_left_corner[1] + self.title_size * 3)
        end_pos = (self.menu_left_corner[0] + 0.5 * self.width, self.menu_left_corner[1] + self.width - self.title_size * 3)
        pygame.draw.line(screen, text_color, start_pos, end_pos, 3)

        self.button_2 = self.draw_button(screen, "Gra podstawowa", start_pos[0]+self.title_size, start_pos[1])

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
        pygame.draw.rect(screen, (193, 225, 193), (self.menu_left_corner[0], self.menu_left_corner[1], self.width - 1, self.width - 1))
        pygame.draw.rect(screen, (0, 0, 0), (self.menu_left_corner[0], self.menu_left_corner[1], self.width, self.width), 3)

        font = pygame.font.SysFont('Arial', int(self.title_size), True)
        text_color = (0, 0, 0)
        text = font.render("WYBOR NICKÓW ORAZ PIONKÓW", True, text_color)
        text_rect = text.get_rect(center=(self.menu_left_corner[0]+0.5*self.width, self.menu_left_corner[1]+self.title_size))
        screen.blit(text, text_rect)

        start_pos = (self.menu_left_corner[0] + 0.5 * self.width, self.menu_left_corner[1] + self.title_size * 3)
        end_pos = (self.menu_left_corner[0] + 0.5 * self.width, self.menu_left_corner[1] + self.width - self.title_size * 3)
        pygame.draw.line(screen, text_color, start_pos, end_pos, 3)

        self.button_3 = self.draw_button(screen, "Gotowe", start_pos[0]+self.title_size, start_pos[1])



