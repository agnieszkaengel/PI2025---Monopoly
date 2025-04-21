from dimensions_generator import Dimensions
from tile import Tile, Street, Station, Action
import pygame
import json
class Board:
    def __init__(self, dim:Dimensions):
        self.board_width = dim.board_width
        self.board_left_corner = dim.board_left_corner
        self.tile_width = dim.tile_width
        self.tile_height = dim.tile_height
        self.tiles = []
        self.create_tiles()

    def create_tiles(self):

        with open("tiles.txt", "r", encoding="utf-8") as f:
            tile_data = json.load(f)

        i = 0
        for tile in tile_data:
            tile_type = tile["tile_type"]
            name = tile["name"]

            if i==0 or i==10 or i==29 or i==39:
                image = tile.get("image")
                action = Action(name, tile_type, self.tile_height, self.tile_height, image)
                self.tiles.append(action)
            else:
                if tile_type == "Street":
                    color = tile["color"]
                    price = tile.get("price")
                    rent = tile.get("rent")
                    if (0 < i < 10) or (19 < i < 29):
                        street = Street(name, tile_type, self.tile_width, self.tile_height, color, price, rent, owner=None)
                    else:
                        street = Street(name, tile_type, self.tile_height, self.tile_width, color, price, rent, owner=None)
                    self.tiles.append(street)

                elif tile_type == "Station":
                    price = tile.get("price")
                    rent = tile.get("rent")
                    image = tile.get("image")
                    if (0 < i < 10) or (19 < i < 29):
                        station = Station(name, tile_type, self.tile_width, self.tile_height, image, price=price, rent=rent, owner=None)
                    else:
                        station = Station(name, tile_type, self.tile_height, self.tile_width, image, price=price, rent=rent, owner=None)
                    self.tiles.append(station)

                elif tile_type == "Action":
                    image = tile.get("image")
                    if (0 < i < 10) or (19 < i < 29):
                        action = Action(name, tile_type, self.tile_width, self.tile_height, image)
                    else:
                        action = Action(name, tile_type, self.tile_height, self.tile_width, image)
                    self.tiles.append(action)
            i=i+1


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
                tile1 = Street("Baza Ulica", 1, self.tile_height, self.tile_width, (255, 0, 255), 100, 20, None)
                self.tiles.append(tile1)

        for i in range(10):
            if i==9:
                action1 = Action("Wiezienie", 3, self.tile_height, self.tile_height, None)
                self.tiles.append(action1)
            else:
                tile1 = Street("Baza Ulica", 1, self.tile_width, self.tile_height, (255, 0, 255), 100, 20, None)
                self.tiles.append(tile1)

        for i in range(10):
            if i == 9:
                action1 = Action("Wiezienie", 3, self.tile_height, self.tile_height, None)
                self.tiles.append(action1)
            else:
                tile1 = Street("Baza Ulica", 1, self.tile_height, self.tile_width, (255, 0, 255), 100, 20, None)
                self.tiles.append(tile1)
'''
    def draw_one_side(self, screen, x, y, start, stop, rotation):
        prev_width = 0
        prev_height = 0
        for i, tile in enumerate(self.tiles[start:stop]):
            tile.draw(screen, x + prev_width, y + prev_height, rotation)
            if start == 0 or start == 20:
                if i==0 and start == 0:
                    prev_width = prev_width+1
                prev_width += tile.width + 1
            elif start == 10 or start == 30:
                if i==0 and start == 10:
                    prev_height = prev_height+1
                prev_height += tile.height + 1

    def draw(self, screen):
        self.draw_one_side(screen, self.board_left_corner[0], self.board_left_corner[1],0 ,10, 180)
        self.draw_one_side(screen, self.board_left_corner[0]+self.tile_height+9*self.tile_width+1+9, self.board_left_corner[1], 10, 20, 90)
        self.draw_one_side(screen, self.board_left_corner[0]+self.tile_height+1, self.board_left_corner[1]+self.tile_height+9*self.tile_width+1+9,20 ,30, 0)
        self.draw_one_side(screen, self.board_left_corner[0], self.board_left_corner[1] + self.tile_height + 1, 30, 40, -90)
