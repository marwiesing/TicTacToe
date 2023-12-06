import time
import pygame


class Game():
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.round = True
        self.player = None
        self.winner = None
        self.field = {i: {'occupied': False, 'player': None} for i in range(1, 10)}

    def set_icon(self, field_number):
        print(
            f"Field Number: {field_number}, occupied: {self.field[field_number]['occupied']}, player: {self.field[field_number]['player']}")
        if self.field[field_number]['occupied'] == False:
            if self.round == True:
                self.player = 1
                self.round = False
            else:
                self.player = 0
                self.round = True
                time.sleep(.5)
            self.field[field_number]['occupied'] = True
            self.field[field_number]['player'] = self.player

    def win_round(self):
        for i in range(3):
            if (
                    all(self.field[3 * i + j]['occupied'] and self.field[3 * i + j]['player'] == self.player for j in
                        range(1, 4)) or
                    all(self.field[i + j + 2 * (j - 1)]['occupied'] and self.field[i + j + 2 * (j - 1)][
                        'player'] == self.player for j in range(1, 4))
            ):
                return True

        if (
                all(self.field[j + ((j - 1) * 3)]['occupied'] and self.field[j + ((j - 1) * 3)]['player'] == self.player
                    for j in range(1, 4)) or
                all(self.field[j + j + 1]['occupied'] and self.field[j + j + 1]['player'] == self.player for j in
                    range(1, 4))
        ):
            return True

        return False

    def display_winner(self, screen, field_checker):
        if self.winner is not None:

            # Display the winner text
            font = pygame.font.Font(None, 36)
            winner_text = font.render(f'Winner: Player {self.winner}', True, (255, 255, 255))
            screen.blit(winner_text, (260, 510))

            # Update the display
            pygame.display.flip()

            # Wait for the player to click on the game board
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
