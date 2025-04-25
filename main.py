import pygame
from dimensions_generator import Dimensions
from board_service import BoardService

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Monopoly Game")


    #street1 = Street("Aleje Ujazdowskie", 1, 100, 130, (255,0,255),100, 20, None)
    #station1 = Station("Dworzec Gdanski", 1, 100, 130, pygame.image.load("Train.png"), 150, 30, None)

    dim = Dimensions(screen)
    board_service = BoardService(dim)
    running = True
    screen.fill((255, 255, 255))

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board_service.handle_click(screen, event)
            #board_service.dice.click(screen, board_service.board.inner_left_corner[0] + board_service.board.inner_width - board_service.dice.button_size[0], board_service.board.inner_left_corner[1] + board_service.board.inner_width - board_service.dice.button_size[1], event)


        board_service.board.draw(screen)
        board_service.start_pos(screen)  # rysuj gracza tylko z aktualną pozycją
        board_service.update(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()