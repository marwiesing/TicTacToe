# game_manager.py
import pygame

from constants import X, Y, WIDTH, HEIGHT, ROWS, COLUMNS, GAME_COLOUR
from game import Game
from gameboard import Gameboard
from player import Player, WINNER
from constants import WINNING_COLOR, COORDINATES_GAME_WIN, COORDINATES_GAME_LOSE, COORDINATES_GAME_DRAW, \
    COORDINATES_CONTINUE

class GameManager:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 36)
        self.game = Game()
        self.gameboard = Gameboard(self.game, screen, X, Y, WIDTH, HEIGHT, ROWS, COLUMNS)

    def run_game_loop(self):
        RUNNING = True
        while RUNNING:
            if self.game.winner is None:
                if self.game.check_if_game_ended():
                    if self.game.winner == Player.PLAYER_X.value:
                        self.game.player_score += 1
                    elif self.game.winner == Player.PLAYER_O.value:
                        self.game.computer_score += 1
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            RUNNING = False
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            self.handle_player_click(event.pos)
                        elif self.game.round == False and self.game.first_round:
                            self.game.process_first_round()
                        elif self.game.round == False and not self.game.first_round:
                            self.handle_computer_move()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.game.reset_game()

            self.update_display()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_player_click(self, pos):
        x, y = pos
        field_number = self.gameboard.get_field_number(x, y)
        if field_number is not None and self.game.round:
            self.game.process_player_move(field_number)

    def handle_computer_move(self):
        self.game.process_computer_move()

    def update_display(self):
        self.screen.fill(GAME_COLOUR)
        self.gameboard.draw_game_field()
        self.gameboard.draw_xo()
        self.gameboard.score()
        self.display_end_result()

    def display_end_result(self):
        if self.game.winner is not None:
            text = None
            text_coordinates = None
            drawWinningRow = False
            if self.game.winner == WINNER.PLAYER_X.value:
                text = 'Congratulations you won!'
                text_coordinates = COORDINATES_GAME_WIN
                drawWinningRow = True
            elif self.game.winner == WINNER.PLAYER_O.value:
                text = 'You lost this round.'
                text_coordinates = COORDINATES_GAME_LOSE
                drawWinningRow = True
            elif self.game.winner == WINNER.DRAW.value:
                text = 'DRAW!'
                text_coordinates = COORDINATES_GAME_DRAW
            if text and text_coordinates:
                self.display_text(self.screen, text, text_coordinates)
            if drawWinningRow:
                self.gameboard.draw_winning_row()

    def display_text(self, screen, text, coordinates):
        display_text = self.font.render(text, True, WINNING_COLOR)
        screen.blit(display_text, coordinates)
        continue_text = self.font.render('Click to continue.', True, WINNING_COLOR)
        screen.blit(continue_text, COORDINATES_CONTINUE)