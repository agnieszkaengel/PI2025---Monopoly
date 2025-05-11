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

    def add_owned_tile(self, tile:Tile):
        self.owned_tiles.append(tile)




