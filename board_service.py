from board import Board
from dice import Dice
from player import Player
from dimensions_generator import Dimensions
from players_singleton import PlayersSingleton
import pygame
class BoardService:
    def __init__(self, dim:Dimensions):
        self.board = Board(dim)
        self.dim = dim
        self.start = (self.board.board_left_corner[0] + self.board.tile_height/2, self.board.board_left_corner[1] + self.board.board_width - self.board.tile_height/2)
        self.players_singleton = PlayersSingleton()
        self.players = self.players_singleton.players
        self.dice = Dice(self.board.tile_height, self.board.tile_width / 2, self.board.font_size)
        self.pending_move = False
        self.list_number = 0
        self.start_add = 200

    def start_pos(self, screen):
        for player in self.players:
            name = player.figure + ".png"
            image = pygame.image.load(name).convert_alpha()
            image = pygame.transform.scale(image, (self.board.tile_height*0.25, self.board.tile_height*0.25))
            image_rect = image.get_rect(center = player.position)
            screen.blit(image, image_rect)


    def handle_click(self, event):
        self.dice.click(event)
        if self.dice.showing_dice:
            self.pending_move = True

    def try_change_pos(self, idx):
        previous_tile_index = self.players[idx].tile_index
        if self.pending_move: #and not self.dice.showing_dice:
            suma = self.dice.get_sum()
            x, y = self.players[idx].position

            if self.players[idx].tile_index < 10:
                right = 10 - self.players[idx].tile_index-suma
                if right > 0:
                    if self.players[idx].tile_index == 0:
                        distance = self.board.tile_height * 0.5 + self.board.tile_width * 0.5 + (suma-1) * self.board.tile_width
                    else:
                        distance = suma * self.board.tile_width
                    self.players[idx].position = (x, y - distance)
                else:
                    if self.players[idx].tile_index == 0:
                        distance_y = self.board.tile_height + self.board.tile_width + (suma-abs(right)-2) * self.board.tile_width
                        distance_x = self.board.tile_height*0.5 + self.board.tile_width * 0.5 + abs(right+1)*self.board.tile_width if right!=0 else 0
                    else:
                        distance_y = (suma-abs(right)-1) * self.board.tile_width + 0.5*self.board.tile_height + 0.5*self.board.tile_width
                        distance_x = abs(right+1)*self.board.tile_width + 0.5*self.board.tile_height + 0.5*self.board.tile_width if right!=0 else 0
                    self.players[idx].position = (x+distance_x, y - distance_y)

            elif self.players[idx].tile_index >= 10 and self.players[idx].tile_index < 20:
                down = 20 - self.players[idx].tile_index - suma
                if down > 0:
                    if self.players[idx].tile_index == 10:
                        distance = self.board.tile_height * 0.5 + self.board.tile_width * 0.5 + (suma - 1) * self.board.tile_width
                    else:
                        distance = suma * self.board.tile_width
                    self.players[idx].position = (x+distance, y)
                else:
                    if self.players[idx].tile_index == 10:
                        distance_x = self.board.tile_height + self.board.tile_width + (suma - abs(down) - 2) * self.board.tile_width
                        distance_y = self.board.tile_height*0.5 + self.board.tile_width * 0.5 + abs(down+1)*self.board.tile_width if down!=0 else 0
                    else:
                        distance_x = (suma - abs(down) - 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width
                        distance_y = abs(down + 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width if down!=0 else 0
                    self.players[idx].position = (x + distance_x, y + distance_y)

            elif self.players[idx].tile_index >= 20 and self.players[idx].tile_index < 30:
                left = 30 - self.players[idx].tile_index - suma
                if left > 0:
                    if self.players[idx].tile_index == 20:
                        distance = self.board.tile_height * 0.5 + self.board.tile_width * 0.5 + (suma - 1) * self.board.tile_width
                    else:
                        distance = suma * self.board.tile_width
                    self.players[idx].position = (x, y + distance)
                else:
                    if self.players[idx].tile_index == 20:
                        distance_y = self.board.tile_height + self.board.tile_width + (suma - abs(left) - 2) * self.board.tile_width
                        distance_x = self.board.tile_height*0.5 + self.board.tile_width * 0.5 + abs(left+1)*self.board.tile_width if left!=0 else 0
                    else:
                        distance_y = (suma - abs(left) - 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width
                        distance_x = abs(left + 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width if left!=0 else 0
                    self.players[idx].position = (x - distance_x, y + distance_y)

            elif self.players[idx].tile_index >= 30 and self.players[idx].tile_index < 40:
                down = 40 - self.players[idx].tile_index - suma
                if down > 0:
                    if self.players[idx].tile_index == 30:
                        distance = self.board.tile_height * 0.5 + self.board.tile_width * 0.5 + (suma - 1) * self.board.tile_width
                    else:
                        distance = suma * self.board.tile_width
                    self.players[idx].position = (x-distance, y)
                else:
                    if self.players[idx].tile_index == 30:
                        distance_x = self.board.tile_height + self.board.tile_width + (suma - abs(down) - 3) * self.board.tile_width
                        distance_y = self.board.tile_height*0.5 + self.board.tile_width * 0.5 + abs(down+1)*self.board.tile_width if down!=0 else 0
                    else:
                        distance_x = (suma - abs(down) - 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width
                        distance_y = abs(down + 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width if down!=0 else 0
                    self.players[idx].position = (x - distance_x, y - distance_y)

            new_index = (self.players[idx].tile_index + suma) % 40
            if previous_tile_index > new_index:
                self.players[idx].money += self.start_add
            self.players[idx].tile_index = new_index


            tile_type, number = self.board.check_position(self.players[idx].tile_index)
            self.list_number = number #numer pola na liście pól w klasie board




            self.pending_move = False
            return True
        return False

    def draw_button(self, screen):
        x = self.board.inner_left_corner[0] + self.board.inner_width - self.dice.button_size[0]
        y = self.board.inner_left_corner[1] + self.board.inner_width - self.dice.button_size[1]
        self.dice.draw_button(screen, x, y)

    def update(self, screen, idx):
        button_x = self.board.inner_left_corner[0] + self.board.inner_width - self.dice.button_size[0]
        button_y = self.board.inner_left_corner[1] + self.board.inner_width - self.dice.button_size[1]

        #self.dice.draw_button(screen, button_x, button_y)
        self.dice.update(screen, button_x, button_y)
        if self.try_change_pos(idx):
            return True, self.dice.is_double()
        return False, False

    def draw_players_menus(self, screen, x, y):
        for i, player in enumerate(self.players):
            match i:
                case 0:
                    player.player_menu.draw_player_menu(screen, player.name, player.money, x, y)
                case 1:
                    player.player_menu.draw_player_menu(screen, player.name, player.money, x, y + (self.dim.screen_height-self.dim.player_menu_height)*0.95)
                case 2:
                    player.player_menu.draw_player_menu(screen, player.name, player.money, x + self.dim.board_width + self.dim.player_menu_width + (self.dim.screen_width-self.dim.board_width)//2 * 0.05 * 2.5, y)
                case 3:
                    player.player_menu.draw_player_menu(screen, player.name, player.money, x + self.dim.board_width + self.dim.player_menu_width + (self.dim.screen_width-self.dim.board_width)//2 * 0.05 * 2.5, y + (self.dim.screen_height-self.dim.player_menu_height)*0.95)


    def move_to_prison(self, idx):
        prison_x = 409.355
        prison_y = 59.355
        self.players[idx].position = (prison_x, prison_y)
        self.players[idx].tile_index = 10