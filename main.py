import pygame
from dimensions_generator import Dimensions
from board_service import BoardService
from menu import Menu
from gameplay import GamePlay


def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Monopoly Game")
    running = True
    gameplay = GamePlay(screen, running)

    gameplay.run(screen)
    pygame.quit()

if __name__ == "__main__":
    main()