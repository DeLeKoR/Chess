import sys
from chess_items import *

clock = pygame.time.Clock()
chessboard = Chessboard(8, 90)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            chessboard.btn_down(event.button, event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 6:
                chessboard = Chessboard(8, 90)
            chessboard.btn_up(event.button, event.pos)
        if event.type == pygame.MOUSEMOTION:
            chessboard.drag(event.pos)
    clock.tick(FPS)
    pygame.display.flip()
