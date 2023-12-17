import time
import pygame
from player import Player
from constants import WINNING_COLOR, COORDINATES_GAME_WIN, COORDINATES_GAME_LOSE, COORDINATES_GAME_DRAW


class Game():
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.round = True
        self.player = None
        self.winner = None
        self.font = pygame.font.Font(None, 36)
        self.field = {i: {'occupied': False, 'player': None, 'winning_row': False, 'winning_direction': None} for i in
                      range(1, 10)}
        self.winning_conditions = self.set_conditions()

    def set_conditions(self):
        winning_conditions = []
        for i in range(3):
            winning_conditions.append({'horizontal': [(3 * i + j) for j in range(1, 4)]})
        for i in range(3):
            winning_conditions.append({'vertical': [(i + j + 2 * (j - 1)) for j in range(1, 4)]})
        winning_conditions.append({'diagonal': [(j + (j - 1) * 3) for j in range(1, 4)]})
        winning_conditions.append({'diagonal': [(j + j + 1) for j in range(1, 4)]})
        return winning_conditions

    def game_player_round(self, field_number):
        if self.field[field_number]['occupied'] == False:
            self.round = False
            self.field[field_number]['occupied'] = True
            self.field[field_number]['player'] = self.player
            time.sleep(0.5)

    def game_computer_round(self):
        None

    def win_round(self):
        for condition in self.winning_conditions:
            direction, indices = list(condition.items())[0]
            if all(self.field[index]['occupied'] and self.field[index]['player'] == self.player for index in indices):
                self.winner = self.player
                for index in indices:
                    self.field[index]['winning_row'] = True
                    self.field[index]['winning_direction'] = direction
                return True
        return False

    def draw(self):
        if all(self.field[index]['occupied'] == True and self.field[index]['winning_row'] == False for index in
               self.field):
            return True
        return False

    def display_winner(self, screen):
        if self.winner is not None:
            if self.winner == Player.PLAYER_X.value:
                display_text = self.font.render(f'Congratulations you won!', True, WINNING_COLOR)
                text_coordinates = COORDINATES_GAME_WIN
            elif self.winner == Player.PLAYER_O.value:
                display_text = self.font.render(f'You lost this round.', True, WINNING_COLOR)
                text_coordinates = COORDINATES_GAME_LOSE
        self.display_text(screen, display_text, text_coordinates)

    def display_draw(self, screen):
        display_text = self.font.render('DRAW', True, WINNING_COLOR)
        self.display_text(screen, display_text, COORDINATES_GAME_DRAW)

    def display_text(self, screen, text, coordinates):
        screen.blit(text, coordinates)
        pygame.display.flip()
        self.wait()
        self.reset_game()

    def wait(self):
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False

    def reset_game(self):
        self.round = True
        self.player = None
        self.winner = None
        for key in self.field:
            self.field[key]['occupied'] = False
            self.field[key]['player'] = None
            self.field[key]['winning_row'] = False
            self.field[key]['winning_direction'] = False
