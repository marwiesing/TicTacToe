import pygame
from gameboard import Gameboard
from game import Game
from constants import RUNNING, X, Y, WIDTH, HEIGHT, ROWS, COLUMNS, GAME_COLOUR

pygame.init()
pygame.display.set_caption('Tic Tac Toe')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


game = Game()
gameboard = Gameboard(game, screen, X, Y, WIDTH, HEIGHT, ROWS, COLUMNS)

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                print(f"Mouse click at coordinates ({x}, {y})")
                field_number = gameboard.get_field_number(x, y)
                if field_number is not None:
                    #print(f"Mouse click in field {field_number}")
                    game.set_icon(field_number)


    screen.fill(GAME_COLOUR)
    gameboard.draw()
    gameboard.game_action()
    gameboard.score()

    if game.win_round():
        game.winner = game.player
        gameboard.draw_winning_row()
        game.display_winner(screen)
        if game.player == 1:
            game.player_score += 1
        else:
            game.computer_score += 1
        game.reset_game()

    pygame.display.flip()
    clock.tick(60)


pygame.quit()