import pygame
from dimensions_generator import Dimensions
from board_service import BoardService
from menu import Menu
from player import Player
class GamePlay:
    def __init__(self, screen, running):
        self.dimensions = Dimensions(screen)
        self.board_service = BoardService(self.dimensions)
        self.menu = Menu(self.dimensions)
        self.current_state = 0
        self.inbox_active = ''
        self.players_number = 0
        self.running = running
        self.player = ''
        self.players_created = False
        self.players: list [Player] = []
        self.current_player_idx = 0

    def create_players(self, start_money):
        for i in range(self.players_number):
            self.players.append(Player(self.menu.users[i][0], self.menu.users[i][1], start_money, (self.board_service.start[0]-(self.dimensions.tile_height*0.5)+(i*0.25*self.dimensions.tile_height)+(0.125*self.dimensions.tile_height), self.board_service.start[1] ), 0))

    def run(self, screen):
        while self.running:
            screen.fill((255, 255, 255))
            if self.current_state == 0:
                self.menu.draw_menu(screen)
            elif self.current_state == 1:
                self.menu.draw_nick_menu(screen)
                print("Ilość przycisków:", len(self.menu.buttons))
            elif self.current_state == 2:
                if not self.players_created:
                    self.create_players(1500)
                    self.board_service.players = self.players
                    self.players_created = True

                current_player = self.players[self.current_player_idx]
                #self.board_service.player = current_player
                print(current_player.name)

                self.board_service.board.draw(screen)
                self.board_service.start_pos(screen)

                turn_finished = self.board_service.update(screen, self.current_player_idx)
                if turn_finished:
                    self.current_player_idx = (self.current_player_idx + 1) % self.players_number
                    print(f"Teraz tura gracza: {self.players[self.current_player_idx].name}")
            else:
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu.buttons[0].collidepoint(event.pos) and self.current_state == 0:
                        self.current_state = 1
                        self.players_number = 2
                        self.menu.create_users_list(self.players_number)
                    elif self.menu.buttons[1].collidepoint(event.pos) and self.current_state == 0:
                        self.current_state = 3
                    elif self.menu.buttons[2].collidepoint(event.pos) and self.current_state == 1:
                        self.current_state = 2
                    elif self.menu.inboxes[0].collidepoint(event.pos):  # and current_state == 1:
                        self.inbox_active = 0 #nick1
                        self.player = 0
                    elif self.menu.inboxes[1].collidepoint(event.pos):  # and current_state == 1:
                        self.inbox_active = 1 #pionek1
                        self.player = 0
                    elif self.menu.inboxes[2].collidepoint(event.pos):  # and current_state == 1:
                        self.inbox_active = 2 #nick2
                        self.player = 1
                    elif self.menu.inboxes[3].collidepoint(event.pos):  # and current_state == 1:
                        self.inbox_active = 3 #pionek2
                        self.player = 1
                    elif self.current_state == 2 and self.board_service.dice.button.collidepoint(event.pos):
                        self.board_service.handle_click(screen, event)

                    else:
                        pass
                elif self.player == 0 or self.player == 1:
                    self.menu.handle_event(event, self.inbox_active, self.player)
            pygame.display.flip()