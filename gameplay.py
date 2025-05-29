
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
    """
    Klasa odpowiada za logikę i pętlę główną rozgrywki oraz przechowywanie jej  parametrów.
    """
    def __init__(self, screen, running):
        """
        Inizjalizuje obiekt GamePlay przypisując wszystkie niezbędne atrybuty.
        :param screen: płaszczyzna ekranu
        :param running: Flaga kontrolująca, czy gra jest w toku.
                        - True: Gra jest aktywna i działa.
                        - False: Gra została zakończona.
        """
        self.dimensions = Dimensions(screen)
        """Obiekt klasy Dimensions przechowujący dynamicznie wyliczone wymiary poszczególnych elementów rozgrywki"""
        self.menu = Menu(self.dimensions)
        """Obiekt klasy Menu odpowiadający za funkcjonalności menu"""
        self.current_state = 0
        """Przechowuje aktualny stan, w którym znajduje się rozgrywka"""
        self.nick_inbox_active = None
        """Przechowuje indeks aktywnego do wpisywania danych okna w menu podawania nicków"""
        self.choice_inbox_active = None #0 - liczba graczy, 1 - majątek pocz, 2 - kwota przy start
        """Przechowuje indeks aktywnego do wpisywania danych okna w menu personalizowanej rozgrywki"""
        self.players_number = 0
        """Przechowuje liczbę graczy uczestniczących w rozgrywce"""
        self.running = running
        """Przechowuje flagę kontorlującą"""
        self.player = ''
        self.players_created = False
        """Flaga przechowująca informację czy lista graczy została już utworzona
                        - True: Lista została utworzona.
                        - False: Lista nie została utworzona."""
        self.players_singleton = PlayersSingleton()
        """Pole inicjalizujące instancję singletona"""
        self.players = self.players_singleton.players
        """Pole przechowujące """
        self.board_service = BoardService(self.dimensions)
        """Obiekt klasy BoardService odpowiadający za obsługę planszy."""
        self.tiles_service = TileService(self.board_service.board, self.dimensions)
        """Obiekt klasy TilesService odpowiadający za obsługę pól."""
        self.current_player_idx = 0
        """Przechowuje indeks gracza z aktualnie aktywną kolejką."""
        self.double_rolls = 0
        """Przechowuje licznik wyrzuconych dubletów w danej kolejce."""
        self.begin_money = 1500
        """Przechowuje wartość majątku początowego graczy: domyślnie 1500."""
        self.screen = None
        """Przechowuje płaszczyznę ekranu."""
        self.turn_active = False
        """Flaga oznaczająca czy tura jest aktywna.
                        - True: tura aktywna.
                        - False: tura nieaktywna"""
        self.tile_action_finished = False
        """Flaga oznaczająca czy akcja dotycząca pola, na którym zatrzymał się pionek zostałą zakończona.
                        - True: akcja zakończona
                        - False: akcja niezakończona"""
        self.move_made = False
        """Flaga oznaczająca czy ruch pionka został wykonany.
                        - True: wykonany
                        - Flase: niewykonany"""

    def create_players(self, start_money):
        """
        Funkcja dodaje graczy do listy graczy.
        :param start_money: Kwota początkowa majątku graczy.
        :return: None
        """
        self.players_singleton.clear_players()
        for i in range(self.players_number):
            player = Player(self.menu.users[i][0], self.menu.users[i][1], start_money, self.board_service.start, 0, self.dimensions)
            self.players_singleton.add_player(player)

    def handle_events(self, event, screen):
        """
        Funkcja rozpoznaje rodzaj eventu i wywołuje odpowiednią funkcję obsługującą ten rodzaj lub zamyka program w przypadku kliknięcia klawisza Q.
        :param event: zdarzenie przechwycone w pętli głównej
        :param screen: płaszczyzna ekranu
        :return: None
        """
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)
        elif event.type == pygame.KEYDOWN:
            self.handle_text_input(event)

    def handle_mouse_click(self, event):
        """
        Funkcja obsługuje kliknięcia myszką podczas różnych stanów gry i wywołuje odpowiednią funkcję do stanu, w którym się znajduje.
        :param event: zdarzenie przechwycone w pętli głównej
        :return: None
        """
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
        """
        Funkcja obsługuje kliknięcia myszką na ekranie głównego menu.
        :param event: zdarzenie przechwycone w pętli głównej
        :return: None
        """
        if self.menu.buttons[0].collidepoint(event.pos):
            self.current_state = GameState.NICKNAME_MENU.value
            self.players_number = 2
        elif self.menu.buttons[1].collidepoint(event.pos):
            self.current_state = GameState.PERSONALIZE_MENU.value #okno wyboru liczby graczy, majątku, start_add

    def handle_nick_menu_click(self, event):
        if self.menu.buttons[2].collidepoint(event.pos) and self.menu.validate_tokens():
            self.current_state = GameState.GAMEPLAY.value
        else:
            self.check_inbox_click(event)

    def handle_personalize_menu_click(self, event):
        """
        Funkcja obsługuje kliknięcia myszką na ekranie menu personalizowanej rozgrywki.
        :param event: zdarzenie przechwycone w pętli głównej
        :return: None
        """
        if self.menu.buttons[3].collidepoint(event.pos) and self.menu.validate_personalization_inputs():
            self.players_number = int(self.menu.personalize_settings[0])
            self.begin_money = int(self.menu.personalize_settings[1])
            self.board_service.start_add = int(self.menu.personalize_settings[2])
            self.current_state = GameState.CUSTOMIZE_PLAYERS.value
        else:
            self.check_inbox_click(event)

    def check_inbox_click(self, event):
        """
        Funkcja sprawdza, które pole do wprowadzania danych zostało kliknięte i aktywuje je.
        :param event: zdarzenie przechwycone w pętli głównej
        :return: None
        """
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
        """
        Funkcja obsługuje wprowadzane przez użytkownika dane tekstowe.
        :param event: zdarzenie przechwycone w pętli głównej
        :return: None
        """
        if self.current_state == GameState.NICKNAME_MENU.value or self.current_state == GameState.CUSTOMIZE_PLAYERS.value:
            if self.nick_inbox_active is not None:
                self.menu.handle_event(event, self.nick_inbox_active, self.player)
        elif self.current_state == GameState.PERSONALIZE_MENU.value:
            if self.choice_inbox_active is not None:
                self.menu.handle_personalize_settings(event, self.choice_inbox_active)

    def handle_gameplay_click(self, event):
        """
        Funkcja obsługuje kliknięcia myszką podczas rozgrywki.
        :param event: zdarzenie przechwycone w pętli głównej
        :return: None
        """
        #self.board_service.handle_click(event)
        if self.board_service.dice.click(event):
            x = self.board_service.board.inner_left_corner[0] + self.board_service.board.inner_width - self.board_service.dice.button_size[0]
            y = self.board_service.board.inner_left_corner[1] + self.board_service.board.inner_width - self.board_service.dice.button_size[1]
            self.board_service.dice.update(self.screen, x, y)
            self.board_service.pending_move = True
            self.turn_active = True
        else:
            handled, flag = self.tiles_service.handle_buttons(self.board_service.board.tiles[self.board_service.list_number], self.players[self.current_player_idx], event)
            if handled:
                match flag:
                    case 0:
                        pass
                    case 1:
                        idx = self.players_singleton.get_player_index(self.board_service.board.tiles[self.board_service.list_number].owner)
                        if self.board_service.board.tiles[self.board_service.list_number].rent_double:
                            self.players[idx].money += self.board_service.board.tiles[self.board_service.list_number].rent * 2
                        else:
                            self.players[idx].money += self.board_service.board.tiles[self.board_service.list_number].rent
                    case 2:
                        self.players[self.current_player_idx].in_prison = False
                    case None:
                        self.players[self.current_player_idx].in_prison = True
                self.tile_action_finished = True


    def prison_check(self):
        if self.players[self.current_player_idx].in_prison:
            self.players[self.current_player_idx].waiting_count += 1
            if self.players[self.current_player_idx].waiting_count >= 3:
                self.players[self.current_player_idx].in_prison = False
                self.players[self.current_player_idx].waiting_count = 0
            self.next_turn()
            return

    def parking_check(self):
        if self.players[self.current_player_idx].in_parking:
            self.players[self.current_player_idx].waiting_count += 1
            if self.players[self.current_player_idx].waiting_count >= 1:
                self.players[self.current_player_idx].in_parking = False
                self.players[self.current_player_idx].waiting_count = 0
            self.next_turn()
            return

    def update_gameplay(self, screen):
        """
        Funkcja aktualizuje stan rozgrywki przy każdym obrocie pętli głównej.
        :param screen: płaszczyzna ekranu
        :return: None
        """
        if not self.players_created:
            self.create_players(self.begin_money)
            self.board_service.players = self.players
            self.players_created = True

        self.board_service.board.draw(screen)
        self.board_service.draw_players_menus(screen, (self.dimensions.screen_width - self.dimensions.board_width) // 2 * 0.05, self.dimensions.screen_height // 2 * 0.025)
        self.board_service.start_pos(screen)
        self.board_service.draw_button(screen)

        if self.tile_action_finished:
            self.prison_check()
            self.parking_check()

        if self.turn_active and not self.players[self.current_player_idx].is_bankrupt:

            self.move_made = self.board_service.try_change_pos(self.current_player_idx)
            print(self.current_player_idx, self.players[self.current_player_idx].tile_index, self.players[self.current_player_idx].in_prison)

            if self.players[self.current_player_idx].tile_index != 10: self.players[self.current_player_idx].in_prison = False
            if self.players[self.current_player_idx].tile_index == 10: self.players[self.current_player_idx].in_prison = True


            is_possibility = self.tiles_service.draw_tile_action(self.board_service.board.tiles[self.board_service.list_number], screen, self.players[self.current_player_idx])


            if self.players[self.current_player_idx].in_prison and self.players[self.current_player_idx].tile_index != 10:
                self.board_service.move_to_prison(self.current_player_idx)

            if is_possibility and not self.tile_action_finished: return
            if not is_possibility: self.tile_action_finished = True

            if self.tile_action_finished and not is_possibility and self.board_service.board.tiles[self.board_service.list_number].owner == self.players[self.current_player_idx].name:
                tile = self.board_service.board.tiles[self.board_service.list_number]
                color = getattr(tile, "color", (128, 128, 128))
                self.board_service.players[self.current_player_idx].player_menu.highlight_tile(tile.name, color)

                number = self.board_service.list_number #numer karty na której zatrzymał się ostatni gracz w ruchu
                tile = self.board_service.board.tiles[number]
                color = tile.color if hasattr(tile, "color") else None # kolor tej karty jeśli istnieje

                #color = self.board_service.board.tiles[number].color #kolor tej karty
                if color is not None:
                    is_complete = self.players[self.current_player_idx].player_menu.check_if_complete(color)
                    print("PO KUPNIE POLA:", is_complete)
                    if is_complete: self.board_service.board.double_rent(color)



            if self.tile_action_finished:
                if self.board_service.dice.is_double():
                    self.tile_action_finished = False
                    self.turn_active = False
                    self.double_rolls += 1
                    if self.double_rolls < 3:
                        pass
                    if self.double_rolls == 3:
                        self.board_service.move_to_prison(self.current_player_idx)
                else:
                    self.double_rolls = 0
                    self.next_turn()


        if self.players_singleton.mark_bankrupt_players() == 1:
                print("Koniec gry")
                self.running = False

        elif self.players[self.current_player_idx].is_bankrupt:
            self.next_turn()




    def next_turn(self):
        self.current_player_idx = (self.current_player_idx + 1) % self.players_number
        self.turn_active = False
        self.tile_action_finished = False

    def run(self, screen):
        """
        Funkcja odpowiada za pętlę główną gry.
        :param screen: płaszczyzna ekranu
        :return: None
        """
        while self.running:
            screen.fill((200, 220, 200))
            self.screen = screen

            for event in pygame.event.get():
                self.handle_events(event, screen)

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
