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
        self.buttons: list[pygame.Rect] = []
        self.create_buttons_list()
        self.buying_finished = False
        self.rent_finished = False


    def create_buttons_list(self):
        self.buttons.append(pygame.Rect(self.window_place[0]+self.button_size[0]*0.5, self.window_place[1]+self.window_size[1]*0.6, self.button_size[0], self.button_size[1]))
        self.buttons.append(pygame.Rect(self.window_place[0]+self.button_size[0]*1.5, self.window_place[1]+self.window_size[1]*0.6, self.button_size[0], self.button_size[1]))
        self.buttons.append(pygame.Rect(self.window_place[0] + self.button_size[0] * 0.5 * 1.5,
                                        self.window_place[1] + self.window_size[1] * 0.6, self.button_size[0]*1.5,
                                        self.button_size[1]))
        self.buttons.append(pygame.Rect(self.window_place[0] + self.button_size[0] * 1.5 * 1.5,
                                        self.window_place[1] + self.window_size[1] * 0.6, self.button_size[0]*1.5,
                                        self.button_size[1]))

    def tile_action(self, tile: Tile, screen, player: Player, event):
            match tile.tile_type:
                case "Action":
                    pass
                case "Station" | "Street":
                    return self.buying_window(screen, tile, player, event)

    def street_service(self):
        pass

    def station_service(self):
        pass

    def buying_window(self, screen, tile, player, event):
        if tile.owner is None and not self.buying_finished:
            self.draw_buy_menu(screen, tile, player.name)
            return self.handle_buttons(tile, player, event)
        elif tile.owner is not None and tile.owner != player.name:
            self.draw_rent_menu(screen, tile)
            self.handle_buttons2(tile, player, event)
            return False
        else:
            return False



    def draw_buy_menu(self, screen, tile, name):
        pygame.draw.rect(screen, (193, 225, 193),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1))
        pygame.draw.rect(screen, (0, 0, 0),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1),2)
        text1 = name + ": Czy chcesz kupić nieruchomość: " + tile.name + "?"
        text2 = "KOSZT NIERUCHOMOSCI: " + str(tile.price) + " ZŁ" + "  POBIERANY CZYNSZ: " + str(tile.rent) + " ZŁ"

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
                self.buying_finished = True
                return False


    def draw_rent_menu(self, screen, tile):
        pygame.draw.rect(screen, (193, 225, 193),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1))
        pygame.draw.rect(screen, (0, 0, 0),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1),2)
        text1 = "Musisz opłacić czynsz graczowi: " + tile.owner
        text2 = "WYSOKOŚĆ CZYNSZU " + str(tile.rent) + " ZŁ"
        font = pygame.font.SysFont('Arial', int(self.font_size), True)
        text_color = (0, 0, 0)
        text1 = font.render(str(text1), True, text_color)
        text2 = font.render(str(text2), True, text_color)
        text_rect = text1.get_rect(center=(self.window_place[0] + self.window_size[0] // 2, self.window_place[1] + self.window_size[1] * 0.1))
        screen.blit(text1, text_rect)
        text_rect = text2.get_rect(center=(self.window_place[0] + self.window_size[0] // 2,self.window_place[1] + self.window_size[1] * 0.1 + self.font_size * 2))
        screen.blit(text2, text_rect)

        pygame.draw.rect(screen, (120, 180, 120), (self.window_place[0] + self.button_size[0] * 0.01, self.window_place[1] + self.window_size[1] * 0.6, self.button_size[0]*1.2, self.button_size[1]))
        text_tak = font.render('OPŁAĆ GOTÓWKĄ', True, (0, 0, 0))
        text_tak_rect = text_tak.get_rect(center=self.buttons[0].center)

        pygame.draw.rect(screen, (200, 100, 100), (
        self.window_place[0] + self.button_size[0] * 1.21, self.window_place[1] + self.window_size[1] * 0.6, self.button_size[0]*1.2, self.button_size[1]))
        text_nie = font.render('ZASTAW NIERUCHOMOŚĆ', True, (0, 0, 0))
        text_nie_rect = text_nie.get_rect(center=self.buttons[1].center)

        screen.blit(text_tak, text_tak_rect)
        screen.blit(text_nie, text_nie_rect)

    def handle_buttons2(self, tile, player, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons[2].collidepoint(event.pos):
                if player.money >= int(tile.rent):
                    player.money -= int(tile.rent)
                return True
            elif self.buttons[3].collidepoint(event.pos):
                self.rent_finished = True
        return None