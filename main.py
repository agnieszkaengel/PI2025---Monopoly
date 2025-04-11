import pygame
from board import Board
from tile import Tile, Street, Station
from dimensions_generator import Dimensions

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Monopoly Game")
    dim = Dimensions(screen)
    board = Board(dim)

    #street1 = Street("Aleje Ujazdowskie", 1, 100, 130, (255,0,255),100, 20, None)
    #station1 = Station("Dworzec Gdanski", 1, 100, 130, pygame.image.load("Train.png"), 150, 30, None)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        board.draw(screen)
        '''
        dim.calculate_all(screen)
        street1.draw(screen, 0, 0)
        station1.draw(screen, station1.width, 0)
        '''
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()