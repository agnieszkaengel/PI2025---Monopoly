from dimensions_generator import Dimensions
from tile import Street, Station, Action
from dice import Dice
import json, pygame
class Board:
    def __init__(self, dim:Dimensions):
        self.board_width = dim.board_width
        self.board_left_corner = dim.board_left_corner
        self.tile_width = dim.tile_width
        self.tile_height = dim.tile_height
        self.tiles = []
        self.create_tiles()
        self.font_size = dim.font_size
        self.inner_width = dim.board_width - 2 * dim.tile_height
        self.inner_left_corner = (dim.board_left_corner[0]+dim.tile_height, dim.board_left_corner[1]+dim.tile_height)




    def create_tiles(self):
        with open("tiles.json", "r", encoding="utf-8") as f:
            tile_data = json.load(f)

        i = 0
        for tile in tile_data:
            tile_type = tile["tile_type"]
            name = tile["name"]
            index = tile["index"]

            if i==0 or i==10 or i==29 or i==39:
                image = tile.get("image")
                image = f"images/{image}" if image else None
                action = Action(name, tile_type, self.tile_height, self.tile_height, image, index)
                self.tiles.append(action)
            else:
                if tile_type == "Street":
                    color = tile["color"]
                    price = tile.get("price")
                    rent = tile.get("rent")
                    if (0 < i < 10) or (19 < i < 29):
                        street = Street(name, tile_type, self.tile_width, self.tile_height, color, price, rent, index, owner=None)
                    else:
                        street = Street(name, tile_type, self.tile_height, self.tile_width, color, price, rent, index, owner=None)
                    self.tiles.append(street)

                elif tile_type == "Station":
                    price = tile.get("price")
                    rent = tile.get("rent")
                    image = tile.get("image")
                    image = f"images/{image}" if image else None

                    if (0 < i < 10) or (19 < i < 29):
                        station = Station(name, tile_type, self.tile_width, self.tile_height, image, price, rent, index, owner=None)
                    else:
                        station = Station(name, tile_type, self.tile_height, self.tile_width, image, price, rent, index, owner=None)
                    self.tiles.append(station)

                elif tile_type == "Action":
                    image = tile.get("image")
                    image = f"images/{image}" if image else None

                    if (0 < i < 10) or (19 < i < 29):
                        action = Action(name, tile_type, self.tile_width, self.tile_height, image, index)
                    else:
                        action = Action(name, tile_type, self.tile_height, self.tile_width, image, index)
                    self.tiles.append(action)
            i=i+1

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
        image = pygame.image.load("Monopoly.png").convert_alpha()
        image = pygame.transform.scale(image, (self.inner_width*0.4, self.inner_width*0.2))
        image_rect = image.get_rect(center=(self.inner_left_corner[0]+0.5*self.inner_width, self.inner_left_corner[1]+0.5*self.inner_width))
        screen.blit(image, image_rect)

    def check_position(self, index):
        for i, tile in enumerate(self.tiles):
            if tile.index == index:
                return tile.tile_type, i
            i=i+1
        return None

