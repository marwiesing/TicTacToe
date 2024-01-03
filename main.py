import pygame
from game_manager import GameManager
from constants import SCREEN_SIZE

pygame.init()
pygame.display.set_caption('Tic Tac Toe')
screen = pygame.display.set_mode((SCREEN_SIZE))
clock = pygame.time.Clock()

game_manager = GameManager(screen, clock)

if __name__ == '__main__':
    game_manager.run_game_loop()
    pygame.quit()