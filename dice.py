import pygame, random, time
class Dice:
    def __init__(self, width, height, font):
        self.button_size = (width, height)
        self.dice_size = width*0.5
        self.font_size = font
        self.button = None
        self.num1, self.num2 = 0,0
        self.showing_dice = False
        self.show_start_time = None

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.collidepoint(event.pos):
                self.random_number()
                self.show_start_time = time.time()
                self.showing_dice = True
                return True
        return False

    def draw_button (self, screen, x, y):
            pygame.draw.rect(screen, (193, 225, 193), (x, y, self.button_size[0], self.button_size[1]))
            pygame.draw.rect(screen, (0,0,0), (x, y, self.button_size[0], self.button_size[1]), 2)
            self.button = pygame.Rect(x, y, self.button_size[0], self.button_size[1])
            text = "RZUĆ KOSTKAMI"
            text_color = (0, 0, 0)
            font = pygame.font.SysFont('Arial', int(self.font_size), True)
            text = font.render(text, True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (x+self.button_size[0]/2, y+self.button_size[1]/2)
            screen.blit(text, text_rect)
            #self.click(screen, x, y, event)

    def random_number(self):
        self.num1 = random.randint(1,6)
        self.num2 = random.randint(1,6)

    def show_dice(self, screen, x, y):
            name1 = str(self.num1) + ".png"
            name2 = str(self.num2) + ".png"
            name1 = f"images/{name1}"
            name2 = f"images/{name2}"

            image1 = pygame.image.load(name1).convert_alpha()
            image1 = pygame.transform.scale(image1, (self.dice_size, self.dice_size))

            image2 = pygame.image.load(name2).convert_alpha()
            image2 = pygame.transform.scale(image2, (self.dice_size, self.dice_size))

            image_rect1 = image1.get_rect(center=(x+self.dice_size//2, y-self.button_size[1]))
            image_rect2 = image2.get_rect(center=(x + self.dice_size*1.5, y-self.button_size[1]))

            screen.blit(image1, image_rect1)
            screen.blit(image2, image_rect2)

    def update(self, screen, x, y):
        if self.showing_dice:
            current_time = time.time()
            if current_time - self.show_start_time <= 5:
                pygame.draw.rect(screen, (200, 220, 200), (x, y, self.button_size[0], self.button_size[1]))  # wyczyść tło
                self.show_dice(screen, x, y)
            else:
                pygame.draw.rect(screen, (200, 220, 200),(x, y-self.button_size[1], self.button_size[0], self.button_size[1]*2))  # wyczyść tło
                self.showing_dice = False
                self.draw_button(screen, x, y)

    def get_sum(self):
        return self.num1+self.num2

    def is_double(self):
        return self.num1 == self.num2