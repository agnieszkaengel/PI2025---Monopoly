import pygame
from board import Board
from dice import Dice
from tile import Tile, Street, Station
from dimensions_generator import Dimensions

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Monopoly Game")


    #street1 = Street("Aleje Ujazdowskie", 1, 100, 130, (255,0,255),100, 20, None)
    #station1 = Station("Dworzec Gdanski", 1, 100, 130, pygame.image.load("Train.png"), 150, 30, None)

    dim = Dimensions(screen)
    board = Board(dim)
    running = True
    screen.fill((255, 255, 255))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

            if event.type == pygame.QUIT:
                running = False
            board.dice.click(screen, board.inner_left_corner[0] + board.inner_width - board.dice.button_size[0], board.inner_left_corner[1] + board.inner_width - board.dice.button_size[1], event)

        board.draw(screen)
        board.dice.update(screen, board.inner_left_corner[0] + board.inner_width - board.dice.button_size[0],
                          board.inner_left_corner[1] + board.inner_width - board.dice.button_size[1])

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()