import pygame
pygame.font.init()

BUF_SIZE = 1024

SCREEN_SIZE = (1536, 864)

FPS = 60

BUTTON_WIDTH = 250
BUTTON_HEIGHT = 80

FONT = pygame.font.SysFont('rubik', 36)

APPROVE_GAME_MESSAGE = bytes((0xff, 0xff))
GET_GAME_RESULT_MESSAGE = bytes((0x11, 0x11))