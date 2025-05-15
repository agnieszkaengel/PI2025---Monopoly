
import pygame
from dimensions_generator import Dimensions
from board_service import BoardService
from menu import Menu
from player import Player
from tile_service import TileService
from players_singleton import PlayersSingleton
from enum import Enum

class GameState(Enum):
    MAIN_MENU = 0
    NICKNAME_MENU = 1
    GAMEPLAY = 2
    PERSONALIZE_MENU = 3
    CUSTOMIZE_PLAYERS = 4

class GamePlay:
    def __init__(self, screen, running):
        self.dimensions = Dimensions(screen)
        self.menu = Menu(self.dimensions)
        self.current_state = 0
        self.nick_inbox_active = None
        self.choice_inbox_active = None #0 - liczba graczy, 1 - majątek pocz, 2 - kwota przy start
        self.players_number = 0
        self.running = running
        self.player = ''
        self.players_created = False
        self.players_singleton = PlayersSingleton()
        self.players = self.players_singleton.players
        self.board_service = BoardService(self.dimensions)
        self.tiles_service = TileService(self.board_service.board, self.dimensions)
        self.current_player_idx = 0
        self.double_rolls = 0
        self.begin_money = 1500
        self.screen = None
        self.turn_active = False
        self.tile_action_finished = None
        self.move_made = False

    def create_players(self, start_money):
        self.players_singleton.clear_players()
        for i in range(self.players_number):
            player = Player(self.menu.users[i][0], self.menu.users[i][1], start_money, self.board_service.start, 0, self.dimensions)
            self.players_singleton.add_player(player)

    def handle_events(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)
        elif event.type == pygame.KEYDOWN:
            self.handle_text_input(event)

    def handle_mouse_click(self, event):
        if self.current_state == GameState.MAIN_MENU.value:
            self.handle_main_menu_click(event)
        elif self.current_state == GameState.NICKNAME_MENU.value:
            self.handle_nick_menu_click(event)
        elif self.current_state == GameState.PERSONALIZE_MENU.value:
            self.handle_personalize_menu_click(event)
        elif self.current_state == GameState.CUSTOMIZE_PLAYERS.value:
            self.handle_nick_menu_click(event)
        elif self.current_state == GameState.GAMEPLAY.value:
            self.handle_gameplay_click(event)

    def handle_main_menu_click(self, event):
        if self.menu.buttons[0].collidepoint(event.pos):
            self.current_state = GameState.NICKNAME_MENU.value
            self.players_number = 2
        elif self.menu.buttons[1].collidepoint(event.pos):
            self.current_state = GameState.PERSONALIZE_MENU.value #okno wyboru liczby graczy, majątku, start_add

    def handle_nick_menu_click(self, event):
        if self.menu.buttons[2].collidepoint(event.pos):
            self.current_state = GameState.GAMEPLAY.value
        else:
            self.check_inbox_click(event)

    def handle_personalize_menu_click(self, event):
        if self.menu.buttons[3].collidepoint(event.pos):
            self.players_number = int(self.menu.personalize_settings[0])
            self.begin_money = int(self.menu.personalize_settings[1])
            self.board_service.start_add = int(self.menu.personalize_settings[2])
            self.current_state = GameState.CUSTOMIZE_PLAYERS.value
        else:
            self.check_inbox_click(event)

    def check_inbox_click(self, event):
        if self.current_state == GameState.NICKNAME_MENU.value or self.current_state == GameState.CUSTOMIZE_PLAYERS.value:
            for i, inbox in enumerate(self.menu.nick_inboxes):
                if inbox.collidepoint(event.pos):
                    self.nick_inbox_active = i
                    self.player = i//2
                    return
        else:
            for i, inbox in enumerate(self.menu.personalize_inboxes):
                if inbox.collidepoint(event.pos):
                    self.choice_inbox_active = i
                    return

    def handle_text_input(self, event):
        if self.current_state == GameState.NICKNAME_MENU.value or self.current_state == GameState.CUSTOMIZE_PLAYERS.value:
            if self.nick_inbox_active is not None:
                self.menu.handle_event(event, self.nick_inbox_active, self.player)
        elif self.current_state == GameState.PERSONALIZE_MENU.value:
            if self.choice_inbox_active is not None:
                self.menu.handle_personalize_settings(event, self.choice_inbox_active)

    def handle_gameplay_click(self, event):
        #self.board_service.handle_click(event)
        if self.board_service.dice.click(event):
            x = self.board_service.board.inner_left_corner[0] + self.board_service.board.inner_width - self.board_service.dice.button_size[0]
            y = self.board_service.board.inner_left_corner[1] + self.board_service.board.inner_width - self.board_service.dice.button_size[1]
            self.board_service.dice.update(self.screen, x, y)
            self.board_service.pending_move = True
            self.turn_active = True
        elif self.tiles_service.handle_buttons(self.board_service.board.tiles[self.board_service.list_number], self.players[self.current_player_idx], event):
            self.tile_action_finished = True
        elif self.tiles_service.handle_buttons2(self.board_service.board.tiles[self.board_service.list_number], self.players[self.current_player_idx], event):
            self.tile_action_finished = True

    def update_gameplay(self, screen):
        if not self.players_created:
            self.create_players(self.begin_money)
            self.board_service.players = self.players
            self.players_created = True

        self.board_service.board.draw(screen)
        self.board_service.draw_players_menus(screen, (self.dimensions.screen_width - self.dimensions.board_width) // 2 * 0.05, self.dimensions.screen_height // 2 * 0.025)
        self.board_service.start_pos(screen)
        self.board_service.draw_button(screen)

        if self.turn_active:
            self.move_made = self.board_service.try_change_pos(self.current_player_idx)
            is_possibility = self.tiles_service.draw_tile_action(self.board_service.board.tiles[self.board_service.list_number], screen, self.players[self.current_player_idx])

            if is_possibility and not self.tile_action_finished: return
            if not is_possibility: self.tile_action_finished = True

            print(self.board_service.board.tiles[self.board_service.list_number].owner, self.players[self.current_player_idx].name, self.tile_action_finished, is_possibility)
            if self.tile_action_finished and not is_possibility and self.board_service.board.tiles[self.board_service.list_number].owner == self.players[self.current_player_idx].name:
                tile = self.board_service.board.tiles[self.board_service.list_number]
                color = getattr(tile, "color", (128, 128, 128))
                self.board_service.players[self.current_player_idx].player_menu.highlight_tile(tile.name, color)

            if self.tile_action_finished:
                if self.board_service.dice.is_double():
                    self.tile_action_finished = False
                    self.turn_active = False
                    self.double_rolls += 1
                    if self.double_rolls < 3:
                        pass
                else:
                    self.double_rolls = 0
                    self.current_player_idx = (self.current_player_idx + 1) % self.players_number
                    self.turn_active = False
                    self.tile_action_finished = False

    def run(self, screen):
        while self.running:
            screen.fill((200, 220, 200))
            self.screen = screen

            for event in pygame.event.get():
                self.handle_events(event)

            match self.current_state:
                case GameState.MAIN_MENU.value:
                    self.menu.draw_menu(screen)
                case GameState.NICKNAME_MENU.value | GameState.CUSTOMIZE_PLAYERS.value:
                    self.menu.create_users_list(self.players_number)
                    self.menu.draw_nick_menu(screen, self.players_number, self.current_state)
                case GameState.GAMEPLAY.value:
                    self.update_gameplay(screen)
                case GameState.PERSONALIZE_MENU.value:
                    self.menu.personalize_game_menu(screen)

            pygame.display.flip()
