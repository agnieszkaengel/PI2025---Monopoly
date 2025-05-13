from dimensions_generator import Dimensions
import pygame, json
from collections import defaultdict


class PlayerMenu:
    def __init__(self, dim: Dimensions):
        self.dim = dim
        self.rect_list = []
        self.tiles_list = [[] for _ in range(10)]
        self.rect_size = (dim.tile_width, dim.tile_height*0.25)
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
        rect = pygame.draw.rect(screen,(0,0,0), (x, y, self.rect_size[0], self.rect_size[1]), 2)
        self.rect_list.append({
            "rect": rect,
            "title": title,
            "border_color": (0,0,0)
        })
        font = pygame.font.SysFont('Arial', int(self.dim.font_size), False)
        text_color = (0, 0, 0)

        words = title.split()
        for word in words:
            text = font.render(word, True, text_color)
            text_rect = text.get_rect(center=(x+text.get_size()[0]*0.5+0.05*self.rect_size[0], y+text.get_size()[1]-0.05*self.rect_size[1]))
            y += self.dim.font_size
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

        self.rect_list = []

        for i in range (10):
            column = i % columns
            row = i // columns

            if row != 0:
                extra_spacing = row * extra_row_spacing + 3 * row_height + ((row-1)*4)*row_height + 0.2 * self.dim.player_menu_height
            elif row == 1:
                extra_spacing = row * extra_row_spacing + 3 * row_height + 0.2 * self.dim.player_menu_height
            else:
                extra_spacing = row * extra_row_spacing + 0.2 * self.dim.player_menu_height

            for j, item in enumerate(self.tiles_list[i]):
                el = j % 4
                rect_x = x + 0.05 * self.rect_size[0] + column * column_width
                rect_y = y + 0.1 * self.rect_size[0] + el * row_height + extra_spacing
                self.draw_tile_rect(screen, rect_x, rect_y, item[0])


        print(len(self.rect_list))

    def highlight_tile(self, title_to_highlight, new_color):
        for i, rect in enumerate(self.rect_list):
            if rect["title"] == title_to_highlight:
                rect["border_color"] = new_color
                print(rect["border_color"])


