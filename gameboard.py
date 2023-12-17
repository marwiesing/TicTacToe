import pygame
from player import Player
from constants import GAME_COLOUR, LINE_COLOR, WINNING_COLOR, FIRST_DIAGONAL_ROW, SECOND_DIAGONAL_ROW, \
    COORDINATES_PLAYER_SCORE, COORDINATES_COMPUTER_SCORE


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
        self.coordinates = self.calculate_coordinates()

    def calculate_coordinates(self):
        coordinates = {}
        field_nr = 0
        for r in range(self.rows):
            for c in range(self.columns):
                field_nr += 1
                coordinates[field_nr] = {
                    'cross_line_horizontal': {
                        'x1': round(self.x + (self.row_spacing * c) + 10),
                        'y1': round(self.y + (self.col_spacing * r) + 10),
                        'x2': round(self.x + (self.row_spacing * c) + 100),
                        'y2': round(self.y + (self.col_spacing * r) + 100),
                    },
                    'cross_line_vertical': {
                        'x1': round(self.x + (self.row_spacing * c) + 10),
                        'y1': round(self.y + (self.col_spacing * r) + 100),
                        'x2': round(self.x + (self.row_spacing * c) + 100),
                        'y2': round(self.y + (self.col_spacing * r) + 10),
                    },
                    'circle_center': (
                        round(self.x + (self.row_spacing * c) + (self.row_spacing / 2)),
                        round(self.y + (self.col_spacing * r) + (self.col_spacing / 2))
                    )
                }
        return coordinates

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

    def draw_game_field(self):
        pygame.draw.rect(self.screen, GAME_COLOUR, pygame.Rect(self.x, self.y, self.width, self.height), 2)
        for i in range(1, self.rows):
            y_position = self.y + i * self.row_spacing
            pygame.draw.line(self.screen, LINE_COLOR, (self.x, y_position), (self.x + self.width, y_position), 5)

        for i in range(1, self.columns):
            x_position = self.x + i * self.col_spacing
            pygame.draw.line(self.screen, LINE_COLOR, (x_position, self.y), (x_position, self.y + self.height), 5)

    def draw_xo(self):
        for field_nr, coord in self.coordinates.items():
            if self.game.field[field_nr]['occupied'] == True:
                if self.game.field[field_nr]['player'] == Player.PLAYER_X.value:
                    # Draw X in this field
                    pygame.draw.line(self.screen, LINE_COLOR,
                                     (coord['cross_line_horizontal']['x1'], coord['cross_line_horizontal']['y1']),
                                     (coord['cross_line_horizontal']['x2'], coord['cross_line_horizontal']['y2']),
                                     8)
                    pygame.draw.line(self.screen, LINE_COLOR,
                                     (coord['cross_line_vertical']['x1'], coord['cross_line_vertical']['y1']),
                                     (coord['cross_line_vertical']['x2'], coord['cross_line_vertical']['y2']),
                                     8)
                else:
                    # Draw Circle in this field
                    pygame.draw.circle(self.screen, LINE_COLOR, coord['circle_center'], 50, 5)

    def get_winning_row(self):
        winning_directions_dict = {}
        for key, value in self.game.field.items():
            if value['winning_row'] and value['winning_direction']:
                direction = value['winning_direction']
                winning_directions_dict[direction] = [key]
                # print(winning_directions_dict)
                return winning_directions_dict
        return None

    def calculate_coordinates_for_direction(self, direction, field):
        coordinates = self.coordinates[field[0]]
        if direction == 'horizontal':
            x1 = coordinates['cross_line_horizontal']['x1']
            y1 = coordinates['circle_center'][1]
            x2 = x1 + self.row_spacing * 3
            y2 = y1
        elif direction == 'vertical':
            x1 = coordinates['circle_center'][0]
            y1 = coordinates['cross_line_horizontal']['y1']
            x2 = x1
            y2 = y1 + self.col_spacing * 3
        elif direction == 'diagonal' and field[0] == FIRST_DIAGONAL_ROW:
            x1 = coordinates['cross_line_horizontal']['x1']
            y1 = coordinates['cross_line_horizontal']['y1']
            x2 = self.coordinates[9]['cross_line_horizontal']['x2']
            y2 = self.coordinates[9]['cross_line_horizontal']['y2']
        elif direction == 'diagonal' and field[0] == SECOND_DIAGONAL_ROW:
            x1 = coordinates['cross_line_vertical']['x2']
            y1 = coordinates['cross_line_vertical']['y2']
            x2 = self.coordinates[7]['cross_line_vertical']['x1']
            y2 = self.coordinates[7]['cross_line_vertical']['y1']
        return x1, y1, x2, y2

    def draw_winning_row(self):
        winning_dict = self.get_winning_row()
        if not winning_dict:
            return None

        direction, field = list(winning_dict.items())[0]
        x1, y1, x2, y2 = self.calculate_coordinates_for_direction(direction, field)
        pygame.draw.line(self.screen, WINNING_COLOR, (x1, y1), (x2, y2), 10)

    def score(self):
        player_score_text = self.font.render(f'Player: {self.game.player_score}', True, (WINNING_COLOR))
        computer_score_text = self.font.render(f'Computer: {self.game.computer_score}', True, (WINNING_COLOR))
        self.screen.blit(player_score_text, COORDINATES_PLAYER_SCORE)
        self.screen.blit(computer_score_text, COORDINATES_COMPUTER_SCORE)

