from time import sleep

import pygame
class Tile:
    def __init__(self, name, tile_type, width, height):
        self.name = name
        self.tile_type = tile_type
        self.width = width
        self.height = height

    def draw(self, screen, x, y, rotation):
        if rotation == 0 or rotation == 180:
            pygame.draw.rect(screen, (193, 225, 193), (x,y,self.width,self.height))
            pygame.draw.rect(screen, (0,0,0), (x,y,self.width,self.height), 2)
        elif rotation == -90 or rotation == 90:
            pygame.draw.rect(screen, (193, 225, 193), (x, y, self.width, self.height))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, self.width, self.height), 2)


    def format_name(self, screen, x, y, rotation, text):
        parts = text.split()
        if rotation == 180 or rotation == 0:
            font = pygame.font.SysFont('Arial', int(0.084 * self.height))
        else:
            font = pygame.font.SysFont('Arial', int(0.084 * self.width))
        text_color = (0, 0, 0)

        text1 = font.render(parts[0], True, text_color)
        rotated_text = pygame.transform.rotate(text1, rotation)
        rotated_text_rect = text1.get_rect()
        rotated_text_rect.center = (x, y)
        screen.blit(rotated_text, rotated_text_rect)

        if len(parts) == 2:
            text2 = font.render(parts[1], True, text_color)
            rotated_text = pygame.transform.rotate(text2, rotation)
            rotated_text_rect = text2.get_rect()
            if rotation == 0:
                rotated_text_rect.center = (x,y+0.084 * self.height)
            elif rotation == 180:
                rotated_text_rect.center = (x, y - 0.084 * self.height)
            elif rotation == 90:
                rotated_text_rect.center = (x + 0.084 * self.width, y)
            else:
                rotated_text_rect.center = (x - 0.084 * self.width, y)

            screen.blit(rotated_text, rotated_text_rect)


class Street(Tile):
    def __init__(self, name, tile_type, width, height, color, price, rent, owner):
        super().__init__(name, tile_type, width, height)
        self.color = color
        self.price = price
        self.rent = rent
        self.owner = owner

    def draw(self, screen, x, y, rotation):
        super().draw(screen, x, y, rotation)
        self.draw_color(screen, x, y, rotation)
        self.draw_name(screen, x, y, rotation)
        self.draw_price(screen, x, y, rotation)

    def draw_color(self, screen, x, y, rotation):
        if rotation == 180:
            pygame.draw.rect(screen, self.color, (x, y + 0.79 * self.height, self.width, 0.21 * self.height))
            pygame.draw.rect(screen, (0, 0, 0), (x, y + 0.79 * self.height, self.width, 0.21 * self.height), 2)
        elif rotation == 90:
            pygame.draw.rect(screen, self.color, (x, y, 0.21 * self.width, self.height))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 0.21 * self.width, self.height), 2)
        elif rotation == 0:
            pygame.draw.rect(screen, self.color, (x, y, self.width, 0.21 * self.height))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, self.width, 0.21 * self.height), 2)
        elif rotation == -90:
            pygame.draw.rect(screen, self.color, (x + 0.79 * self.width, y, 0.21 * self.width, self.height))
            pygame.draw.rect(screen, (0, 0, 0), (x + 0.79 * self.width, y, 0.21 * self.width, self.height), 2)

    def draw_name(self, screen, x, y, rotation):
        if rotation == 180:
            super().format_name(screen, x + self.width / 2, y + 0.65 * self.height, rotation, self.name)
        elif rotation == 0:
            super().format_name(screen, x + self.width / 2, y + 0.35 * self.height, rotation, self.name)
        elif rotation == -90:
            super().format_name(screen, x + 0.65 * self.width, y - 5 + self.height / 2 , rotation, self.name)
        elif rotation == 90:
            super().format_name(screen, x + 0.4 * self.width , y - 5 + self.height / 2, rotation, self.name)

    def draw_price(self, screen, x, y, rotation):
        if rotation == 180:
            super().format_name(screen, x + self.width / 2, y + 0.2 * self.height, rotation, str(self.price))
        elif rotation == 0:
            super().format_name(screen, x + self.width / 2, y + 0.8 * self.height, rotation, str(self.price))
        elif rotation == -90:
            super().format_name(screen, x + 0.2 * self.width, y + 0.45 * self.height, rotation, str(self.price))
        elif rotation == 90:
            super().format_name(screen, x + 0.8 * self.width , y + self.height * 0.45, rotation, str(self.price))


class Station(Tile):
    def __init__(self, name, tile_type, width, height, image, price, rent, owner):
        super().__init__(name, tile_type, width, height)
        self.image = image
        self.price = price
        self.rent = rent
        self.owner = owner
        self.image_place = ((0.125*self.width), (0.3*self.height))

    def draw(self, screen, x, y, rotation):
        super().draw(screen, x, y, rotation)
        self.draw_price(screen, x, y, rotation)
        self.draw_name(screen, x, y, rotation)



    def draw_name(self, screen, x, y, rotation):
        if rotation == 180:
            super().format_name(screen, x + self.width / 2, y + 0.9 * self.height, rotation, self.name)
        elif rotation == 0:
            super().format_name(screen, x + self.width / 2, y + 0.1 * self.height, rotation, self.name)
        elif rotation == -90:
            super().format_name(screen, x + 0.9 * self.width, y - 5 + self.height / 2, rotation, self.name)
        elif rotation == 90:
            super().format_name(screen, x + 0.15 * self.width, y - 5 + self.height / 2, rotation, self.name)

    def draw_price(self, screen, x, y, rotation):
        if rotation == 180:
            super().format_name(screen, x + self.width / 2, y + 0.2 * self.height, rotation, str(self.price))
        elif rotation == 0:
            super().format_name(screen, x + self.width / 2, y + 0.8 * self.height, rotation, str(self.price))
        elif rotation == -90:
            super().format_name(screen, x + 0.2 * self.width, y + 0.45 * self.height, rotation, str(self.price))
        elif rotation == 90:
            super().format_name(screen, x + 0.8 * self.width, y + self.height * 0.45, rotation, str(self.price))


class Action(Tile):
    def __init__(self, name, tile_type, width, height, image):
        super().__init__(name, tile_type, width, height)
        self.image = image
    '''
    def draw(self, screen, x, y):
        super().draw(screen, x, y)
        '''


