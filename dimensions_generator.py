import pygame

S_P = 1

class Dimensions:
   def __init__(self, screen):
       self.calculate_all(screen)

   screen_width = None
   screen_height = None
   board_width = None
   board_left_corner = (None,None)
   tile_width = None
   tile_height = None
   font_size = None


   def get_dimensions(self):
       info = pygame.display.Info()
       self.screen_width = info.current_w
       self.screen_height = info.current_h

   def calculate_board_size(self, screen):
       # self.get_dimensions()
       if self.screen_width > self.screen_height:
           self.board_width = S_P*self.screen_height
       else:
           self.board_width = S_P*self.screen_width

       x_start = (self.screen_width-self.board_width)/2
       y_start = (self.screen_height-self.board_width)/2
       self.board_left_corner = x_start, y_start
       #pygame.draw.rect(screen, (193, 225, 193), (x_start, y_start, self.board_width, self.board_width))

   def calculate_tile_size(self):
       self.tile_width = 0.0818 * self.board_width
       self.tile_height = 0.1319 * self.board_width
       self.font_size = 0.084 * self.tile_height

   def calculate_all(self, screen):
       self.get_dimensions()
       self.calculate_board_size(screen)
       self.calculate_tile_size()
