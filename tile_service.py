from board import Board
import pygame
from player import Player
from dimensions_generator import Dimensions
from tile import Tile
import json
import random
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
        self.kasa_spol = []
        self.szansa = []
        self.card_used = True
        self.random = None
        self.load_kasa_and_szansa()
        self.pledge_input_active = False
        self.pledge_input_text = ""
        self.pledge_inbox = pygame.Rect(
            self.window_place[0]*1.11,
            self.window_place[1] + self.window_size[1] * 0.3,
            0.75*self.window_size[0],
            0.2*self.window_size[1]
        )


    def create_buttons_list(self):
        self.buttons.append(pygame.Rect(self.window_place[0]+self.button_size[0]*0.5, self.window_place[1]+self.window_size[1]*0.6, self.button_size[0], self.button_size[1]))
        self.buttons.append(pygame.Rect(self.window_place[0]+self.button_size[0]*1.5, self.window_place[1]+self.window_size[1]*0.6, self.button_size[0], self.button_size[1]))
        #self.buttons.append(pygame.Rect((self.window_place[0] + self.button_size[0] * 0.1, self.window_place[1] + self.window_size[1] * 0.6, self.button_size[0]*1.4, self.button_size[1])))
        #self.buttons.append(pygame.Rect((self.window_place[0] + self.button_size[0] * 1.5, self.window_place[1] + self.window_size[1] * 0.6, self.button_size[0]*1.4, self.button_size[1])))

    def draw_tile_action(self, tile: Tile, screen, player: Player):
            match tile.tile_type:
                case "Action":
                    match tile.name:
                        #case "WIEZIENIE":
                            #player.in_prison = True
                            #return True
                            #return self.buying_window(screen, tile, player)
                        #case "PARKING":
                            #player.in_parking = True
                            #return True
                        #case "IDZ DO WIEZIENIA":
                            #player.in_prison = True
                            #return True
                            #return self.buying_window(screen, tile, player)
                        case "Kasa Spoleczna":
                            self.show_card(screen, 0)
                            return True
                        case "Szansa":
                            self.show_card(screen, 1)
                            return True

                    return False
                case "Station" | "Street":
                    return self.buying_window(screen, tile, player)

    def street_service(self):
        pass

    def station_service(self):
        pass

    def buying_window(self, screen, tile, player):
        #if player.in_prison:
            #self.draw_prison_menu(screen, player.name)
            #return True
        if tile.owner is None and not self.buying_finished and not player.in_prison:
            self.draw_buy_menu(screen, tile, player.name)
            return True #czy jest mozliwosc akcji - czy czekamy na klikniecie jakiegos przycisku
            #return self.handle_buttons(tile, player, event)
        elif tile.owner is not None and tile.owner != player.name and not player.in_prison:
            self.draw_rent_menu(screen, tile, player.name)
            #self.handle_buttons2(tile, player, event)
            return True
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
                if self.pledge_input_active:
                   self.pledge_input_active = False
                   return True, 4 # 4 - zastawienie do banku

                #elif tile.name == 'WIEZIENIE':
                    #player.money -= 50
                    #return True, 2 # 2 - wybór przy wiezieniu

                elif tile.name == 'Kasa Spoleczna':
                    if self.kasa_spol[self.random]["rodzaj"] == 1:
                        player.money += int(self.kasa_spol[self.random]["kwota_zysku"])
                    else:
                        player.money -= int(self.kasa_spol[self.random]["kwota_straty"])

                    if player.money < 0: player.money = 0
                    return True, 3 # 3 - wybór przy kasie spolecznej i szansie

                elif tile.name == 'Szansa':
                    if self.kasa_spol[self.random]["rodzaj"] == 1:
                        player.money += int(self.szansa[self.random]["kwota_zysku"])
                    else:
                        player.money -= int(self.szansa[self.random]["kwota_straty"])

                    if player.money < 0: player.money = 0
                    return True, 3 # 3 - wybór przy kasie spolecznej i szansie

                elif tile.owner is None: #and player.money >= tile.price:
                    tile.owner = player.name
                    player.money -= tile.price
                    if player.money < 0: player.money = 0
                    return True, 0 # 0 - kupowanie nieruchomości
                elif tile.owner is not None:# and player.money >= tile.rent:
                    if tile.rent_double:
                        player.money -= 2*tile.rent
                    else:
                        player.money -= tile.rent
                    if player.money < 0: player.money = 0
                    return True, 1 # 1 - opłata czynszu
                else:
                    return True, 0

            elif self.buttons[1].collidepoint(event.pos):
                #if tile.name == 'WIEZIENIE':
                #    return True, 5
                #elif tile.owner is not None:
                 #   return True, 6
                #else:
                return True, 0

            else:
                return True, 0



    def draw_rent_menu(self, screen, tile, name):
        pygame.draw.rect(screen, (193, 225, 193),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1))
        pygame.draw.rect(screen, (0, 0, 0),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1),2)
        text1 = name + "  Musisz opłacić czynsz graczowi: " + tile.owner

        if tile.rent_double:
            rent = tile.rent * 2
        else:
            rent = tile.rent

        text2 = "WYSOKOŚĆ CZYNSZU " + str(rent) + " ZŁ"
        font = pygame.font.SysFont('Arial', int(self.font_size), True)
        text_color = (0, 0, 0)
        text1 = font.render(str(text1), True, text_color)
        text2 = font.render(str(text2), True, text_color)
        text_rect = text1.get_rect(center=(self.window_place[0] + self.window_size[0] // 2, self.window_place[1] + self.window_size[1] * 0.1))
        screen.blit(text1, text_rect)
        text_rect = text2.get_rect(center=(self.window_place[0] + self.window_size[0] // 2,self.window_place[1] + self.window_size[1] * 0.1 + self.font_size * 2))
        screen.blit(text2, text_rect)

        rect = pygame.draw.rect(screen, (120, 180, 120), (self.window_place[0] + self.button_size[0] * 0.1, self.window_place[1] + self.window_size[1] * 0.6, self.button_size[0]*1.4, self.button_size[1]))
        text_tak = font.render('OPŁAĆ GOTÓWKĄ', True, (0, 0, 0))
        text_tak_rect = text_tak.get_rect(center=rect.center)

        '''
        rect = pygame.draw.rect(screen, (200, 100, 100), (
        self.window_place[0] + self.button_size[0] * 1.5, self.window_place[1] + self.window_size[1] * 0.6, self.button_size[0]*1.4, self.button_size[1]))
        text_nie = font.render('ZASTAW NIERUCHOMOŚĆ', True, (0, 0, 0))
        text_nie_rect = text_nie.get_rect(center=rect.center)
        screen.blit(text_nie, text_nie_rect)
        '''

        screen.blit(text_tak, text_tak_rect)



    def draw_prison_menu(self, screen, name):
        pygame.draw.rect(screen, (193, 225, 193),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1))
        pygame.draw.rect(screen, (0, 0, 0),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1),2)
        text1 = name + "Czy chcesz wykupić się z więzenia?"
        text2 = "KOSZT: 50 ZŁ"

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
        '''
        pygame.draw.rect(screen, (200, 100, 100), (self.window_place[0]+self.button_size[0]*1.5, self.window_place[1]+self.window_size[1]*0.6, self.button_size[0], self.button_size[1]))
        text_nie = font.render('NIE', True, (0, 0, 0))
        text_nie_rect = text_nie.get_rect(center=self.buttons[1].center)
        screen.blit(text_nie, text_nie_rect)
        '''
        screen.blit(text_tak, text_tak_rect)


    def load_kasa_and_szansa(self):
        with open("karty_kasa_spoleczna.json", "r", encoding="utf-8") as f:
            tile_data = json.load(f)
        for tile in tile_data:
            self.kasa_spol.append({ "rodzaj": tile["rodzaj_karty"], "kwota_zysku": tile["kwota_zysku"], "kwota_straty": tile["kwota_straty"], "tekst": tile["tekst"]})

        with open("karty_szansa.json", "r", encoding="utf-8") as f:
            tile_data = json.load(f)
        for tile in tile_data:
            self.szansa.append({"rodzaj": tile["rodzaj_karty"], "kwota_zysku": tile["kwota_zysku"],"kwota_straty": tile["kwota_straty"], "tekst": tile["tekst"]})


    def show_card(self, screen, t):
        if self.card_used:
            self.give_random_card(t)
            self.card_used = False

        if t == 0:
            text = self.kasa_spol[self.random]["tekst"]
            typ = self.kasa_spol[self.random]["rodzaj"]
            self.draw_card(text, "KASA SPOŁECZNA", screen, typ)
        elif t == 1:
            text = self.szansa[self.random]["tekst"]
            typ = self.szansa[self.random]["rodzaj"]
            self.draw_card(text, "SZANSA", screen, typ)


    def give_random_card(self, type):
        if type == 0: x = 13
        else: x = 9
        self.random = random.randint(0, x)


    def wypisz_tekst_w_linijkach(self, screen, font, text, text_color, start_x, start_y, font_size, slowa_na_linie=6):
        slowa = text.split()
        for i in range(0, len(slowa), slowa_na_linie):
            linia = ' '.join(slowa[i:i + slowa_na_linie])
            text_surface = font.render(linia, True, text_color)
            text_rect = text_surface.get_rect(center=(start_x, start_y + i // slowa_na_linie * int(font_size * 1.5)))
            screen.blit(text_surface, text_rect)

    def draw_card(self, text, title, screen, typ):
        pygame.draw.rect(screen, (193, 225, 193),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1))
        pygame.draw.rect(screen, (0, 0, 0),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1),2)


        font = pygame.font.SysFont('Arial', int(self.font_size), True)
        text_color = (0, 0, 0)
        self.wypisz_tekst_w_linijkach(
            screen=screen,
            font=font,
            text=str(text),
            text_color=text_color,
            start_x=self.window_place[0] + self.window_size[0] // 2,
            start_y=self.window_place[1] + self.window_size[1] * 0.1 + 2 * int(self.font_size),
            font_size=self.font_size
        )

        '''
        text1 = font.render(str(text), True, text_color)
        text_rect = text1.get_rect(center=(self.window_place[0] + self.window_size[0] // 2, self.window_place[1] + self.window_size[1] * 0.1+2*int(self.font_size)))
        screen.blit(text1, text_rect)
        '''

        title1 = font.render(str(title), True, text_color)
        text_rect = title1.get_rect(center=(self.window_place[0] + self.window_size[0] // 2, self.window_place[1] + self.window_size[1] * 0.1))
        screen.blit(title1, text_rect)

        if typ == 2: #zysk
            rect = pygame.draw.rect(screen, (120, 180, 120), (self.window_place[0] + self.button_size[0] * 0.1, self.window_place[1] + self.window_size[1] * 0.6,
                self.button_size[0] * 1.4, self.button_size[1]))
            text_tak = font.render('OPŁAĆ GOTÓWKĄ', True, (0, 0, 0))
            text_tak_rect = text_tak.get_rect(center=rect.center)

            '''
            rect = pygame.draw.rect(screen, (200, 100, 100), (self.window_place[0] + self.button_size[0] * 1.5, self.window_place[1] + self.window_size[1] * 0.6,
                self.button_size[0] * 1.4, self.button_size[1]))
            text_nie = font.render('ZASTAW NIERUCHOMOŚĆ', True, (0, 0, 0))
            text_nie_rect = text_nie.get_rect(center=rect.center)
            screen.blit(text_nie, text_nie_rect)
            '''

            screen.blit(text_tak, text_tak_rect)

        else:
            rect = pygame.draw.rect(screen, (120, 180, 120), (
            self.window_place[0] + self.button_size[0] * 0.1, self.window_place[1] + self.window_size[1] * 0.6,
            self.button_size[0] * 1.4, self.button_size[1]))
            text_tak = font.render('OK', True, (0, 0, 0))
            text_tak_rect = text_tak.get_rect(center=rect.center)
            screen.blit(text_tak, text_tak_rect)

    def draw_pledge_menu(self, screen, name):
        pygame.draw.rect(screen, (193, 225, 193),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1))
        pygame.draw.rect(screen, (0, 0, 0),(self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1),2)

        font = pygame.font.SysFont('Arial', int(self.font_size), True)
        text_color = (0, 0, 0)

        title1 = font.render(str(name) + str(": ZASTAWIENIE NIERUCHOMOŚCI"), True, text_color)
        text_rect = title1.get_rect(center=(self.window_place[0] + self.window_size[0] // 2, self.window_place[1] + self.window_size[1] * 0.1))
        screen.blit(title1, text_rect)

        text1 = font.render(str("Podaj nazwę nieruchomości do zastawienia:"), True, text_color)
        text_rect = text1.get_rect(
            center=(self.window_place[0] + self.window_size[0] // 2, self.window_place[1] + self.window_size[1] * 0.1+int(self.font_size)))
        screen.blit(text1, text_rect)

        # Pole tekstowe
        box_color = (255, 255, 255) if self.pledge_input_active else (193, 225, 193)
        pygame.draw.rect(screen, box_color, self.pledge_inbox, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.pledge_inbox, 2)

        # Wpisany tekst
        input_surface = font.render(self.pledge_input_text, True, (0, 0, 0))
        screen.blit(input_surface, (self.pledge_inbox.x + 5, self.pledge_inbox.y + 5))

        rect = pygame.draw.rect(screen, (120, 180, 120), (
        self.window_place[0] + self.button_size[0] * 0.1, self.window_place[1] + self.window_size[1] * 0.6,
        self.button_size[0] * 1.4, self.button_size[1]))
        text_tak = font.render('ZASTAW', True, (0, 0, 0))
        text_tak_rect = text_tak.get_rect(center=rect.center)
        screen.blit(text_tak, text_tak_rect)
        '''
        rect = pygame.draw.rect(screen, (200, 100, 100), (
        self.window_place[0] + self.button_size[0] * 1.5, self.window_place[1] + self.window_size[1] * 0.6,
        self.button_size[0] * 1.4, self.button_size[1]))
        text_nie = font.render('NIE CHCĘ', True, (0, 0, 0))
        text_nie_rect = text_nie.get_rect(center=rect.center)
        screen.blit(text_nie, text_nie_rect)
        '''

    def click(self, event):
        print("CLICK")
        if event.type == pygame.KEYDOWN and self.pledge_input_active:
            print("KEYDOWN")
            if event.key == pygame.K_BACKSPACE:
                self.pledge_input_text = self.pledge_input_text[:-1]
            else:
                self.pledge_input_text += event.unicode


    def end_screen(self, screen, name):
        pygame.draw.rect(screen, (193, 225, 193),
                         (self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1))
        pygame.draw.rect(screen, (0, 0, 0),
                         (self.window_place[0], self.window_place[1], self.window_size[0] - 1, self.window_size[1] - 1),
                         2)

