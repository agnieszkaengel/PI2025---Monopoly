from typing import Tuple
class Player:
    def __init__(self, name, figure, money, pos:Tuple[int, int], idx):
        self.name = name
        self.figure = figure
        self.money = money
        self.position = pos
        self.tile_index = idx