from typing import Tuple
from tile import Tile
from dimensions_generator import Dimensions
from player_menu import PlayerMenu
import pygame
class Player:
    def __init__(self, name, figure, money, pos:Tuple[int, int], idx, dim:Dimensions):
        self.name = name
        self.figure = figure
        self.money = money
        self.position = pos
        self.tile_index = idx
        self.owned_tiles = []
        self.player_menu = PlayerMenu(dim)
        self.in_prison = False
        self.in_parking = False
        self.waiting_count = 0

    def add_owned_tile(self, tile:Tile):
        self.owned_tiles.append(tile)

    def highlight(self, title_to_highlight, border_color):
        self.player_menu.highlight_tile(title_to_highlight, border_color)

    def __repr__(self):
        return f"Player(name={self.name}, figure={self.figure})"

