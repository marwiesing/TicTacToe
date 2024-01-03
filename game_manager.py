import pygame
from gameboard import Gameboard
from game import Game
from player import Player
from constants import RUNNING, X, Y, WIDTH, HEIGHT, ROWS, COLUMNS, GAME_COLOUR

class GameManager:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.game = Game()
        self.gameboard = Gameboard(self.game, screen, X, Y, WIDTH, HEIGHT, ROWS, COLUMNS)

    def run_game_loop(self):
        global RUNNING
        while RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_player_click(event.pos)
                elif self.game.round == False and self.game.first_round:
                    self.game.process_first_round()

            self.update_display()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_player_click(self, pos):
        x, y = pos
        field_number = self.gameboard.get_field_number(x, y)
        if field_number is not None and self.game.round:
            self.game.process_player_move(field_number)
        elif not self.game.round:
            self.handle_computer_move(field_number)

    def handle_computer_move(self, field_number):
        #self.game.process_computer_move()
        self.game.game_player_round(field_number)

    def update_display(self):
        self.screen.fill(GAME_COLOUR)
        self.gameboard.draw_game_field()
        self.gameboard.draw_xo()
        self.gameboard.score()

        if self.game.win_round():
            self.handle_winner()
        elif self.game.draw():
            self.game.display_draw(self.screen)

    def handle_winner(self):
        if self.game.winner == Player.PLAYER_X.value:
            self.game.player_score += 1
        elif self.game.winner == Player.PLAYER_O.value:
            self.game.computer_score += 1
        self.gameboard.draw_winning_row()
        self.game.display_winner(self.screen)