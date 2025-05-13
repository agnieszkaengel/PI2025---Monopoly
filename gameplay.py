import pygame
from dimensions_generator import Dimensions
from board_service import BoardService
from menu import Menu
from player import Player
from tile_service import TileService



class GamePlay:
    def __init__(self, screen, running):
        self.dimensions = Dimensions(screen)
        self.board_service = BoardService(self.dimensions)
        self.menu = Menu(self.dimensions)
        self.tiles_service = TileService(self.board_service.board, self.dimensions)
        self.current_state = 0
        self.nick_inbox_active = 100
        self.choice_inbox_active = 100 #0 - liczba graczy, 1 - majątek pocz, 2 - kwota przy start
        self.players_number = 0
        self.running = running
        self.player = ''
        self.players_created = False
        self.players: list [Player] = []
        self.current_player_idx = 0
        self.double_rolls = 0
        self.begin_money = 1500
        self.last_event = None

    def create_players(self, start_money):
        for i in range(self.players_number):
            self.players.append(Player(self.menu.users[i][0], self.menu.users[i][1], start_money, self.board_service.start, 0, self.dimensions))


    def run(self, screen):
        while self.running:
            screen.fill((200, 220, 200))
            if self.current_state == 0:
                self.menu.draw_menu(screen)
            elif self.current_state == 1:
                self.menu.draw_nick_menu(screen, self.players_number, self.current_state)
            elif self.current_state == 2:
                if not self.players_created:
                    self.create_players(self.begin_money)
                    self.board_service.players = self.players
                    self.players_created = True

                self.board_service.board.draw(screen)
                self.board_service.draw_players_menus(screen, (self.dimensions.screen_width-self.dimensions.board_width)//2 * 0.05, self.dimensions.screen_height//2 * 0.025)
                self.board_service.start_pos(screen)

                turn_finished, was_double = self.board_service.update(screen, self.current_player_idx)
                is_bought = self.tiles_service.tile_action(self.board_service.board.tiles[self.board_service.list_number], screen, self.players[self.current_player_idx], self.last_event)

               # if is_bought:
                #    tile = self.board_service.board.tiles[self.board_service.list_number]
                 #   print(tile.color)
                  #  self.players[self.current_player_idx].player_menu.highlight_tile(tile.name, tile.color)

                print(self.players[self.current_player_idx].money)
                #obsluga pol
                if turn_finished:
                    self.tiles_service.buying_finished = False
                    self.tiles_service.rent_finished = False
                    if was_double:
                        self.double_rolls += 1
                        if self.double_rolls < 3:
                            pass
                        else:
                            self.double_rolls = 0
                            self.current_player_idx = (self.current_player_idx + 1) % self.players_number
                    else:
                        self.double_rolls = 0
                        self.current_player_idx = (self.current_player_idx + 1) % self.players_number
            elif self.current_state == 3:
                self.menu.personalize_game_menu(screen)#pass #menu wyboru kwoty startowej, liczby graczy, kwoty przejscia prze start
            elif self.current_state == 4:
                self.menu.draw_nick_menu(screen, self.players_number, self.current_state)#pass #menu wyboru kwoty startowej, liczby graczy, kwoty przejscia prze start

            else:
                pass

            for event in pygame.event.get():
                self.last_event = event
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu.buttons[0].collidepoint(event.pos) and self.current_state == 0:
                        self.current_state = 1
                        self.players_number = 2
                        self.menu.create_users_list(self.players_number)
                    elif self.menu.buttons[1].collidepoint(event.pos) and self.current_state == 0:
                        self.current_state = 3
                    elif self.menu.buttons[3].collidepoint(event.pos) and self.current_state == 3:
                        self.current_state = 4
                        self.players_number = int(self.menu.personalize_settings[0])
                        self.begin_money = int(self.menu.personalize_settings[1])
                        self.board_service.start_add = int(self.menu.personalize_settings[2])
                        self.menu.create_users_list(self.players_number)
                    elif self.menu.buttons[2].collidepoint(event.pos) and self.current_state == 1:
                        if self.menu.validate_tokens():
                            self.current_state = 2
                    elif self.menu.buttons[2].collidepoint(event.pos) and self.current_state == 4:
                        if self.menu.validate_tokens():
                            self.current_state = 2
                    elif len(self.menu.nick_inboxes) > 0 and self.menu.nick_inboxes[0].collidepoint(event.pos):# and self.current_state == 1:
                        self.nick_inbox_active = 0 #nick1
                        self.player = 0
                    elif len(self.menu.nick_inboxes) > 0 and self.menu.nick_inboxes[1].collidepoint(event.pos):# and self.current_state == 1 or self.current_state == 4:
                        self.nick_inbox_active = 1 #pionek1
                        self.player = 0
                    elif len(self.menu.nick_inboxes) > 0 and self.menu.nick_inboxes[2].collidepoint(event.pos):# and self.current_state == 1 or self.current_state == 4:
                        self.nick_inbox_active = 2 #nick2
                        self.player = 1
                    elif len(self.menu.nick_inboxes) > 0 and self.menu.nick_inboxes[3].collidepoint(event.pos):# and self.current_state == 1 or self.current_state == 4:
                        self.nick_inbox_active = 3 #pionek2
                        self.player = 1
                    elif len(self.menu.nick_inboxes) > 0 and self.menu.nick_inboxes[4].collidepoint(event.pos):# and self.current_state == 1 or self.current_state == 4:
                        self.nick_inbox_active = 4 #nick3
                        self.player = 2
                    elif len(self.menu.nick_inboxes) > 0 and self.menu.nick_inboxes[5].collidepoint(event.pos):# and self.current_state == 1 or self.current_state == 4:
                        self.nick_inbox_active = 5 #pionek3
                        self.player = 2
                    elif len(self.menu.nick_inboxes) > 0 and self.menu.nick_inboxes[6].collidepoint(event.pos):# and self.current_state == 1 or self.current_state == 4:
                        self.nick_inbox_active = 6 #nick4
                        self.player = 3
                    elif len(self.menu.nick_inboxes) > 0 and self.menu.nick_inboxes[7].collidepoint(event.pos):# and self.current_state == 1 or self.current_state == 4:
                        self.nick_inbox_active = 7 #pionek4
                        self.player = 3
                    elif len(self.menu.personalize_inboxes) > 0 and self.menu.personalize_inboxes[0].collidepoint(event.pos):
                        self.choice_inbox_active = 0
                    elif len(self.menu.personalize_inboxes) > 0 and self.menu.personalize_inboxes[1].collidepoint(event.pos):
                        self.choice_inbox_active = 1
                    elif len(self.menu.personalize_inboxes) > 0 and self.menu.personalize_inboxes[2].collidepoint(event.pos):
                        self.choice_inbox_active = 2
                    elif self.current_state == 2 and self.board_service.dice.button.collidepoint(event.pos):
                        self.board_service.handle_click(event)
                    else:
                        pass
                elif 0<=self.nick_inbox_active<=7:
                    self.menu.handle_event(event, self.nick_inbox_active, self.player)
                elif 0<=self.choice_inbox_active<=2:
                    self.menu.handle_personalize_settings(event, self.choice_inbox_active)



            pygame.display.flip()