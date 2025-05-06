import pygame
class Tile:
    def __init__(self, name, tile_type, width, height, index):
        self.name = name
        self.tile_type = tile_type
        self.width = width
        self.height = height
        self.index = index
        self.owner = None
        if self.width<self.height:
            self.font = 0.084 * self.height
        else:
            self.font = 0.084 * self.width

    def draw(self, screen, x, y, rotation):
        if rotation == 0 or rotation == 180:
            pygame.draw.rect(screen, (193, 225, 193), (x+1,y+1,self.width-1,self.height-1))
            pygame.draw.rect(screen, (0,0,0), (x,y,self.width,self.height), 2)
        elif rotation == -90 or rotation == 90:
            pygame.draw.rect(screen, (193, 225, 193), (x+1, y+1, self.width-1, self.height-1))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, self.width, self.height), 2)


    def format_text(self, screen, x, y, rotation, text):
        parts = text.split()
        font = pygame.font.SysFont('Arial', int(self.font))
        text_color = (0, 0, 0)

        text1 = font.render(parts[0], True, text_color)
        rotated_text = pygame.transform.rotate(text1, rotation)
        rotated_text_rect = rotated_text.get_rect()
        rotated_text_rect.center = (x, y)
        screen.blit(rotated_text, rotated_text_rect)

        if len(parts) == 2 or len(parts) == 3:
            text2 = font.render(parts[1], True, text_color)
            rotated_text = pygame.transform.rotate(text2, rotation)
            rotated_text_rect = rotated_text.get_rect()
            if rotation == 0:
                rotated_text_rect.center = (x, y + self.font)
            elif rotation == 180:
                rotated_text_rect.center = (x, y - self.font)
            elif rotation == 90:
                rotated_text_rect.center = (x + self.font, y)
            else:
                rotated_text_rect.center = (x - self.font, y)

            screen.blit(rotated_text, rotated_text_rect)

        if len(parts) == 3:
            text3 = font.render(parts[2], True, text_color)
            rotated_text = pygame.transform.rotate(text3, rotation)
            rotated_text_rect = rotated_text.get_rect()
            if rotation == 0:
                rotated_text_rect.center = (x, y + 2*self.font)
            elif rotation == 180:
                rotated_text_rect.center = (x, y - 2*self.font)
            elif rotation == 90:
                rotated_text_rect.center = (x + 2*self.font, y)
            else:
                rotated_text_rect.center = (x - 2*self.font, y)

            screen.blit(rotated_text, rotated_text_rect)

    def draw_text(self, screen, x, y, rotation, param1, param2, text):
        if rotation == 180:
            self.format_text(screen, x + self.width / 2, y + param1 * self.height - 4, rotation, text)
        elif rotation == 0:
            self.format_text(screen, x + self.width / 2, y + param2 * self.height, rotation, text)
        elif rotation == -90:
            self.format_text(screen, x + param1 * self.width, y + self.height / 2 , rotation, text)
        elif rotation == 90:
            self.format_text(screen, x + param2 * self.width , y + self.height / 2, rotation, text)


class Street(Tile):
    def __init__(self, name, tile_type, width, height, color, price, rent, index, owner):
        super().__init__(name, tile_type, width, height, index)
        self.color = color
        self.price = price
        self.rent = rent
        self.owner = owner

    def draw(self, screen, x, y, rotation):
        super().draw(screen, x, y, rotation)
        self.draw_color(screen, x, y, rotation)
        self.draw_text(screen, x, y, rotation, 0.65, 0.35, self.name)
        self.draw_text(screen, x, y, rotation, 0.2, 0.8, str(self.price))

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
            pygame.draw.rect(screen, self.color, (x + 0.79 * self.width, y , 0.21 * self.width, self.height))
            pygame.draw.rect(screen, (0, 0, 0), (x + 0.79 * self.width, y, 0.21 * self.width, self.height), 2)


class Station(Tile):
    def __init__(self, name, tile_type, width, height, image, price, rent, index, owner):
        super().__init__(name, tile_type, width, height, index)
        self.image = image
        self.price = price
        self.rent = rent
        self.owner = owner
        #self.image_place = ((0.125*self.width), (0.3*self.height))

    def draw(self, screen, x, y, rotation):
        super().draw(screen, x, y, rotation)
        self.draw_text(screen, x, y, rotation, 0.2, 0.8, str(self.price))
        self.draw_text(screen, x, y, rotation, 0.9, 0.1, self.name)

        image = pygame.image.load(self.image).convert_alpha()
        rot_image = pygame.transform.rotate(image, rotation)
        if rotation == 180 or rotation == 0:
            rot_image = pygame.transform.scale(rot_image, (self.width*0.5, self.width*0.5))
        else:
            rot_image = pygame.transform.scale(rot_image, (self.height * 0.5, self.height * 0.5))
        image_rect = rot_image.get_rect(center=(x + self.width // 2, y + self.height // 2))
        screen.blit(rot_image, image_rect)


class Action(Tile):
    def __init__(self, name, tile_type, width, height, image, index):
        super().__init__(name, tile_type, width, height, index)
        self.image = image

    def draw(self, screen, x, y, rotation):
        super().draw(screen, x, y, rotation)
        if self.name == "START":
            self.draw_text(screen, x, y, 0, 0.2, 0.2, self.name)
        elif self.name == "PARKING":
            self.draw_text(screen, x, y, 180, 0.9, 0.9, self.name)
        elif self.name == "IDZ DO WIEZIENIA":
            self.draw_text(screen, x, y, 0, 0.1, 0.1, self.name)
        else:
            self.draw_text(screen, x, y, rotation, 0.9, 0.1, self.name)


        image = pygame.image.load(self.image).convert_alpha()
        rot_image = pygame.transform.rotate(image, rotation)
        if rotation == 180 or rotation == 0:
            rot_image = pygame.transform.scale(rot_image, (self.width * 0.5, self.width * 0.5))
        else:
            rot_image = pygame.transform.scale(rot_image, (self.height * 0.5, self.height * 0.5))
        image_rect = rot_image.get_rect(center=(x + self.width // 2, y + self.height // 2))
        screen.blit(rot_image, image_rect)




