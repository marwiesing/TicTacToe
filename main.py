import pygame
from gameboard import Gameboard
from game import Game

pygame.init()
pygame.display.set_caption('Tic Tac Toe')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
running = True

x, y, width, height = 240, 100, 350, 350
rows, columns = 3, 3
game_colour = (24, 181, 168)
line_color = (14, 128, 122)

field_checker = Gameboard(x, y, width, height, rows, columns)
game = Game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                print(f"Mouse click at coordinates ({x}, {y})")
                field_number = field_checker.get_field_number(x, y)
                if field_number is not None:
                    # print(f"Mouse click in field {field_number}")
                    game.set_icon(field_number)

    screen.fill(game_colour)

    pygame.draw.rect(screen, game_colour,
                     pygame.Rect(field_checker.x, field_checker.y, field_checker.width, field_checker.height), 2)
    for i in range(1, rows):
        y_position = field_checker.y + i * field_checker.row_spacing
        pygame.draw.line(screen, line_color, (field_checker.x, y_position),
                         (field_checker.x + field_checker.width, y_position), 5)

    for i in range(1, columns):
        x_position = field_checker.x + i * field_checker.col_spacing
        pygame.draw.line(screen, line_color, (x_position, field_checker.y),
                         (x_position, field_checker.y + field_checker.height), 5)

    # Draw Game Action: X or O:
    field_nr = 0
    x_position = field_checker.x
    y_position = field_checker.y
    x_spacing = field_checker.row_spacing
    y_spacing = field_checker.col_spacing
    for r in range(0, rows):
        for c in range(0, columns):
            field_nr += 1
            line1 = {
                'x1': round(x_position + (x_spacing * c) + 10),
                'y1': round(y_position + (y_spacing * r) + 10),
                'x2': round(x_position + (x_spacing * c) + 100),
                'y2': round(y_position + (y_spacing * r) + 100),
            }

            line2 = {
                'x1': round(x_position + (x_spacing * c) + 10),
                'y1': round(y_position + (y_spacing * r) + 100),
                'x2': round(x_position + (x_spacing * c) + 100),
                'y2': round(y_position + (y_spacing * r) + 10),
            }
            circle_center = (
                round(x_position + (x_spacing * c) + (x_spacing / 2)),
                round(y_position + (y_spacing * r) + (y_spacing / 2))
            )
            if game.field[field_nr]['occupied'] == True:
                if game.field[field_nr]['player'] == 1:
                    # Draw X in this field
                    pygame.draw.line(screen, line_color,
                                     (line1['x1'], line1['y1']),
                                     (line1['x2'], line1['y2']),
                                     8)
                    pygame.draw.line(screen, line_color,
                                     (line2['x1'], line2['y1']),
                                     (line2['x2'], line2['y2']),
                                     8)
                else:
                    # Draw Circle in this field
                    pygame.draw.circle(screen, line_color, circle_center, 50, 5)

    # Draw Score:
    player_score_text = font.render(f'Player: {game.player_score}', True, (255, 255, 255))
    computer_score_text = font.render(f'Computer: {game.computer_score}', True, (255, 255, 255))
    screen.blit(player_score_text, (0, 5))
    screen.blit(computer_score_text, (0, 30))

    if game.win_round():
        game.winner = game.player
        game.display_winner(screen, field_checker)
        if game.player == 1:
            game.player_score += 1
        else:
            game.computer_score += 1
        game.reset_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()