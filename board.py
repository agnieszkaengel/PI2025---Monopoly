from dimensions_generator import Dimensions
from tile import Tile, Street, Station, Action
import pygame
class Board:
    def __init__(self, dim:Dimensions):
        self.board_width = dim.board_width
        self.board_left_corner = dim.board_left_corner
        self.tile_width = dim.tile_width
        self.tile_height = dim.tile_height
        self.tiles = []
        self.create_tiles()

    def create_tiles(self):
        '''
        action1 = Action("Wiezienie", 3, self.tile_height, self.tile_height, None)
        self.tiles.append(action1)
        street1 = Street("Ulica Marsa", 1, self.tile_width, self.tile_height, (255, 0, 255), 100, 20, None)
        self.tiles.append(street1)
        station1 = Station("Dworzec Gdanski", 2, self.tile_width, self.tile_height, pygame.image.load("Train.png"), 150, 30, None)
        self.tiles.append(station1)
        street1 = Street("Ulica Jagiellonska", 1, self.tile_width, self.tile_height, (173, 216, 230), 100, 20, None)
        self.tiles.append(street1)
        street1 = Street("Ulica Plowiecka", 1, self.tile_width, self.tile_height, (255, 0, 255), 100, 20, None)
        self.tiles.append(street1)
        street1 = Street("Ulica Stalowa", 1, self.tile_width, self.tile_height, (139, 69, 19), 100, 20, None)
        self.tiles.append(street1)
        street1 = Street("Ulica Marszalkowska", 1, self.tile_width, self.tile_height, (0, 128, 0), 100, 20, None)
        self.tiles.append(street1)
        station1 = Station("Dworzec Gdanski", 2, self.tile_width, self.tile_height, pygame.image.load("Train.png"), 150,
                           30, None)
        self.tiles.append(station1)
        street1 = Street("Ulica Jagiellonska", 1, self.tile_width, self.tile_height, (173, 216, 230), 100, 20, None)
        self.tiles.append(street1)
        street1 = Street("Ulica Plowiecka", 1, self.tile_width, self.tile_height, (255, 0, 255), 100, 20, None)
        self.tiles.append(street1)
      #  self.tiles.append(action1)
        '''
        for i in range(10):
            if i==0:
                action1 = Action("Wiezienie", 3, self.tile_height, self.tile_height, None)
                self.tiles.append(action1)
            else:
                tile1 = Station("Baza Ulica", 1, self.tile_width, self.tile_height, None, 100, 20, None)
                self.tiles.append(tile1)

        for i in range(10):
            if i == 0:
                action1 = Action("Wiezienie", 3, self.tile_height, self.tile_height, None)
                self.tiles.append(action1)
            else:
                tile1 = Station("Baza Ulica", 1, self.tile_height, self.tile_width, None, 100, 20, None)
                self.tiles.append(tile1)

        for i in range(10):
            if i==9:
                action1 = Action("Wiezienie", 3, self.tile_height, self.tile_height, None)
                self.tiles.append(action1)
            else:
                tile1 = Station("Baza Ulica", 1, self.tile_width, self.tile_height, None, 100, 20, None)
                self.tiles.append(tile1)

        for i in range(10):
            if i == 9:
                action1 = Action("Wiezienie", 3, self.tile_height, self.tile_height, None)
                self.tiles.append(action1)
            else:
                tile1 = Station("Baza Ulica", 1, self.tile_height, self.tile_width, None, 100, 20, None)
                self.tiles.append(tile1)

    def draw_one_side(self, screen, x, y, start, stop, rotation):
        prev_width = 0
        prev_height = 0
        for i, tile in enumerate(self.tiles[start:stop]):
            tile.draw(screen, x + prev_width, y + prev_height, rotation)
            if start == 0 or start == 20:
                if i==0 and start == 0:
                    prev_width = prev_width+1
                prev_width += tile.width
            elif start == 10 or start == 30:
                if i==0 and start == 10:
                    prev_height = prev_height+1
                prev_height += tile.height

    def draw(self, screen):
        self.draw_one_side(screen, self.board_left_corner[0], self.board_left_corner[1],0 ,10, 180)
        self.draw_one_side(screen, self.board_left_corner[0]+self.tile_height+9*self.tile_width+1, self.board_left_corner[1], 10, 20, 90)
        self.draw_one_side(screen, self.board_left_corner[0]+self.tile_height+1, self.board_left_corner[1]+self.tile_height+9*self.tile_width+1,20 ,30, 0)
        self.draw_one_side(screen, self.board_left_corner[0], self.board_left_corner[1] + self.tile_height + 1, 30, 40, -90)
