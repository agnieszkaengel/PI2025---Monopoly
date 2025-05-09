from typing import Tuple
from tile import Tile
from dimensions_generator import Dimensions
import pygame
class Player:
    def __init__(self, name, figure, money, pos:Tuple[int, int], idx, dim:Dimensions):
        self.name = name
        self.figure = figure
        self.money = money
        self.position = pos
        self.tile_index = idx
        self.owned_tiles = []
        self.dim = dim

    def add_owned_tile(self, tile:Tile):
        self.owned_tiles.append(tile)


    def draw_player_menu(self, screen, x, y):
        pygame.draw.rect(screen, (193, 225, 193), (x, y, self.dim.player_menu_width, self.dim.player_menu_height))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, self.dim.player_menu_width, self.dim.player_menu_height), 3)
        print(self.dim.player_menu_width, self.dim.player_menu_height)

        font = pygame.font.SysFont('Arial', int(self.dim.font_size * 2), True)
        text_color = (0, 0, 0)
        text = font.render(str(self.name), True, text_color)
        text_rect = text.get_rect(center=(x+2*int(text.get_size()[1]), y+2 * int(self.dim.font_size * 1.2)))
        screen.blit(text, text_rect)

