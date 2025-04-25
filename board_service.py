from board import Board
from dice import Dice
from player import Player
from dimensions_generator import Dimensions
import pygame

class BoardService:
    def __init__(self, dim:Dimensions):
        self.board = Board(dim)
        self.player = Player("gracz1", "pionek1.png", 1500, (self.board.board_left_corner[0] + self.board.tile_height/2, self.board.board_left_corner[1] + self.board.board_width - self.board.tile_height/2))
        self.dice = Dice(self.board.tile_height, self.board.tile_width / 2, self.board.font_size)
        self.pending_move = False

    def create_players_list(self):
        self.player = Player("gracz1", "pionek1.png", 1500, (self.board.board_left_corner[0] + self.board.tile_height/2, self.board.board_left_corner[1] + self.board.board_width - self.board.tile_height/2))

    def start_pos(self, screen):
            image = pygame.image.load(self.player.figure).convert_alpha()
            image = pygame.transform.scale(image, (self.board.tile_height*0.3, self.board.tile_height*0.3))
            image_rect = image.get_rect(center = self.player.position)
            screen.blit(image, image_rect)

    def handle_click(self, screen, event):
        self.dice.click(
            screen,
            self.board.inner_left_corner[0] + self.board.inner_width - self.dice.button_size[0],
            self.board.inner_left_corner[1] + self.board.inner_width - self.dice.button_size[1],
            event
        )
        if self.dice.showing_dice:
            self.pending_move = True

    def try_change_pos(self):
        if self.pending_move and not self.dice.showing_dice:
            suma = self.dice.get_sum()
            x, y = self.player.position

            if self.player.tile_index < 10:
                right = 10 - self.player.tile_index-suma
                if right > 0:
                    if self.player.tile_index == 0:
                        distance = self.board.tile_height * 0.5 + self.board.tile_width * 0.5 + (suma-1) * self.board.tile_width
                    else:
                        distance = suma * self.board.tile_width
                    self.player.position = (x, y - distance)
                else:
                    if self.player.tile_index == 0:
                        distance_y = self.board.tile_height + self.board.tile_width + (suma-abs(right)-2) * self.board.tile_width
                        distance_x = self.board.tile_height*0.5 + self.board.tile_width * 0.5 + abs(right+1)*self.board.tile_width if right!=0 else 0
                    else:
                        distance_y = (suma-abs(right)-1) * self.board.tile_width + 0.5*self.board.tile_height + 0.5*self.board.tile_width
                        distance_x = abs(right+1)*self.board.tile_width + 0.5*self.board.tile_height + 0.5*self.board.tile_width if right!=0 else 0
                    self.player.position = (x+distance_x, y - distance_y)

            elif self.player.tile_index >= 10 and self.player.tile_index < 20:
                down = 20 - self.player.tile_index - suma
                if down > 0:
                    if self.player.tile_index == 10:
                        distance = self.board.tile_height * 0.5 + self.board.tile_width * 0.5 + (suma - 1) * self.board.tile_width
                    else:
                        distance = suma * self.board.tile_width
                    self.player.position = (x+distance, y)
                else:
                    if self.player.tile_index == 10:
                        distance_x = self.board.tile_height + self.board.tile_width + (suma - abs(down) - 2) * self.board.tile_width
                        distance_y = self.board.tile_height*0.5 + self.board.tile_width * 0.5 + abs(down+1)*self.board.tile_width if down!=0 else 0
                    else:
                        distance_x = (suma - abs(down) - 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width
                        distance_y = abs(down + 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width if down!=0 else 0
                    self.player.position = (x + distance_x, y + distance_y)

            elif self.player.tile_index >= 20 and self.player.tile_index < 30:
                left = 30 - self.player.tile_index - suma
                if left > 0:
                    if self.player.tile_index == 20:
                        distance = self.board.tile_height * 0.5 + self.board.tile_width * 0.5 + (suma - 1) * self.board.tile_width
                    else:
                        distance = suma * self.board.tile_width
                    self.player.position = (x, y + distance)
                else:
                    if self.player.tile_index == 20:
                        distance_y = self.board.tile_height + self.board.tile_width + (suma - abs(left) - 2) * self.board.tile_width
                        distance_x = self.board.tile_height*0.5 + self.board.tile_width * 0.5 + abs(left+1)*self.board.tile_width if left!=0 else 0
                    else:
                        distance_y = (suma - abs(left) - 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width
                        distance_x = abs(left + 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width if left!=0 else 0
                    self.player.position = (x - distance_x, y + distance_y)

            elif self.player.tile_index >= 30 and self.player.tile_index < 40:
                down = 40 - self.player.tile_index - suma
                if down > 0:
                    if self.player.tile_index == 30:
                        distance = self.board.tile_height * 0.5 + self.board.tile_width * 0.5 + (suma - 1) * self.board.tile_width
                    else:
                        distance = suma * self.board.tile_width
                    self.player.position = (x-distance, y)
                else:
                    if self.player.tile_index == 30:
                        distance_x = self.board.tile_height + self.board.tile_width + (suma - abs(down) - 3) * self.board.tile_width
                        distance_y = self.board.tile_height*0.5 + self.board.tile_width * 0.5 + abs(down+1)*self.board.tile_width if down!=0 else 0
                    else:
                        distance_x = (suma - abs(down) - 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width
                        distance_y = abs(down + 1) * self.board.tile_width + 0.5 * self.board.tile_height + 0.5 * self.board.tile_width if down!=0 else 0
                    self.player.position = (x - distance_x, y - distance_y)
            '''     
            if self.player.tile_index == 0 or self.player.tile_index == 20 or self.player.tile_index == 30 or self.player.tile_index == 10:
                distance = self.board.tile_height * 0.5 + self.board.tile_width * 0.5 + (suma-1) * self.board.tile_width
            else:
                distance = suma * self.board.tile_width

            if self.player.tile_index < 10 and suma < 11 - self.player.tile_index:
                self.player.position = (x, y - distance)
            '''
            self.player.tile_index = (self.player.tile_index + suma) % 40
            print(self.player.tile_index)
            self.pending_move = False

    def update(self, screen):
        button_x = self.board.inner_left_corner[0] + self.board.inner_width - self.dice.button_size[0]
        button_y = self.board.inner_left_corner[1] + self.board.inner_width - self.dice.button_size[1]

        self.dice.draw_button(screen, button_x, button_y)
        self.dice.update(screen, button_x, button_y)
        self.try_change_pos()
