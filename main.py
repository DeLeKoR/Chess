import sys
from options import *
from chess_items import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE))
pygame.display.set_caption("Шахматы")
screen.fill(BACKGROUND)
clock = pygame.time.Clock()

chessbord = Chessboard(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    clock.tick(FPS)
    pygame.display.flip()
