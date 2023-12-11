import pygame
from constants import GAME_COLOUR, LINE_COLOR, WINNING_COLOR


class Gameboard:
    def __init__(self, game, screen, x, y, width, height, rows, columns):
        self.game = game
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns
        self.row_spacing = height / rows
        self.col_spacing = width / columns
        self.font = pygame.font.Font(None, 36)

    def get_field_number(self, click_x, click_y):
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = self.x + col * self.col_spacing
                x2 = x1 + self.col_spacing
                y1 = self.y + row * self.row_spacing
                y2 = y1 + self.row_spacing

                if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                    return row * self.columns + col + 1
        return None

    def draw(self):
        pygame.draw.rect(self.screen, GAME_COLOUR, pygame.Rect(self.x, self.y, self.width, self.height), 2)
        for i in range(1, self.rows):
            y_position = self.y + i * self.row_spacing
            pygame.draw.line(self.screen, LINE_COLOR, (self.x, y_position), (self.x + self.width, y_position), 5)

        for i in range(1, self.columns):
            x_position = self.x + i * self.col_spacing
            pygame.draw.line(self.screen, LINE_COLOR, (x_position, self.y), (x_position, self.y + self.height), 5)

    def game_action(self):
        field_nr = 0
        x_position = self.x
        y_position = self.y
        x_spacing = self.row_spacing
        y_spacing = self.col_spacing
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                field_nr += 1
                cross_line_horizontal = {
                    'x1': round(x_position + (x_spacing * c) + 10),
                    'y1': round(y_position + (y_spacing * r) + 10),
                    'x2': round(x_position + (x_spacing * c) + 100),
                    'y2': round(y_position + (y_spacing * r) + 100),
                }

                cross_line_vertical = {
                    'x1': round(x_position + (x_spacing * c) + 10),
                    'y1': round(y_position + (y_spacing * r) + 100),
                    'x2': round(x_position + (x_spacing * c) + 100),
                    'y2': round(y_position + (y_spacing * r) + 10),
                }
                circle_center = (
                    round(x_position + (x_spacing * c) + (x_spacing / 2)),
                    round(y_position + (y_spacing * r) + (y_spacing / 2))
                )
                if self.game.field[field_nr]['occupied'] == True:
                    if self.game.field[field_nr]['player'] == 1:
                        # Draw X in this field
                        pygame.draw.line(self.screen, LINE_COLOR,
                                         (cross_line_horizontal['x1'], cross_line_horizontal['y1']),
                                         (cross_line_horizontal['x2'], cross_line_horizontal['y2']),
                                         8)
                        pygame.draw.line(self.screen, LINE_COLOR,
                                         (cross_line_vertical['x1'], cross_line_vertical['y1']),
                                         (cross_line_vertical['x2'], cross_line_vertical['y2']),
                                         8)
                    else:
                        # Draw Circle in this field
                        pygame.draw.circle(self.screen, LINE_COLOR, circle_center, 50, 5)

    def draw_winning_row(self):
        for key in self.game.field:
            if self.game.field[key]['winning_row'] == True:
                print(f'Winning fields are: {key}, Richtung: {self.game.field[key]["winning_direction"]}')

    def score(self):
        player_score_text = self.font.render(f'Player: {self.game.player_score}', True, (WINNING_COLOR))
        computer_score_text = self.font.render(f'Computer: {self.game.computer_score}', True, (WINNING_COLOR))
        self.screen.blit(player_score_text, (0, 5))
        self.screen.blit(computer_score_text, (0, 30))

