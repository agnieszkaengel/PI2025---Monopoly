from dimensions_generator import Dimensions
import pygame, json
from collections import defaultdict


class PlayerMenu:
    def __init__(self, dim: Dimensions):
        self.dim = dim
        self.rect_list = []
        self.tiles_list = [[] for _ in range(10)]
        self.rect_size = (dim.tile_width, dim.tile_height*0.21)
        self.load_tiles_list()

    def draw_player_menu(self, screen, name, x, y):
        pygame.draw.rect(screen, (193, 225, 193), (x, y, self.dim.player_menu_width, self.dim.player_menu_height))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.dim.player_menu_width, self.dim.player_menu_height), 3)
        print(self.dim.player_menu_width, self.dim.player_menu_height)

        font = pygame.font.SysFont('Arial', int(self.dim.font_size * 2), True)
        text_color = (0, 0, 0)
        text = font.render(str(name), True, text_color)
        text_rect = text.get_rect(center=(x+2*int(text.get_size()[1]), y+2 * int(self.dim.font_size * 1.2)))
        screen.blit(text, text_rect)

        self.create_rect_list(screen, x, y)

    def draw_tile_rect(self, screen, x, y, title):
        rect = pygame.draw.rect(screen, (0, 0, 0), (x, y, self.rect_size[0], self.rect_size[1]), 3)
        #self.rect_list.append(rect)
        font = pygame.font.SysFont('Arial', int(self.dim.font_size), False)
        text_color = (0, 0, 0)
        text = font.render(str(title), True, text_color)
        text_rect = text.get_rect(center=(x+text.get_size()[0], y+text.get_size()[1]))
        screen.blit(text, text_rect)
        return rect

    def load_tiles_list(self):
        with open("tiles_for_player_menu.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            column = item["column"]
            self.tiles_list[column].append((item["name"], item["color"], item["index"], item["column"]))

    def create_rect_list(self, screen, x, y):
        columns = 4
        row_height = self.rect_size[1] * 1.05
        column_width = self.rect_size[0] * 1.05
        extra_row_spacing = self.rect_size[1] * 0.4

        for i, item in enumerate(self.tiles_list):
            column = i % columns
            row = i // columns
            extra_spacing = (row // 4) * extra_row_spacing

            rect_x = x + 0.05 * self.rect_size[0] + column * column_width
            rect_y = y + 0.1 * self.rect_size[0] + row * row_height + extra_spacing
            self.draw_tile_rect(screen, rect_x, rect_y, item[0])





