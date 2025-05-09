from board import Board
import pygame
from player import Player
from dimensions_generator import Dimensions
from tile import Tile
class TileService:
    def __init__(self, board:Board, dim:Dimensions):
        self.tiles_list = board.tiles
        self.window_size = (dim.tile_width*5, dim.tile_height)
        self.window_place = (board.inner_left_corner[0]+4, board.inner_left_corner[1]+4)
        self.font_size = dim.font_size*1.2
        self.button_size = (self.window_size[0]//3, self.window_size[1]//3)
        self.buttons: list[pygame.Rect] = self.create_buttons_list()


    def create_buttons_list(self):
        buttons = []
        buttons.append(pygame.Rect(self.window_place[0]+self.button_size[0]*0.5, self.window_place[1]+self.window_size[1]*0.6, self.button_size[0], self.button_size[1]))
        buttons.append(pygame.Rect(self.window_place[0]+self.button_size[0]*1.5, self.window_place[1]+self.window_size[1]*0.6, self.button_size[0], self.button_size[1]))
        return buttons


    def tile_action(self, tile: Tile, screen, player: Player, event):
            match tile.tile_type:
                case "Action":
                    pass
                case "Station" | "Street":
                    self.buying_window(screen, tile, player, event)

    def street_service(self):
        pass

    def station_service(self):
        pass

    def buying_window(self, screen, tile, player, event):
        if tile.owner is None:
            self.draw_buy_menu(screen, tile)
            self.handle_buttons(tile, player, event)
        elif tile.owner != player.name:
            print("Musisz zapłacić czynsz graczowi:", tile.owner)
            print("Wartość:", tile.rent)
        else:
            pass

    def draw_buy_menu(self, screen, tile):
        pygame.draw.rect(screen, (193, 225, 193),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1))
        pygame.draw.rect(screen, (0, 0, 0),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1),2)
        text1 = "Czy chcesz kupić nieruchomość: " + tile.name + "?"
        text2 = "KOSZT NIERUCHOMOSCI: " + str(tile.price) + "ZŁ"

        font = pygame.font.SysFont('Arial', int(self.font_size), True)
        text_color = (0, 0, 0)
        text1 = font.render(str(text1), True, text_color)
        text2 = font.render(str(text2), True, text_color)
        text_rect = text1.get_rect(center=(self.window_place[0] + self.window_size[0]//2, self.window_place[1]+self.window_size[1]*0.1))
        screen.blit(text1, text_rect)
        text_rect = text2.get_rect(center=(self.window_place[0] + self.window_size[0] // 2, self.window_place[1] + self.window_size[1] * 0.1 + self.font_size*2))
        screen.blit(text2, text_rect)


        pygame.draw.rect(screen, (120, 180, 120), (self.window_place[0]+self.button_size[0]*0.5, self.window_place[1]+self.window_size[1]*0.6, self.button_size[0], self.button_size[1]))
        text_tak = font.render('TAK', True, (0, 0, 0))
        text_tak_rect = text_tak.get_rect(center=self.buttons[0].center)

        pygame.draw.rect(screen, (200, 100, 100), (self.window_place[0]+self.button_size[0]*1.5, self.window_place[1]+self.window_size[1]*0.6, self.button_size[0], self.button_size[1]))
        text_nie = font.render('NIE', True, (0, 0, 0))
        text_nie_rect = text_nie.get_rect(center=self.buttons[1].center)

        screen.blit(text_tak, text_tak_rect)
        screen.blit(text_nie, text_nie_rect)

    def handle_buttons(self, tile, player, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons[0].collidepoint(event.pos):
                if tile.owner is None and player.money >= tile.price:
                    tile.owner = player.name
                    player.money -= tile.price
                return True
            elif self.buttons[1].collidepoint(event.pos):
                return False
        return None
